"""Fighter class — core combat entity for 2D street fighting game."""

import pygame
import math
import random
from characters import CHARACTERS, get_character

# --- Constants ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 220, 50)
GROUND_Y = 520
SCREEN_WIDTH = 1080
FIGHTER_W = 50
FIGHTER_H = 90
GRAVITY = 0.65

# --- States ---
IDLE = 'idle'
WALK_F = 'walk_f'
WALK_B = 'walk_b'
JUMP = 'jump'
CROUCH = 'crouch'
ATTACK = 'attack'
BLOCK = 'block'
BLOCK_STAND = 'block_stand'
HIT_STUN = 'hit_stun'
BLOCK_STUN = 'block_stun'
KNOCKDOWN = 'knockdown'
GETUP = 'getup'
SPECIAL = 'special'
SUPER = 'super'
WIN = 'win'
LOSE = 'lose'


class Hitbox:
    """Active hitbox during attacks."""
    __slots__ = ['x', 'y', 'w', 'h', 'damage', 'kbx', 'kby', 'owner', 'hit', 'hitstun', 'blockstun']

    def __init__(self, x, y, w, h, damage, kbx, kby, owner, hitstun=12, blockstun=8):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.damage = damage
        self.kbx, self.kby = kbx, kby
        self.owner = owner
        self.hit = False
        self.hitstun = hitstun
        self.blockstun = blockstun

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


class Fighter:
    """A fighting game character."""

    def __init__(self, char_id, x, facing_right=True):
        data = get_character(char_id)
        self.char_id = char_id
        self.name = data['name']
        self.color = data['color']
        self.body_color = data.get('body_color', data['color'])
        self.speed = data['speed']
        self.jump_power = data['jump_power']
        self.max_hp = data['max_hp']
        self.hp = self.max_hp
        self.weight = data['weight']
        self.moves = data['moves']
        self.ai_prefs = data.get('ai', {})
        self.atk_style = data.get('attack_styles', {'light': 'punch', 'heavy': 'kick', 'trail': self.color})

        # Position & physics
        self.x = float(x)
        self.y = float(GROUND_Y)
        self.vx = 0.0
        self.vy = 0.0
        self.facing_right = facing_right
        self.on_ground = True

        # State
        self.state = IDLE
        self.state_frame = 0
        self.hitstun_timer = 0
        self.ko_timer = 0
        self.invincible = 0

        # Combat
        self.cursed_energy = 50.0
        self.max_ce = 100.0
        self.hitboxes = []
        self.current_attack = None
        self.attack_startup = 0
        self.attack_active = 0
        self.attack_recovery = 0
        self.combo_count = 0
        self.combo_damage = 0
        self.combo_timer = 0

        # Super / domain
        self.domain_active = None
        self.domain_timer = 0
        self.domain_trigger = None
        self.buffs = {}

        # Visual
        self.squash = 1.0
        self.stretch = 1.0
        self.flash_timer = 0
        self.punch_extend = 0

        # Build move mapping
        self._build_move_map()

    def _build_move_map(self):
        """Map keyboard inputs to moves. Uses strike/projectile/grab types from characters.py.
        Supers are detected by high CE cost (>=50)."""
        strikes = [(n, d) for n, d in self.moves.items() if d.get('type') == 'strike']
        projectiles = [(n, d) for n, d in self.moves.items() if d.get('type') == 'projectile' and d.get('ce_cost', 0) < 50]
        grabs = [(n, d) for n, d in self.moves.items() if d.get('type') == 'grab' and d.get('ce_cost', 0) < 50]
        supers = [(n, d) for n, d in self.moves.items() if d.get('ce_cost', 0) >= 50]
        # Also check for 'super' type explicitly
        supers += [(n, d) for n, d in self.moves.items() if d.get('type') == 'super' and (n, d) not in supers]
        self.move_map = {}
        if strikes: self.move_map['atk1'] = strikes[0]
        if len(strikes) > 1: self.move_map['atk2'] = strikes[1]
        if len(strikes) > 2: self.move_map['mod_atk1'] = strikes[2]
        if projectiles:
            self.move_map['atk3'] = projectiles[0]
        elif len(strikes) > 3:
            self.move_map['atk3'] = strikes[3]  # fallback
        if len(projectiles) > 1:
            self.move_map['mod_atk2'] = projectiles[1]
        elif len(strikes) > 4:
            self.move_map['mod_atk2'] = strikes[4]
        if grabs:
            self.move_map['mod_atk3'] = grabs[0]
        elif len(strikes) > 5:
            self.move_map['mod_atk3'] = strikes[5]
        if supers: self.move_map['super'] = supers[0]

    def reset(self, x, facing_right=True):
        """Reset for new round."""
        self.x = float(x)
        self.y = float(GROUND_Y)
        self.vx, self.vy = 0, 0
        self.hp = self.max_hp
        self.cursed_energy = 50.0
        self.state = IDLE
        self.state_frame = 0
        self.hitboxes = []
        self.hitstun_timer = 0
        self.invincible = 0
        self.combo_count = 0
        self.combo_timer = 0
        self.domain_active = None
        self.domain_timer = 0
        self.buffs = {}
        self.facing_right = facing_right
        self.on_ground = True

    def handle_input(self, keys, p1_keys, opponent):
        """Process input and update state. p1_keys is a dict of key bindings."""
        try:
            self._handle_input_inner(keys, p1_keys, opponent)
        except Exception as e:
            import traceback as tb
            err = f"handle_input CRASH: {e}\n{tb.format_exc()}"
            print(err)
            with open("crash_fighter.txt", "w") as f:
                f.write(err)
            raise

    def _handle_input_inner(self, keys, p1_keys, opponent):
        """Actual input handling logic."""
        if self.state in (HIT_STUN, BLOCK_STUN, KNOCKDOWN, GETUP, WIN, LOSE, SUPER):
            return

        # Normalize keys: convert any format to a simple dict
        k = {}
        for action, keycode in p1_keys.items():
            try:
                k[action] = bool(keys[keycode])
            except (KeyError, IndexError, TypeError):
                k[action] = False

        mod = k['mod']
        super_key = k['super']

        # Check attacks (mod+button BEFORE bare button)
        if self.state not in (ATTACK, SPECIAL):
            if mod and super_key and 'super' in self.move_map:
                self._try_move(self.move_map['super'][1], 'super')
            elif mod and k['atk3'] and 'mod_atk3' in self.move_map:
                self._try_move(self.move_map['mod_atk3'][1], 'mod_atk3')
            elif mod and k['atk2'] and 'mod_atk2' in self.move_map:
                self._try_move(self.move_map['mod_atk2'][1], 'mod_atk2')
            elif mod and k['atk1'] and 'mod_atk1' in self.move_map:
                self._try_move(self.move_map['mod_atk1'][1], 'mod_atk1')
            elif k['atk3'] and 'atk3' in self.move_map:
                self._try_move(self.move_map['atk3'][1], 'atk3')
            elif k['atk2'] and 'atk2' in self.move_map:
                self._try_move(self.move_map['atk2'][1], 'atk2')
            elif k['atk1'] and 'atk1' in self.move_map:
                self._try_move(self.move_map['atk1'][1], 'atk1')

        # Movement (only if not attacking)
        if self.state not in (ATTACK, SPECIAL, BLOCK, BLOCK_STAND):
            left = k['left']
            right = k['right']
            jump = k['jump']
            block = k['block']

            if block:
                self.state = BLOCK_STAND if self.on_ground else IDLE
                self.vx = 0
            elif left:
                self.state = WALK_B if self.facing_right else WALK_F
                self.vx = -self.speed
            elif right:
                self.state = WALK_F if self.facing_right else WALK_B
                self.vx = self.speed
            else:
                if self.on_ground and self.state not in (JUMP, CROUCH):
                    self.state = IDLE
                self.vx = 0

            if jump and self.on_ground:
                self.vy = -self.jump_power
                self.on_ground = False
                self.state = JUMP
                self.squash = 0.7
                self.stretch = 1.3

    def _try_move(self, move_data, key_name):
        """Attempt to execute a move."""
        ce_cost = move_data.get('ce_cost', 0)
        if self.cursed_energy < ce_cost:
            return
        self.cursed_energy -= ce_cost
        mtype = move_data.get('type', 'strike')

        if mtype == 'super':
            self.state = SUPER
            self.state_frame = 0
            self.current_attack = move_data
            self.domain_trigger = self.char_id
            self.vx = 0
        elif mtype in ('projectile', 'grab'):
            self.state = SPECIAL
            self.state_frame = 0
            self.current_attack = move_data
            self.attack_startup = move_data.get('startup', 6)
            self.attack_active = move_data.get('active', 6)
            self.attack_recovery = move_data.get('recovery', 12)
            self.punch_extend = 0
            self.vx = 0
        else:  # strike
            self.state = ATTACK
            self.state_frame = 0
            self.current_attack = move_data
            self.attack_startup = move_data.get('startup', 4)
            self.attack_active = move_data.get('active', 4)
            self.attack_recovery = move_data.get('recovery', 8)
            self.punch_extend = 0
            self.vx = 0

    def start_attack(self, atype='light'):
        """Legacy method for simple attacks."""
        if atype in self.move_map:
            self._try_move(self.move_map[atype][1], atype)

    def update(self, screen_width, particles=None):
        """Update physics, state, and combat."""
        self.state_frame += 1

        # CE regen
        if self.cursed_energy < self.max_ce:
            self.cursed_energy = min(self.max_ce, self.cursed_energy + 0.3)

        # Combo timer decay
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_count = 0
            self.combo_damage = 0

        # Invincibility decay
        if self.invincible > 0:
            self.invincible -= 1

        # Squash/stretch decay
        self.squash += (1.0 - self.squash) * 0.15
        self.stretch += (1.0 - self.stretch) * 0.15

        # Flash decay
        if self.flash_timer > 0:
            self.flash_timer -= 1

        # Domain timer
        if self.domain_active:
            self.domain_timer -= 1
            if self.domain_timer <= 0:
                self.domain_active = None

        # Hitstun
        if self.state == HIT_STUN:
            self.hitstun_timer -= 1
            self.vx *= 0.85
            if self.hitstun_timer <= 0:
                self.state = IDLE
            self._apply_physics(screen_width)
            return

        # Block stun
        if self.state == BLOCK_STUN:
            self.hitstun_timer -= 1
            self.vx *= 0.85
            if self.hitstun_timer <= 0:
                self.state = IDLE
            self._apply_physics(screen_width)
            return

        # Knockdown
        if self.state == KNOCKDOWN:
            self.vx *= 0.9
            self._apply_physics(screen_width)
            if self.on_ground and self.state_frame > 30:
                self.state = GETUP
                self.state_frame = 0
                self.invincible = 40
            return

        # Getup
        if self.state == GETUP:
            self.vx = 0
            if self.state_frame > 40:
                self.state = IDLE
            return

        # Win/lose
        if self.state in (WIN, LOSE):
            self.vx = 0
            return

        # Attack state
        if self.state in (ATTACK, SPECIAL):
            self._update_attack(particles)
            self._apply_physics(screen_width)
            return

        # Super state
        if self.state == SUPER:
            if self.state_frame > 60:
                self.state = IDLE
                self.domain_active = self.char_id
                self.domain_timer = 180
                self.domain_trigger = None
            self._apply_physics(screen_width)
            return

        # Normal physics
        self._apply_physics(screen_width)

    def _update_attack(self, particles=None):
        """Handle attack phases: startup -> active -> recovery."""
        if self.current_attack is None:
            self.state = IDLE
            return

        total_startup = self.attack_startup
        total_active = total_startup + self.attack_active
        total_recovery = total_active + self.attack_recovery

        # Punch extend animation
        if self.state_frame <= total_startup:
            self.punch_extend = min(1.0, self.punch_extend + 0.2)
        elif self.state_frame <= total_active:
            self.punch_extend = 1.0
            # Spawn hitbox
            if not self.hitboxes:
                dmg = self.current_attack.get('damage', 20)
                kbx = self.current_attack.get('knockback_x', 5) * self.weight
                kby = self.current_attack.get('knockback_y', -3)
                hitstun = self.current_attack.get('hitstun', 12)
                blockstun = self.current_attack.get('blockstun', 8)
                rng = self.current_attack.get('range', 55)
                dir = 1 if self.facing_right else -1
                hx = self.x + dir * 25
                hy = self.y - 50
                self.hitboxes = [Hitbox(hx, hy, rng, 30, dmg, kbx * dir, kby, self, hitstun, blockstun)]
            # Update hitbox position
            dir = 1 if self.facing_right else -1
            self.hitboxes[0].x = self.x + dir * 25
            self.hitboxes[0].y = self.y - 50
        elif self.state_frame <= total_recovery:
            self.punch_extend = max(0, self.punch_extend - 0.15)
            self.hitboxes = []
        else:
            self.state = IDLE
            self.hitboxes = []
            self.current_attack = None
            self.punch_extend = 0

    def _apply_physics(self, screen_width):
        """Apply gravity and boundary clamping."""
        if not self.on_ground:
            self.vy += GRAVITY

        self.x += self.vx
        self.y += self.vy

        # Ground collision
        if self.y >= GROUND_Y:
            if not self.on_ground and self.vy > 5:
                self.squash = 1.3
                self.stretch = 0.7
            self.y = GROUND_Y
            self.vy = 0
            self.on_ground = True
            if self.state == JUMP:
                self.state = IDLE

        # Airborne stretch
        if not self.on_ground and self.vy > 2:
            self.stretch = 1.15
            self.squash = 0.9

        # Screen bounds
        self.x = max(FIGHTER_W / 2, min(screen_width - FIGHTER_W / 2, self.x))

    def take_damage(self, damage, kbx, kby, hitstun=12, is_blocking=False):
        """Receive damage from a hit."""
        if self.invincible > 0:
            return False

        if is_blocking or self.state in (BLOCK, BLOCK_STAND):
            # Blocked
            self.hp -= int(damage * 0.15)
            self.state = BLOCK_STUN
            self.hitstun_timer = max(8, hitstun - 4)
            self.vx = kbx * 0.3
            return True

        # Damage scaling from combos
        scale = max(0.5, 1.0 - self.combo_count * 0.1)
        actual_damage = int(damage * scale)
        self.hp = max(0, self.hp - actual_damage)

        # Apply knockback
        self.vx = kbx / self.weight
        self.vy = kby / self.weight

        if abs(kbx) > 8 or kby < -8:
            # Big knockback -> knockdown
            self.state = KNOCKDOWN
            self.state_frame = 0
            self.on_ground = False
        else:
            self.state = HIT_STUN
            self.hitstun_timer = hitstun

        self.flash_timer = 8
        return True

    def register_hit(self, opponent):
        """Called when this fighter's attack connects."""
        self.cursed_energy = min(self.max_ce, self.cursed_energy + 10)
        self.combo_count += 1
        self.combo_timer = 60  # 1 second to continue combo

    def apply_domain_effect(self, opponent):
        """Apply domain/super effect to opponent each frame."""
        if not self.domain_active:
            return
        from characters import DOMAIN_EFFECTS
        effect = DOMAIN_EFFECTS.get(self.domain_active, {})
        etype = effect.get('type', 'zone_damage')

        if etype == 'zone_damage':
            dist = abs(self.x - opponent.x)
            if dist < 350 and self.domain_timer % 15 == 0:
                opponent.take_damage(effect.get('dps', 3) * 8, 3 if self.facing_right else -3, -2)
        elif etype == 'stun':
            if self.domain_timer == 179:  # First frame
                opponent.state = HIT_STUN
                opponent.hitstun_timer = effect.get('stun_duration', 90)
                opponent.vx = 0
        elif etype == 'self_buff':
            self.buffs['damage_boost'] = effect.get('damage_boost', 1.5)
        elif etype == 'combo':
            if self.domain_timer % 20 == 0 and self.domain_timer > 120:
                opponent.take_damage(effect.get('dmg_per_hit', 25), 5 if self.facing_right else -5, -3)

    # --- DRAWING ---

    def draw(self, surface, particles=None):
        """Draw the fighter."""
        cx = int(self.x)
        cy = int(self.y)
        dir = 1 if self.facing_right else -1

        # Flash effect
        if self.flash_timer > 0 and self.flash_timer % 2 == 0:
            draw_color = WHITE
        else:
            draw_color = self.body_color

        # Squash/stretch
        w = int(FIGHTER_W * self.squash)
        h = int(FIGHTER_H * self.stretch)

        lean = int(self.vx * 0.5) if self.state in (WALK_F, WALK_B) else 0
        bob = math.sin(self.state_frame * 0.15) * 2 if self.state == IDLE else 0

        top = cy - h + int(bob)
        bot = cy

        # Legs
        leg_spread = 8 if self.state in (WALK_F, WALK_B) else 5
        leg_bob = int(math.sin(self.state_frame * 0.3) * 5) if self.state in (WALK_F, WALK_B) else 0
        pygame.draw.line(surface, draw_color, (cx - 4, cy - 15), (cx - leg_spread + leg_bob, bot), 5)
        pygame.draw.line(surface, draw_color, (cx + 4, cy - 15), (cx + leg_spread - leg_bob, bot), 5)

        # Crouch
        if self.state == CROUCH:
            top = cy - h // 2 + 10

        # Body
        body_rect = pygame.Rect(cx - w // 2 + lean, top + 15, w, h - 30)
        pygame.draw.rect(surface, draw_color, body_rect, border_radius=6)

        # Belt / detail line
        pygame.draw.line(surface, BLACK, (cx - w // 2 + 3 + lean, cy - 15), (cx + w // 2 - 3 + lean, cy - 15), 2)

        # Head
        head_r = 14
        head_y = top + head_r + 2
        pygame.draw.circle(surface, draw_color, (cx + lean, head_y), head_r)

        # Character-specific details
        self._draw_detail(surface, cx, top, bot, dir, lean, bob, draw_color)

        # Face
        self._draw_face(surface, cx + lean, head_y, dir)

        # Arms
        self._draw_arms(surface, cx, top + 20, lean, dir, draw_color)

        # Hitbox debug (comment out for release)
        # for hb in self.hitboxes:
        #     pygame.draw.rect(surface, (255, 0, 0, 100), hb.rect, 2)

    def _draw_detail(self, surface, cx, top, bot, dir, lean, bob, color):
        """Character-specific visual details."""
        if self.char_id == 'ryu':
            # Headband
            pygame.draw.line(surface, (200, 50, 50), (cx - 14 + lean, top + 8 + bob), (cx + 14 + lean, top + 8 + bob), 3)
            # Tied ends
            pygame.draw.line(surface, (200, 50, 50), (cx - 14 + lean, top + 8 + bob), (cx - 20 + lean, top + 3 + bob), 2)
        elif self.char_id == 'blaze':
            # Boxing gloves (bigger hands)
            pass  # drawn in arms
        elif self.char_id == 'titan':
            # Shoulder pads
            pygame.draw.ellipse(surface, (120, 120, 130), (cx - 28 + lean, top + 14 + bob, 18, 12))
            pygame.draw.ellipse(surface, (120, 120, 130), (cx + 10 + lean, top + 14 + bob, 18, 12))
        elif self.char_id == 'viper':
            # Mask lower face
            pygame.draw.rect(surface, (60, 80, 60), (cx - 10 + lean, top + 14 + bob, 20, 8), border_radius=3)
        elif self.char_id == 'storm':
            # Cape edges
            pygame.draw.line(surface, (80, 80, 160), (cx - 18 + lean, top + 15 + bob), (cx - 22 + lean, bot - 10), 3)
            pygame.draw.line(surface, (80, 80, 160), (cx + 18 + lean, top + 15 + bob), (cx + 22 + lean, bot - 10), 3)
        elif self.char_id == 'crusher':
            # Spiked hair
            for i in range(-2, 3):
                hx = cx + i * 5 + lean
                hy = top - 2 + bob
                pygame.draw.line(surface, (180, 50, 50), (hx, hy + 8), (hx + i * 2, hy), 3)

    def _draw_face(self, surface, cx, hy, dir):
        """Draw face expression."""
        if self.state == HIT_STUN or self.flash_timer > 0:
            # Hurt face - X eyes
            for ex in [cx - 6, cx + 6]:
                pygame.draw.line(surface, BLACK, (ex - 3, hy - 3), (ex + 3, hy + 3), 2)
                pygame.draw.line(surface, BLACK, (ex - 3, hy + 3), (ex + 3, hy - 3), 2)
            # Open mouth
            pygame.draw.ellipse(surface, (80, 20, 20), (cx - 4, hy + 5, 8, 5))
            return

        if self.state == BLOCK or self.state == BLOCK_STAND:
            # Gritted teeth
            pygame.draw.line(surface, BLACK, (cx - 4, hy + 6), (cx + 4, hy + 6), 2)
            # Squinting eyes
            pygame.draw.line(surface, BLACK, (cx - 8, hy), (cx - 3, hy), 2)
            pygame.draw.line(surface, BLACK, (cx + 3, hy), (cx + 8, hy), 2)
            return

        if self.state == WIN:
            # Happy - big smile
            pygame.draw.arc(surface, BLACK, (cx - 5, hy + 1, 10, 8), 3.14, 6.28, 2)
            # Eyes
            pygame.draw.circle(surface, BLACK, (cx - 6, hy - 1), 2)
            pygame.draw.circle(surface, BLACK, (cx + 6, hy - 1), 2)
            return

        # Normal face
        # Eyes
        pygame.draw.circle(surface, BLACK, (cx - 6 + dir, hy - 1), 2)
        pygame.draw.circle(surface, BLACK, (cx + 6 + dir, hy - 1), 2)
        # Mouth
        pygame.draw.line(surface, BLACK, (cx - 3 + dir * 2, hy + 6), (cx + 3 + dir * 2, hy + 6), 1)

    def _draw_arms(self, surface, cx, ay, lean, dir, color):
        """Draw arms — attacking arm extends during attacks."""
        # Back arm (always tucked)
        bx = cx - dir * 15 + lean
        pygame.draw.line(surface, color, (cx + lean, ay), (bx, ay + 5), 5)

        # Front arm
        if self.state in (ATTACK, SPECIAL) and self.punch_extend > 0:
            # Extended punch
            ext = int(self.punch_extend * 35)
            fx = cx + dir * (20 + ext) + lean
            fy = ay - 3
            pygame.draw.line(surface, color, (cx + dir * 15 + lean, ay), (fx, fy), 5)
            # Fist
            fist_r = 8 if self.char_id == 'blaze' else 6
            pygame.draw.circle(surface, color, (fx, fy), fist_r)
            # Attack trail particles hint
            if self.punch_extend > 0.5:
                trail = self.atk_style.get('trail', self.color)
                for i in range(3):
                    tx = fx - dir * (5 + i * 8)
                    ty = fy + random.randint(-3, 3)
                    pygame.draw.circle(surface, trail, (tx, ty), max(1, 4 - i))
        elif self.state in (BLOCK, BLOCK_STAND):
            # Block stance - arms crossed
            pygame.draw.line(surface, color, (cx + dir * 10 + lean, ay - 5), (cx + dir * 5 + lean, ay + 10), 5)
            pygame.draw.line(surface, color, (cx - dir * 5 + lean, ay - 5), (cx + dir * 5 + lean, ay + 10), 5)
        else:
            # Normal arm
            arm_bob = math.sin(self.state_frame * 0.2) * 3 if self.state == IDLE else 0
            fx = cx + dir * 18 + lean
            fy = ay + 3 + int(arm_bob)
            pygame.draw.line(surface, color, (cx + dir * 10 + lean, ay), (fx, fy), 5)

    def get_rect(self):
        """Return collision rect."""
        return pygame.Rect(self.x - FIGHTER_W // 2, self.y - FIGHTER_H, FIGHTER_W, FIGHTER_H)
