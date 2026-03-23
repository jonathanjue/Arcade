import pygame
import sys
import math
import random
from fighter import Fighter, GROUND_Y, P1_KEYS, P2_KEYS, DOMAIN_EFFECTS
from particles import ParticleSystem
from effects import DomainExpansionOverlay
from ui import (HealthBar, CursedEnergyBar, ComboCounter, RoundIndicator,
                TitleScreen, CharacterSelect, KO_Screen, StorySelect, CHAR_COLORS,
                WHITE, YELLOW)
from story import STORY_CHAPTERS, get_chapter

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

TITLE = 'title'
CHAR_SELECT = 'char_select'
STORY_SELECT = 'story_select'
FIGHTING = 'fighting'
ROUND_END = 'round_end'
GAME_OVER = 'game_over'


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jujutsu Kaisen: Curse Clash")
        self.clock = pygame.time.Clock()
        self.state = TITLE
        self.game_mode = "ai"
        self.title_screen = TitleScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.char_select = CharacterSelect(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.story_select = StorySelect(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.ko_screen = None
        self.p1 = None
        self.p2 = None
        self.p1_char = "yuji"
        self.p2_char = "sukuna"
        self.p1_wins = 0
        self.p2_wins = 0
        self.round_timer = 99 * FPS
        self.round_number = 1
        self.winner = None
        self.p1_health = HealthBar(20, 20, 400, 25, True)
        self.p2_health = HealthBar(SCREEN_WIDTH - 420, 20, 400, 25, False)
        self.p1_energy = CursedEnergyBar(20, 50, 200, 10, True)
        self.p2_energy = CursedEnergyBar(SCREEN_WIDTH - 220, 50, 200, 10, False)
        self.combo1 = ComboCounter(50, 80)
        self.combo2 = ComboCounter(SCREEN_WIDTH - 200, 80)
        self.round_indicator = RoundIndicator(SCREEN_WIDTH // 2, 10)
        self.bg_particles = ParticleSystem()
        self.domain_overlay = None
        self.screen_shake = 0
        self.buildings = self._generate_buildings()
        self.bg_surface = None
        self._prerender_background()
        self.ai_timer = 0
        self.ai_action = {}
        self.ai_plan = []
        self.ai_plan_idx = 0
        self.round_intro_timer = 0
        self.show_round_intro = False
        self.current_chapter = None
        self.story_progress = 0
        self.p1_cooldowns = {}
        self.p2_cooldowns = {}
        # Domain background override
        self.domain_bg_color = None
        self.domain_bg_timer = 0

    def _generate_buildings(self):
        buildings = []
        x = 0
        while x < SCREEN_WIDTH + 100:
            w = random.randint(60, 150)
            h = random.randint(150, 400)
            nw = random.randint(3, 8)
            shade = random.randint(-10, 10)
            color = (20+shade, 15+shade, 30+shade)
            wins = []
            for row in range(nw):
                for col in range(w // 25):
                    if random.random() > 0.35:
                        wc = random.choice([(255,200,100),(100,180,255),(200,200,180),(255,180,80)])
                        wins.append((col, row, wc))
            buildings.append({'x':x,'w':w,'h':h,'windows':nw,'color':color,'lit':wins})
            x += w + random.randint(10, 30)
        return buildings

    def _prerender_background(self):
        self.bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            pct = y / SCREEN_HEIGHT
            r, g, b = int(25+pct*15), int(20+pct*10), int(35+pct*20)
            pygame.draw.line(self.bg_surface, (max(0,min(255,r)),max(0,min(255,g)),max(0,min(255,b))), (0,y),(SCREEN_WIDTH,y))
        for b in self.buildings:
            by = GROUND_Y - b['h'] + 80
            pygame.draw.rect(self.bg_surface, b['color'], (b['x'], by, b['w'], b['h']))
            pygame.draw.rect(self.bg_surface, (40,35,50), (b['x']+b['w']//4, by-6, b['w']//2, 6))
            for col, row, wc in b['lit']:
                wx, wy = b['x']+10+col*25, by+15+row*(b['h']//b['windows'])
                pygame.draw.rect(self.bg_surface, wc, (wx, wy, 12, 15))
        pygame.draw.rect(self.bg_surface, (35,30,45), (0,GROUND_Y+80,SCREEN_WIDTH,SCREEN_HEIGHT-GROUND_Y))
        pygame.draw.line(self.bg_surface, (80,70,90), (0,GROUND_Y+80),(SCREEN_WIDTH,GROUND_Y+80),2)

    def _draw_background(self):
        # Check for domain background override
        if self.domain_bg_timer > 0:
            self.domain_bg_timer -= 1
            # Draw tinted background
            self.screen.blit(self.bg_surface, (0,0))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            alpha = min(120, self.domain_bg_timer)
            overlay.fill((*self.domain_bg_color, alpha))
            self.screen.blit(overlay, (0,0))
            # Domain particles
            if self.domain_bg_timer % 3 == 0:
                self.bg_particles.emit(random.randint(0,SCREEN_WIDTH), random.randint(0,SCREEN_HEIGHT),
                                       2, self.domain_bg_color, (0.5,2), (2,5), (20,40), 360, 0, gravity=-0.02)
        else:
            self.screen.blit(self.bg_surface, (0,0))

        if random.random() > 0.85:
            self.bg_particles.emit(random.randint(0,SCREEN_WIDTH), GROUND_Y+65,1,(100,80,120),(0.2,0.5),(1,2),(60,120),180,270,gravity=-0.01)
        self.bg_particles.update()
        self.bg_particles.draw(self.screen)

    def _handle_collisions(self):
        for hb in self.p1.get_hitboxes():
            if hb.rect.colliderect(self.p2.get_hurtbox()):
                if self.p1.register_hit(hb, self.p2):
                    self.screen_shake = 8
                    if self.p2.health <= 0: self._round_over(self.p1)
        for hb in self.p2.get_hitboxes():
            if hb.rect.colliderect(self.p1.get_hurtbox()):
                if self.p2.register_hit(hb, self.p1):
                    self.screen_shake = 8
                    if self.p1.health <= 0: self._round_over(self.p2)

    def _round_over(self, winner):
        if winner == self.p1: self.p1_wins += 1
        else: self.p2_wins += 1
        self.state = GAME_OVER if self.p1_wins >= 2 or self.p2_wins >= 2 else ROUND_END
        self.winner = winner
        self.ko_screen = KO_Screen(SCREEN_WIDTH, SCREEN_HEIGHT)

    def _start_round(self):
        self.p1 = Fighter(200, GROUND_Y, self.p1_char, CHAR_COLORS.get(self.p1_char, (200,200,200)), True, P1_KEYS)
        self.p2 = Fighter(SCREEN_WIDTH - 200, GROUND_Y, self.p2_char, CHAR_COLORS.get(self.p2_char, (200,200,200)), False, P2_KEYS)
        self.round_timer = 99 * FPS
        self.state = FIGHTING
        self.domain_overlay = None
        self.screen_shake = 0
        self.ai_timer = 0
        self.ai_plan = []
        self.ai_plan_idx = 0
        self.p1_cooldowns = {}
        self.p2_cooldowns = {}
        self.show_round_intro = True
        self.round_intro_timer = 90
        self.domain_bg_color = None
        self.domain_bg_timer = 0

    # ============ AI ============
    def _update_ai(self):
        if self.game_mode not in ("ai", "story"):
            return
        self.ai_timer += 1
        p2, p1 = self.p2, self.p1
        if p2.hitstun > 0 or p2.blockstun > 0 or p2.stun_timer > 0:
            self.ai_action = {}
            return
        if self.ai_plan and self.ai_plan_idx < len(self.ai_plan):
            if self.ai_timer % 10 == 0: self.ai_plan_idx += 1
            self.ai_action = self.ai_plan[min(self.ai_plan_idx, len(self.ai_plan)-1)] if self.ai_plan else {}
            return
        if self.ai_timer % random.randint(14, 24) != 0:
            return
        dist = abs(p2.x - p1.x)
        right = p2.x < p1.x
        go = P2_KEYS['right'] if right else P2_KEYS['left']
        back = P2_KEYS['left'] if right else P2_KEYS['right']
        act = {}
        if p1.state in ('attack','special','ultimate') and dist < 110:
            if random.random() < 0.5:
                act[P2_KEYS['block']] = True
                self.ai_action = act
                return
        if dist < 90:
            r = random.random()
            if r < 0.28: act[P2_KEYS['jab']] = True
            elif r < 0.45: act[P2_KEYS['heavy']] = True
            elif r < 0.55: act[P2_KEYS['block']] = True
            elif r < 0.65: act[P2_KEYS['jump']] = True
            elif r < 0.75 and p2.cursed_energy >= 20:
                self.ai_plan = [{}, {go: True, P2_KEYS['jab']: True}]
                self.ai_plan_idx = 0
                return
            else: act[back] = True
        elif dist < 250:
            r = random.random()
            if r < 0.45: act[go] = True
            elif r < 0.6: act[P2_KEYS['jab']] = True
            elif r < 0.7 and p2.cursed_energy >= 25:
                self.ai_plan = [{}, {go: True, P2_KEYS['heavy']: True}]
                self.ai_plan_idx = 0
                return
            elif r < 0.8: act[P2_KEYS['jump']] = True
            else: act[back] = True
        else:
            act[go] = True
        if p2.cursed_energy >= 100 and dist < 180 and random.random() < 0.1:
            self.ai_plan = [{}, {P2_KEYS['block']: True}, {P2_KEYS['block']: True, P2_KEYS['ultimate']: True}]
            self.ai_plan_idx = 0
            return
        self.ai_action = act

    def _get_ai_keys(self):
        keys = {k: False for k in list(P2_KEYS.values())}
        for k, v in self.ai_action.items():
            if k in keys: keys[k] = v
        return keys

    # ============ MOVE LIST HUD ============
    def _draw_fight_hud(self):
        from characters import CHARACTERS
        from fighter import DOMAIN_EFFECTS
        char = CHARACTERS.get(self.p1_char, {})
        moves = char.get('moves', {})
        supers = char.get('supers', {})

        panel = pygame.Surface((240, 340), pygame.SRCALPHA)
        pygame.draw.rect(panel, (0,0,0,110), panel.get_rect(), border_radius=6)
        self.screen.blit(panel, (SCREEN_WIDTH-255, 90))

        tf = pygame.font.SysFont('arial', 12, bold=True)
        mf = pygame.font.SysFont('arial', 11)
        y = 96

        self.screen.blit(tf.render("CONTROLS", True, (200,200,210)), (SCREEN_WIDTH-245, y)); y+=16
        for c in ["WASD: Move/Jump/Block", "1: Jab", "2: Heavy", "3: Special",
                   "Q+1: Alt Light", "Q+2: Alt Heavy", "Q+3: Alt Special",
                   "Q+E: Extra Special", "E: Ultimate"]:
            self.screen.blit(mf.render(c, True, (150,150,160)), (SCREEN_WIDTH-245, y)); y+=14

        y += 4
        self.screen.blit(tf.render("ALL MOVES", True, (200,200,210)), (SCREEN_WIDTH-245, y)); y+=16

        # Show all moves with mapped input
        shown = 0
        lights = [(n,d) for n,d in moves.items() if d.get('type')=='light']
        heavies = [(n,d) for n,d in moves.items() if d.get('type')=='heavy']
        specials = [(n,d) for n,d in moves.items() if d.get('type') in ('special','trap','buff','charge','heal')]
        others = [(n,d) for n,d in moves.items() if d.get('type') not in ('light','heavy','special','trap','buff','charge','heal')]

        for i, (mname, mdata) in enumerate(lights):
            if shown >= 12: break
            inp = "1" if i==0 else ("Q+1" if i==1 else "3")
            cost = mdata.get('ce_cost',0)
            dmg = mdata.get('damage',0)
            dn = mname.replace('_',' ').title()[:18]
            c = WHITE
            line = f"{inp:>4} {dn}"
            self.screen.blit(mf.render(line, True, c), (SCREEN_WIDTH-245, y))
            self.screen.blit(mf.render(f"{dmg}d", True, (120,120,130)), (SCREEN_WIDTH-55, y))
            y += 14; shown += 1

        for i, (mname, mdata) in enumerate(heavies):
            if shown >= 12: break
            inp = "2" if i==0 else "Q+2"
            dmg = mdata.get('damage',0)
            dn = mname.replace('_',' ').title()[:18]
            self.screen.blit(mf.render(f"{inp:>4} {dn}", True, YELLOW), (SCREEN_WIDTH-245, y))
            self.screen.blit(mf.render(f"{dmg}d", True, (120,120,130)), (SCREEN_WIDTH-55, y))
            y += 14; shown += 1

        for i, (mname, mdata) in enumerate(specials):
            if shown >= 12: break
            inp = "3" if i==0 else ("Q+3" if i==1 else "Q+E")
            cost = mdata.get('ce_cost',0)
            dmg = mdata.get('damage',0)
            dn = mname.replace('_',' ').title()[:18]
            self.screen.blit(mf.render(f"{inp:>4} {dn}", True, (255,150,100)), (SCREEN_WIDTH-245, y))
            info = f"{dmg}d"
            if cost > 0: info += f" {cost}CE"
            self.screen.blit(mf.render(info, True, (180,130,100)), (SCREEN_WIDTH-65, y))
            y += 14; shown += 1

        # Super
        domain = DOMAIN_EFFECTS.get(self.p1_char, {})
        dn = domain.get('name','Super')[:22]
        dc = (100,255,100) if self.p1.cursed_energy >= 100 else (255,100,100)
        self.screen.blit(mf.render(f"  E  {dn} [100 CE]", True, dc), (SCREEN_WIDTH-245, y))

    # ============ MAIN LOOP ============
    def run(self):
        running = True
        just_pressed = {}
        while running:
            just_pressed = {}
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    just_pressed[event.key] = True
                    if event.key == pygame.K_ESCAPE:
                        if self.state in (FIGHTING, CHAR_SELECT, STORY_SELECT):
                            self.state = TITLE
                        else:
                            running = False
            keys = pygame.key.get_pressed()

            # ---- TITLE ----
            if self.state == TITLE:
                self.title_screen.draw(self.screen)
                sel = self.title_screen.handle_input(keys, just_pressed)
                if sel == 0:
                    self.game_mode = "ai"
                    self.char_select.reset()
                    self.char_select.two_player = False
                    self.state = CHAR_SELECT
                elif sel == 1:
                    self.game_mode = "2p"
                    self.char_select.reset()
                    self.char_select.two_player = True
                    self.state = CHAR_SELECT
                elif sel == 2:
                    self.game_mode = "story"
                    self.story_progress = 0
                    self.state = STORY_SELECT
                elif sel == 3:
                    running = False

            # ---- STORY SELECT ----
            elif self.state == STORY_SELECT:
                self.story_select.draw(self.screen, STORY_CHAPTERS)
                ch = self.story_select.handle_input(keys, just_pressed, len(STORY_CHAPTERS))
                if ch > 0:
                    chapter = get_chapter(ch)
                    if chapter:
                        self.current_chapter = chapter
                        self.p2_char = chapter.get('opponent_char', 'sukuna')
                        # Go to character select for P1
                        self.char_select.reset()
                        self.char_select.two_player = False
                        self.char_select.story_mode = True
                        self.char_select.story_chapter = chapter
                        self.state = CHAR_SELECT

            # ---- CHARACTER SELECT ----
            elif self.state == CHAR_SELECT:
                self.char_select.draw(self.screen)
                result = self.char_select.handle_input(keys, just_pressed)
                if result:
                    self.p1_char = result[0]
                    if self.game_mode == "story" and self.current_chapter:
                        self.p2_char = self.current_chapter.get('opponent_char', 'sukuna')
                    else:
                        self.p2_char = result[1]
                    self.p1_wins = 0
                    self.p2_wins = 0
                    self.round_number = 1
                    self._start_round()

            # ---- FIGHTING ----
            elif self.state == FIGHTING:
                if self.show_round_intro:
                    self.round_intro_timer -= 1
                    self._draw_background()
                    if self.p1: self.p1.draw(self.screen)
                    if self.p2: self.p2.draw(self.screen)
                    if self.round_intro_timer > 45:
                        f = pygame.font.SysFont('arial', 48, bold=True)
                        t = f.render(f"ROUND {self.round_number}", True, (255,200,50))
                        self.screen.blit(t, (SCREEN_WIDTH//2-t.get_width()//2, SCREEN_HEIGHT//3))
                    elif self.round_intro_timer > 0:
                        f = pygame.font.SysFont('arial', 60, bold=True)
                        t = f.render("FIGHT!", True, (255,50,50))
                        self.screen.blit(t, (SCREEN_WIDTH//2-t.get_width()//2, SCREEN_HEIGHT//2-20))
                    if self.round_intro_timer <= 0:
                        self.show_round_intro = False
                    pygame.display.flip()
                    self.clock.tick(FPS)
                    continue

                for cd_dict in (self.p1_cooldowns, self.p2_cooldowns):
                    for k in list(cd_dict.keys()):
                        cd_dict[k] -= 1
                        if cd_dict[k] <= 0: del cd_dict[k]

                self._update_ai()
                self.p1.handle_input(keys, self.p2)
                if self.game_mode in ("ai", "story"):
                    self.p2.handle_input(self._get_ai_keys(), self.p1)
                else:
                    self.p2.handle_input(keys, self.p1)
                self.p1.update(SCREEN_WIDTH)
                self.p2.update(SCREEN_WIDTH)

                # Domain triggers - set background color
                for f in [self.p1, self.p2]:
                    if f.domain_trigger:
                        domain = DOMAIN_EFFECTS.get(f.domain_trigger, {})
                        bg = domain.get('bg_color')
                        if bg:
                            self.domain_bg_color = bg
                            self.domain_bg_timer = domain.get('duration', 120)
                        f.domain_trigger = None

                self._handle_collisions()

                if self.p1.domain_active:
                    self.p1.apply_domain_effect(self.p2)
                if self.p2.domain_active:
                    self.p2.apply_domain_effect(self.p1)
                if self.p1.current_attack == 'ultimate' and self.p1.name == 'yuji':
                    self.p1.apply_combo_hit(self.p2)
                if self.p2.current_attack == 'ultimate' and self.p2.name == 'yuji':
                    self.p2.apply_combo_hit(self.p1)

                self.round_timer -= 1
                if self.round_timer <= 0:
                    self._round_over(self.p1 if self.p1.health > self.p2.health else self.p2)

                if self.domain_overlay:
                    self.domain_overlay.update()
                    if not self.domain_overlay.alive: self.domain_overlay = None
                if self.screen_shake > 0: self.screen_shake -= 1

                # ---- DRAW ----
                self._draw_background()
                self.p1.draw(self.screen)
                self.p2.draw(self.screen)
                if self.domain_overlay: self.domain_overlay.draw(self.screen)

                ui_bg = pygame.Surface((SCREEN_WIDTH, 85), pygame.SRCALPHA)
                pygame.draw.rect(ui_bg, (0,0,0,130), (0,0,SCREEN_WIDTH,85))
                self.screen.blit(ui_bg, (0,0))
                self.p1_health.draw(self.screen, self.p1)
                self.p2_health.draw(self.screen, self.p2)
                self.p1_energy.draw(self.screen, self.p1)
                self.p2_energy.draw(self.screen, self.p2)
                self.combo1.draw(self.screen, self.p1)
                self.combo2.draw(self.screen, self.p2)
                self.round_indicator.draw(self.screen, self.p1_wins, self.p2_wins)
                tf = pygame.font.SysFont('arial', 36, bold=True)
                tt = tf.render(str(max(0, self.round_timer//FPS)), True, (255,200,50))
                self.screen.blit(tt, (SCREEN_WIDTH//2-tt.get_width()//2, 40))
                rf = pygame.font.SysFont('arial', 18)
                rt = rf.render(f"Round {self.round_number}", True, (200,200,200))
                self.screen.blit(rt, (SCREEN_WIDTH//2-rt.get_width()//2, 75))
                self._draw_fight_hud()

                # Domain name display
                for f in [self.p1, self.p2]:
                    if f.domain_active:
                        domain = DOMAIN_EFFECTS.get(f.name, {})
                        dname = domain.get('name', 'DOMAIN')
                        dfont = pygame.font.SysFont('arial', 28, bold=True)
                        dt = dfont.render(dname.upper(), True, f.color)
                        self.screen.blit(dt, (SCREEN_WIDTH//2-dt.get_width()//2, 100))

            # ---- ROUND END / GAME OVER ----
            elif self.state in (ROUND_END, GAME_OVER):
                self._draw_background()
                if self.p1: self.p1.draw(self.screen)
                if self.p2: self.p2.draw(self.screen)
                if self.ko_screen:
                    self.ko_screen.draw(self.screen, self.winner.name if self.winner else "???")
                    if self.ko_screen.frame > 90:
                        if just_pressed.get(pygame.K_RETURN) or just_pressed.get(pygame.K_SPACE):
                            if self.state == GAME_OVER:
                                if self.game_mode == "story" and self.winner == self.p1:
                                    self.story_progress += 1
                                    next_ch = get_chapter(self.story_progress + 1)
                                    if next_ch:
                                        self.current_chapter = next_ch
                                        self.p1_char = next_ch.get('player_char', 'yuji')
                                        self.p2_char = next_ch.get('opponent_char', 'sukuna')
                                        self.p1_wins = 0
                                        self.p2_wins = 0
                                        self.round_number = 1
                                        self._start_round()
                                        continue
                                self.state = TITLE
                            else:
                                self.round_number += 1
                                self._start_round()

            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()
