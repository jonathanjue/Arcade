"""
engine.py - Main game loop and state machine for 2D Street Fighting Game.
"""

import pygame
import sys
import random
import traceback

from characters import CHARACTERS, list_characters, get_character, DOMAIN_EFFECTS
from fighter import (
    Fighter, GROUND_Y, IDLE, WALK_F, WALK_B, JUMP, CROUCH,
    ATTACK, SPECIAL, SUPER, BLOCK, BLOCK_STAND,
    HIT_STUN, BLOCK_STUN, KNOCKDOWN, GETUP, WIN, LOSE,
)
from particles import ParticleEmitter, hit_spark, dust_puff, block_spark, get_default_emitter
from effects import EffectManager, draw_domain_overlay
from stages import get_stage, list_stages
from ui import (
    TitleScreen, CharacterSelect, KO_Screen,
    draw_health_bar, draw_ce_bar, draw_round_counter,
    SCREEN_WIDTH, SCREEN_HEIGHT,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
FPS = 60
P1_START_X = 300
P2_START_X = 780
WINS_NEEDED = 2

# ---------------------------------------------------------------------------
# Key bindings
# ---------------------------------------------------------------------------
P1_KEYS = {
    'left':  pygame.K_a,
    'right': pygame.K_d,
    'jump':  pygame.K_w,
    'block': pygame.K_s,
    'atk1':  pygame.K_1,
    'atk2':  pygame.K_2,
    'atk3':  pygame.K_3,
    'mod':   pygame.K_q,
    'super': pygame.K_e,
}

P2_KEYS = {
    'left':  pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'jump':  pygame.K_UP,
    'block': pygame.K_DOWN,
    'atk1':  pygame.K_j,
    'atk2':  pygame.K_k,
    'atk3':  pygame.K_l,
    'mod':   pygame.K_u,
    'super': pygame.K_i,
}

_AI_BLANK = {k: False for k in P1_KEYS}


# ---------------------------------------------------------------------------
# GameEngine
# ---------------------------------------------------------------------------
class GameEngine:

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Street Fighter")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'TITLE'

        self.particles = get_default_emitter()
        self.fx = EffectManager()

        self.char_select = None
        self.p1_char = None
        self.p2_char = None
        self.stage_name = None
        self.stage_bg = None
        self.fighter1 = None
        self.fighter2 = None
        self.ko_screen = KO_Screen()
        self.p1_wins = 0
        self.p2_wins = 0
        self.round_num = 1
        self.is_ai = True
        self.round_end_timer = 0.0
        self.fight_started = False

    # ===================================================================
    # MAIN LOOP
    # ===================================================================
    def run(self):
        handlers = {
            'TITLE': self.run_title,
            'CHAR_SELECT': self.run_char_select,
            'FIGHTING': self.run_fighting,
            'ROUND_END': self.run_round_end,
            'GAME_OVER': self.run_game_over,
        }
        while self.running:
            handler = handlers.get(self.state)
            if handler:
                try:
                    handler()
                except Exception:
                    import traceback as tb
                    err = f"\n=== CRASH in state '{self.state}' ===\n"
                    err += tb.format_exc()
                    print(err)
                    # Also save to file for when terminal cuts off
                    with open("crash_log.txt", "w") as f:
                        f.write(err)
                    self.running = False
            else:
                self.running = False

        pygame.quit()
        sys.exit()

    # ===================================================================
    # TITLE
    # ===================================================================
    def run_title(self):
        title = TitleScreen()
        while self.state == 'TITLE' and self.running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.running = False
                    return
                sel = title.handle_event(ev)
                if sel is not None:
                    if sel == 0:  # VS MODE
                        self.state = 'CHAR_SELECT'
                        self._init_char_select()
                        return
                    elif sel == 2:  # QUIT
                        self.running = False
                        return
            title.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    # ===================================================================
    # CHARACTER SELECT
    # ===================================================================
    def _init_char_select(self):
        char_names = list_characters()
        roster = []
        for name in char_names:
            c = CHARACTERS[name]
            roster.append({"name": name, "color": c["color"], "moves": c.get("moves", {})})
        self.char_select = CharacterSelect(roster)
        self.char_select.current_player = 1

    def run_char_select(self):
        stage_idx = 0
        stage_names = list_stages()
        selecting_stage = False

        while self.state == 'CHAR_SELECT' and self.running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.running = False
                    return
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    self.state = 'TITLE'
                    return

                if not selecting_stage:
                    self.char_select.handle_event(ev)
                    if self.char_select.confirmed:
                        selecting_stage = True
                else:
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_UP:
                            stage_idx = (stage_idx - 1) % len(stage_names)
                        elif ev.key == pygame.K_DOWN:
                            stage_idx = (stage_idx + 1) % len(stage_names)
                        elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                            p1_name = list_characters()[self.char_select.p1_selection]
                            p2_name = list_characters()[self.char_select.p2_selection]
                            self._init_fight(p1_name, p2_name, stage_names[stage_idx])
                            return

            # --- Draw ---
            if not selecting_stage:
                self.char_select.draw(self.screen)
                font = pygame.font.SysFont('arial', 16)
                who = "P1" if self.char_select.current_player == 1 else "P2"
                hint = font.render(f"{who}  ARROWS to browse  |  ENTER to confirm", True, (200, 200, 200))
                self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)))
            else:
                self.screen.fill((15, 15, 35))
                font = pygame.font.SysFont('arial', 32, bold=True)
                small = pygame.font.SysFont('arial', 22)
                title_s = font.render("SELECT STAGE", True, (255, 255, 255))
                self.screen.blit(title_s, title_s.get_rect(center=(SCREEN_WIDTH // 2, 120)))
                for i, sn in enumerate(stage_names):
                    col = (255, 220, 0) if i == stage_idx else (180, 180, 180)
                    prefix = "> " if i == stage_idx else "  "
                    s = small.render(prefix + sn.upper(), True, col)
                    self.screen.blit(s, s.get_rect(center=(SCREEN_WIDTH // 2, 260 + i * 50)))
                foot = pygame.font.SysFont('arial', 16).render(
                    "UP/DOWN to browse  |  ENTER to confirm", True, (150, 150, 150))
                self.screen.blit(foot, foot.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)))

            pygame.display.flip()
            self.clock.tick(FPS)

    # ===================================================================
    # FIGHT INIT
    # ===================================================================
    def _init_fight(self, p1_char_name, p2_char_name, stage_name):
        self.p1_char = p1_char_name
        self.p2_char = p2_char_name
        self.stage_name = stage_name

        self.fighter1 = Fighter(p1_char_name, P1_START_X, facing_right=True)
        self.fighter2 = Fighter(p2_char_name, P2_START_X, facing_right=False)

        stage_inst = get_stage(stage_name)
        self.stage_bg = stage_inst.prerender(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.particles.clear()
        self.fx.clear_all()
        self.ko_screen = KO_Screen()
        self.p1_wins = 0
        self.p2_wins = 0
        self.round_num = 1
        self.round_end_timer = 0.0
        self.fight_started = True
        self.state = 'FIGHTING'
        # First frame tick so dt isn't huge
        self.clock.tick(FPS)

    def _reset_round(self):
        self.fighter1.reset(P1_START_X, facing_right=True)
        self.fighter2.reset(P2_START_X, facing_right=False)
        self.particles.clear()
        self.fx.clear_all()
        self.ko_screen = KO_Screen()
        self.round_end_timer = 0.0

    # ===================================================================
    # FIGHTING
    # ===================================================================
    def run_fighting(self):
        dt = self.clock.tick(FPS) / 1000.0
        dt = min(dt, 0.05)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
                return
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                self.state = 'TITLE'
                return

        try:
            keys = pygame.key.get_pressed()

            # Face each other
            self.fighter1.facing_right = self.fighter1.x < self.fighter2.x
            self.fighter2.facing_right = self.fighter2.x < self.fighter1.x

            # P1 input
            self.fighter1.handle_input(keys, P1_KEYS, self.fighter2)

            # P2 input (human or AI)
            if not self.is_ai:
                self.fighter2.handle_input(keys, P2_KEYS, self.fighter1)
            else:
                ai_keys = _build_ai_keys(self.fighter2, self.fighter1)
                self.fighter2.handle_input(ai_keys, P1_KEYS, self.fighter1)

            # Update fighters
            try:
                self.fighter1.update(SCREEN_WIDTH, self.particles)
            except Exception as e:
                import traceback as tb
                err = f"fighter1.update CRASH: {e}\n{tb.format_exc()}"
                print(err)
                with open("crash_fighter.txt", "w") as f:
                    f.write(err)
                self.running = False
                return
            try:
                self.fighter2.update(SCREEN_WIDTH, self.particles)
            except Exception as e:
                import traceback as tb
                err = f"fighter2.update CRASH: {e}\n{tb.format_exc()}"
                print(err)
                with open("crash_fighter.txt", "w") as f:
                    f.write(err)
                self.running = False
                return

            # Hitbox collisions
            self._resolve_hitboxes(self.fighter1, self.fighter2)
            self._resolve_hitboxes(self.fighter2, self.fighter1)

            # Particles
            self.particles.update(dt)

            # Domain effects
            self._apply_domains()

            # KO check
            ko_happened = False
            if self.fighter1.hp <= 0:
                self.p2_wins += 1
                self.ko_screen.trigger(2)
                self.fighter1.state = LOSE
                self.fighter2.state = WIN
                ko_happened = True
            elif self.fighter2.hp <= 0:
                self.p1_wins += 1
                self.ko_screen.trigger(1)
                self.fighter1.state = WIN
                self.fighter2.state = LOSE
                ko_happened = True

            if ko_happened:
                self.state = 'ROUND_END'
                self.round_end_timer = 0.0
                return

            # Draw
            try:
                self._draw_fight()
            except Exception as e:
                import traceback as tb
                err = f"_draw_fight CRASH: {e}\n{tb.format_exc()}"
                print(err)
                with open("crash_fighter.txt", "w") as f:
                    f.write(err)
                self.running = False

        except Exception:
            import traceback as tb
            err = tb.format_exc()
            print(err)
            with open("crash_log.txt", "w") as f:
                f.write(err)
            self.running = False

    # ===================================================================
    # ROUND END
    # ===================================================================
    def run_round_end(self):
        dt = self.clock.tick(FPS) / 1000.0
        dt = min(dt, 0.05)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
                return
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                self.state = 'TITLE'
                return

        self.ko_screen.update()
        self.particles.update(dt)
        self.round_end_timer += dt

        self._draw_fight()

        if self.round_end_timer > 3.5 or not self.ko_screen.active:
            self._after_ko()

    def _after_ko(self):
        if self.p1_wins >= WINS_NEEDED or self.p2_wins >= WINS_NEEDED:
            self.state = 'GAME_OVER'
        else:
            self.round_num += 1
            self._reset_round()
            self.state = 'FIGHTING'

    # ===================================================================
    # GAME OVER
    # ===================================================================
    def run_game_over(self):
        self.clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
                return
            if ev.type == pygame.KEYDOWN:
                self.state = 'TITLE'
                return

        self.screen.fill((10, 10, 25))
        font_big = pygame.font.SysFont('arial', 64, bold=True)
        font_med = pygame.font.SysFont('arial', 32)
        winner = 1 if self.p1_wins >= WINS_NEEDED else 2
        win_name = self.p1_char if winner == 1 else self.p2_char

        t1 = font_big.render("GAME OVER", True, (255, 220, 0))
        self.screen.blit(t1, t1.get_rect(center=(SCREEN_WIDTH // 2, 200)))

        t2 = font_med.render(f"PLAYER {winner}  ({win_name})  WINS!", True, (0, 200, 255))
        self.screen.blit(t2, t2.get_rect(center=(SCREEN_WIDTH // 2, 310)))

        t3 = font_med.render(f"{self.p1_wins} - {self.p2_wins}", True, (200, 200, 200))
        self.screen.blit(t3, t3.get_rect(center=(SCREEN_WIDTH // 2, 380)))

        font_sm = pygame.font.SysFont('arial', 20)
        t4 = font_sm.render("Press any key to continue", True, (140, 140, 140))
        self.screen.blit(t4, t4.get_rect(center=(SCREEN_WIDTH // 2, 500)))

        pygame.display.flip()

    # ===================================================================
    # DRAW
    # ===================================================================
    def _draw_fight(self):
        # Stage background
        if self.stage_bg:
            self.screen.blit(self.stage_bg, (0, 0))
        else:
            self.screen.fill((30, 30, 50))

        # Domain overlay (under fighters)
        for f in (self.fighter1, self.fighter2):
            if f.domain_active:
                effect = DOMAIN_EFFECTS.get(f.domain_active, {})
                color = effect.get('color', (200, 200, 255))
                draw_domain_overlay(self.screen, color, f.domain_timer, 180)

        # Fighters
        self.fighter1.draw(self.screen, self.particles)
        self.fighter2.draw(self.screen, self.particles)

        # Particles
        self.particles.draw(self.screen)

        # Visual effects
        self.fx.update()
        self.fx.draw(self.screen)

        # HUD
        draw_health_bar(self.screen, 20, 10,
                        self.fighter1.hp, self.fighter1.max_hp,
                        self.fighter1.color, self.fighter1.name)
        draw_ce_bar(self.screen, 20, 65,
                    self.fighter1.cursed_energy, self.fighter1.max_ce)

        draw_health_bar(self.screen, SCREEN_WIDTH - 440, 10,
                        self.fighter2.hp, self.fighter2.max_hp,
                        self.fighter2.color, self.fighter2.name, flip=True)
        draw_ce_bar(self.screen, SCREEN_WIDTH - 440, 65,
                    self.fighter2.cursed_energy, self.fighter2.max_ce)

        draw_round_counter(self.screen, self.p1_wins, self.p2_wins, self.round_num)

        # Combo counters
        self._draw_combo(self.fighter1, 240, 90)
        self._draw_combo(self.fighter2, SCREEN_WIDTH - 240, 90)

        # KO overlay
        if self.ko_screen.active:
            self.ko_screen.draw(self.screen)

        # Ground line
        pygame.draw.line(self.screen, (60, 60, 60), (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 1)

        pygame.display.flip()

    def _draw_combo(self, fighter, cx, y):
        if fighter.combo_count > 1 and fighter.combo_timer > 0:
            font = pygame.font.SysFont('arial', 22, bold=True)
            txt = font.render(f"{fighter.combo_count} HIT!", True, (255, 255, 80))
            rect = txt.get_rect(center=(cx, y))
            bg = pygame.Surface((rect.width + 16, rect.height + 8), pygame.SRCALPHA)
            bg.fill((0, 0, 0, 160))
            self.screen.blit(bg, (rect.x - 8, rect.y - 4))
            self.screen.blit(txt, rect)

    # ===================================================================
    # COLLISION
    # ===================================================================
    def _resolve_hitboxes(self, attacker, defender):
        if not attacker.hitboxes:
            return

        opp_rect = defender.get_rect()

        for hb in attacker.hitboxes:
            if hb.hit:
                continue
            if not hb.rect.colliderect(opp_rect):
                continue

            is_blocking = defender.state in (BLOCK_STAND, BLOCK)

            defender.take_damage(
                hb.damage, hb.kbx, hb.kby,
                hitstun=hb.hitstun, is_blocking=is_blocking,
            )
            attacker.register_hit(defender)
            hb.hit = True

            # Visual feedback
            hx = int((hb.x + hb.w / 2 + defender.x) / 2)
            hy = int(hb.y + hb.h / 2)
            if is_blocking:
                block_spark(hx, hy)
            else:
                hit_spark(hx, hy, attacker.color)

    # ===================================================================
    # DOMAIN EFFECTS
    # ===================================================================
    def _apply_domains(self):
        try:
            self.fighter1.apply_domain_effect(self.fighter2)
            self.fighter2.apply_domain_effect(self.fighter1)
        except Exception:
            pass

def _build_ai_keys(fighter, opponent):
    """Build a pygame key-style dict for the AI. Keys are integer pygame constants."""
    keys = {v: False for v in P1_KEYS.values()}

    dist = abs(fighter.x - opponent.x)
    prefs = fighter.ai_prefs if hasattr(fighter, 'ai_prefs') else {}
    aggression = prefs.get('aggression', 0.5)
    zoning = prefs.get('zoning', 0.3)

    if fighter.state in (HIT_STUN, BLOCK_STUN, KNOCKDOWN, ATTACK, SPECIAL, SUPER, WIN, LOSE):
        return keys

    r = random.random()

    # Block reaction
    if opponent.state in (ATTACK, SPECIAL) and dist < 140 and r < 0.6:
        keys[P1_KEYS['block']] = True
        return keys

    super_entry = fighter.move_map.get('super')
    super_cost = super_entry[1].get('ce_cost', 999) if super_entry else 999
    atk3_entry = fighter.move_map.get('atk3')
    atk3_cost = atk3_entry[1].get('ce_cost', 999) if atk3_entry else 999

    atk_button = None
    atk_mod = False

    if dist < 130:
        if r < aggression * 0.35:
            if r < 0.07 and fighter.cursed_energy >= super_cost:
                atk_button, atk_mod = 'super', False
            elif r < 0.18 and fighter.cursed_energy >= atk3_cost:
                atk_button = 'atk3'
            else:
                atk_button = random.choice(['atk1', 'atk1', 'atk2'])
        elif r < aggression * 0.35 + 0.12:
            keys[P1_KEYS['jump']] = True
        elif r < aggression * 0.35 + 0.22:
            keys[P1_KEYS['block']] = True
            return keys

    elif dist < 300:
        if r < aggression * 0.20:
            if r < 0.04 and fighter.cursed_energy >= super_cost:
                atk_button, atk_mod = 'super', False
            elif r < 0.10 and fighter.cursed_energy >= atk3_cost:
                atk_button = 'atk3'
            else:
                atk_button = random.choice(['atk1', 'atk2'])
        elif r < aggression * 0.20 + 0.10:
            keys[P1_KEYS['jump']] = True
        else:
            if fighter.facing_right:
                keys[P1_KEYS['right']] = True
            else:
                keys[P1_KEYS['left']] = True

    else:
        has_proj = any(m.get('type') == 'projectile' for m in fighter.moves.values() if isinstance(m, dict))
        if zoning > 0.5 and has_proj and r < zoning * 0.35:
            if fighter.cursed_energy >= atk3_cost:
                atk_button = 'atk3'
            else:
                if fighter.facing_right:
                    keys[P1_KEYS['right']] = True
                else:
                    keys[P1_KEYS['left']] = True
        else:
            if fighter.facing_right:
                keys[P1_KEYS['right']] = True
            else:
                keys[P1_KEYS['left']] = True
            if r > 0.82:
                keys[P1_KEYS['jump']] = True

    if atk_button:
        keys[P1_KEYS[atk_button]] = True
        if atk_mod:
            keys[P1_KEYS['mod']] = True

    return keys


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    game = GameEngine()
    game.run()


if __name__ == "__main__":
    main()
