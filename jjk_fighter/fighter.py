import pygame
import math
import random
from particles import ParticleSystem
from effects import create_effect
from characters import CHARACTERS

GRAVITY = 0.6
GROUND_Y = 500
FIGHTER_WIDTH = 50
FIGHTER_HEIGHT = 80
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

IDLE = 'idle'
WALK = 'walk'
JUMP = 'jump'
ATTACK = 'attack'
BLOCK = 'block'
HIT = 'hit'
KNOCKDOWN = 'knockdown'
ULTIMATE = 'ultimate'

# Key bindings
P1_KEYS = {
    'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w, 'block': pygame.K_s,
    'atk1': pygame.K_1, 'atk2': pygame.K_2, 'atk3': pygame.K_3,
    'mod': pygame.K_q, 'super': pygame.K_e
}
P2_KEYS = {
    'left': pygame.K_j, 'right': pygame.K_l, 'jump': pygame.K_i, 'block': pygame.K_k,
    'atk1': pygame.K_8, 'atk2': pygame.K_9, 'atk3': pygame.K_0,
    'mod': pygame.K_u, 'super': pygame.K_o
}

# Domain effects
DOMAIN_EFFECTS = {
    'yuji':    {'name': 'Black Flash Barrage', 'type': 'combo', 'hits': 5, 'dmg_per_hit': 25, 'buff_after': {'damage_boost': 1.5, 'duration': 300}},
    'gojo':    {'name': 'Unlimited Void', 'type': 'stun_domain', 'stun_duration': 180, 'ce_drain': 50, 'dmg': 30, 'duration': 240, 'bg_color': (20, 60, 180)},
    'sukuna':  {'name': 'Malevolent Shrine', 'type': 'zone_damage', 'dps': 3, 'duration': 300, 'dmg_on_start': 50, 'bg_color': (120, 10, 10)},
    'megumi':  {'name': 'Chimera Shadow Garden', 'type': 'summon_zone', 'dmg_per_tick': 4, 'duration': 240, 'dmg_on_start': 40, 'bg_color': (30, 10, 60)},
    'nobara':  {'name': 'Hairpin: Star', 'type': 'explosion', 'dmg': 100, 'stun': 60},
    'nanami':  {'name': 'Ratio: Collapse', 'type': 'single_strike', 'dmg': 120, 'guaranteed_crit': True},
    'inumaki': {'name': '"DIE"', 'type': 'self_sacrifice', 'dmg': 150, 'self_dmg': 100},
    'todo':    {'name': 'Solo Stance', 'type': 'self_buff', 'damage_boost': 2.0, 'speed_boost': 1.5, 'duration': 480},
    'mahito':  {'name': 'True Form', 'type': 'transform', 'damage_boost': 1.5, 'defense_boost': 0.7, 'duration': 480, 'dmg_on_start': 40},
    'jogo':    {'name': 'Coffin of the Iron Mountain', 'type': 'zone_damage', 'dps': 4, 'duration': 300, 'dmg_on_start': 60, 'bg_color': (100, 30, 0)},
    'hanami':  {'name': 'Shining Sea of Trees', 'type': 'zone_heal', 'hps': 1, 'dps': 2, 'duration': 300, 'bg_color': (20, 60, 15)},
    'choso':   {'name': 'Blood Meteor', 'type': 'projectile_nuke', 'dmg': 130, 'stun': 45},
}

ATTACK_STYLES = {
    'yuji':    {'light': 'punch', 'heavy': 'kick', 'trail': (255, 150, 30)},
    'gojo':    {'light': 'palm', 'heavy': 'push', 'trail': (30, 100, 255)},
    'sukuna':  {'light': 'slash', 'heavy': 'slash', 'trail': (255, 50, 50)},
    'megumi':  {'light': 'stab', 'heavy': 'shadow', 'trail': (180, 50, 255)},
    'nobara':  {'light': 'hammer', 'heavy': 'hammer_big', 'trail': (255, 100, 150)},
    'nanami':  {'light': 'blade', 'heavy': 'blade_heavy', 'trail': (200, 180, 100)},
    'inumaki': {'light': 'headbutt', 'heavy': 'shout', 'trail': (100, 200, 150)},
    'todo':    {'light': 'punch', 'heavy': 'slam', 'trail': (180, 180, 180)},
    'mahito':  {'light': 'extend', 'heavy': 'reshape', 'trail': (150, 150, 200)},
    'jogo':    {'light': 'ember', 'heavy': 'fireball', 'trail': (255, 80, 20)},
    'hanami':  {'light': 'root', 'heavy': 'vine', 'trail': (80, 160, 80)},
    'choso':   {'light': 'blood_cut', 'heavy': 'blood_spray', 'trail': (180, 30, 30)},
}


class Hitbox:
    def __init__(self, x, y, w, h, damage, kb_x, kb_y):
        self.rect = pygame.Rect(x, y, w, h)
        self.damage = damage
        self.kb_x = kb_x
        self.kb_y = kb_y
        self.has_hit = False


class Fighter:
    def __init__(self, x, y, name, color, facing_right=True, key_bindings=None):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.name = name
        self.color = color
        self.facing_right = facing_right
        self.keys = key_bindings or P1_KEYS
        self.on_ground = True
        self.state = IDLE
        self.state_frame = 0
        self.health = 100
        self.max_health = 100
        self.cursed_energy = 50
        self.max_cursed_energy = 100
        self.combo_count = 0
        self.combo_timer = 0
        self.hitstun = 0
        self.blockstun = 0
        self.invincible = 0
        self.hitboxes = []
        self.particles = ParticleSystem()
        self.active_effects = []
        self.domain_trigger = None
        self.attack_startup = 0
        self.attack_active = 0
        self.attack_recovery = 0
        self.current_attack = None
        self.current_move_name = None
        self._pending_hitbox = None
        self.buffs = {}
        self.domain_active = None
        self.stun_timer = 0
        self.transformed = False
        self.anim_frame = 0
        self.squash = 1.0
        self.stretch = 1.0
        # Load moves from characters.py
        char_info = CHARACTERS.get(name, CHARACTERS['yuji'])
        self.char_data = {
            'speed': char_info.get('speed', 5),
            'jump_power': char_info.get('jump_power', -12),
            'special_cost': 25,
            'ultimate_cost': 100,
        }
        self.all_moves = char_info.get('moves', {})
        self.all_supers = char_info.get('supers', {})
        # Map moves to input combos
        self.move_map = self._build_move_map()
        self.atk_style = ATTACK_STYLES.get(name, ATTACK_STYLES['yuji'])

    def _build_move_map(self):
        """Map all moves to keyboard input combos"""
        m = {}
        lights = []
        heavies = []
        specials = []
        for mname, mdata in self.all_moves.items():
            t = mdata.get('type', '')
            if t == 'light':
                lights.append((mname, mdata))
            elif t == 'heavy':
                heavies.append((mname, mdata))
            elif t in ('special', 'trap', 'buff', 'charge', 'heal'):
                specials.append((mname, mdata))
        # Map lights: atk1 = first, mod+atk1 = second, atk3 = third
        if len(lights) > 0: m['atk1'] = lights[0]
        if len(lights) > 1: m['mod_atk1'] = lights[1]
        if len(lights) > 2: m['atk3'] = lights[2]
        # Map heavies: atk2 = first, mod+atk2 = second
        if len(heavies) > 0: m['atk2'] = heavies[0]
        if len(heavies) > 1: m['mod_atk2'] = heavies[1]
        # Map specials: mod+atk3 = first, super = second (or more)
        if len(specials) > 0: m['mod_atk3'] = specials[0]
        if len(specials) > 1: m['mod_super'] = specials[1]
        if len(specials) > 2: m['atk3_special'] = specials[2]
        # Map supers
        for sname, sdata in self.all_supers.items():
            m['super'] = (sname, sdata)
            break
        return m

    def handle_input(self, keys, opponent):
        if self.hitstun > 0 or self.blockstun > 0 or self.stun_timer > 0:
            return
        self.facing_right = self.x < opponent.x
        if self.state in (ATTACK, ULTIMATE):
            return

        k = self.keys
        speed = self.char_data['speed']
        if self.buffs.get('speed_boost', 0) > 0:
            speed *= self.buffs['speed_boost']

        moving = False
        if keys[k['left']]:
            self.vx = -speed
            moving = True
            if self.on_ground: self.state = WALK
        elif keys[k['right']]:
            self.vx = speed
            moving = True
            if self.on_ground: self.state = WALK

        if not moving:
            self.vx = 0
            if self.on_ground and self.state not in (ATTACK, BLOCK, ULTIMATE):
                self.state = IDLE

        if keys[k['jump']] and self.on_ground:
            self.vy = self.char_data['jump_power']
            self.on_ground = False
            self.state = JUMP
            self.squash = 0.7
            self.stretch = 1.3

        if keys[k['block']] and self.on_ground and not moving:
            self.state = BLOCK
            self.vx = 0
            return

        # Check for attacks - check mod+button combos FIRST
        mod = keys[k['mod']]
        super_key = keys[k['super']]

        if mod and super_key:
            # mod+super = second special
            self._try_move('mod_super')
        elif mod and keys[k['atk1']]:
            self._try_move('mod_atk1')
        elif mod and keys[k['atk2']]:
            self._try_move('mod_atk2')
        elif mod and keys[k['atk3']]:
            self._try_move('mod_atk3')
        elif super_key:
            self._try_move('super')
        elif keys[k['atk3']]:
            self._try_move('atk3_special') if 'atk3_special' in self.move_map else self._try_move('atk3')
        elif keys[k['atk2']]:
            self._try_move('atk2')
        elif keys[k['atk1']]:
            self._try_move('atk1')

    def _try_move(self, input_key):
        """Execute a move from the move map"""
        if input_key == 'super':
            entry = self.move_map.get('super')
            if entry and self.cursed_energy >= entry[1].get('ce_cost', 100):
                self._start_ultimate()
            return
        entry = self.move_map.get(input_key)
        if not entry:
            return
        mname, mdata = entry
        cost = mdata.get('ce_cost', 0)
        if cost > 0 and self.cursed_energy < cost:
            return
        self._execute_move(mname, mdata)

    def _execute_move(self, mname, mdata):
        """Execute a specific move from characters.py"""
        self.cursed_energy -= mdata.get('ce_cost', 0)
        dmg = mdata.get('damage', 25)
        if self.buffs.get('damage_boost', 0) > 0:
            dmg = int(dmg * self.buffs['damage_boost'])
        startup = mdata.get('startup', 5)
        active = mdata.get('active', 4)
        recovery = mdata.get('recovery', 10)
        kb_x = mdata.get('kb_x', 5)
        kb_y = mdata.get('kb_y', -3)
        w = int(mdata.get('range', 50))
        h = 35

        mtype = mdata.get('type', 'light')
        if mtype in ('special', 'trap', 'buff', 'charge', 'heal'):
            self.state = ULTIMATE if mdata.get('ce_cost', 0) >= 50 else ATTACK
        elif mtype == 'heavy':
            self.state = ATTACK
        else:
            self.state = ATTACK

        self.attack_startup = startup
        self.attack_active = active
        self.attack_recovery = recovery
        self.current_attack = mtype
        self.current_move_name = mname
        self.state_frame = 0
        self.hitboxes = []
        d = 1 if self.facing_right else -1
        self._pending_hitbox = (dmg, kb_x, kb_y, w, h)

        if mtype == 'heavy':
            self.vx = d * 6

        # Spawn VFX
        vfx = mdata.get('vfx', '')
        if vfx:
            effect = create_effect(vfx, self.x + d*60, self.y-30, self.facing_right)
            if effect:
                self.active_effects.append(effect)

        # Apply non-damage effects
        effect_name = mdata.get('effect', '')
        if effect_name == 'heal' or mname == 'rev_cursed':
            self.health = min(self.max_health, self.health + mdata.get('heal', 80))
        elif effect_name == 'speed_boost' or mdata.get('buff') == 'speed_boost':
            self.buffs['speed_boost'] = 1.5
        elif effect_name == 'damage_boost' or mdata.get('buff') == 'damage_boost':
            self.buffs['damage_boost'] = 1.3
        elif effect_name == 'defense_boost' or mdata.get('buff') == 'defense_boost':
            self.buffs['defense_boost'] = 0.5
        elif mdata.get('invincible'):
            self.invincible = max(self.invincible, active + 10)

    def _start_ultimate(self):
        domain = DOMAIN_EFFECTS.get(self.name)
        if not domain:
            return
        self.state = ULTIMATE
        self.state_frame = 0
        self.attack_startup = 15
        self.attack_active = 10
        self.attack_recovery = 25
        self.cursed_energy -= 100
        self.hitboxes = []
        self.current_attack = 'ultimate'
        self.current_move_name = domain.get('name', 'Super')
        self.invincible = 30
        self.domain_trigger = self.name
        dmg = domain.get('dmg_on_start', domain.get('dmg', 80))
        if self.buffs.get('damage_boost', 0) > 0:
            dmg = int(dmg * self.buffs['damage_boost'])
        self._pending_hitbox = (dmg, 15, -10, 80, 60)
        self.domain_active = {'effect': domain, 'timer': domain.get('duration', 120)}
        self.particles.emit(self.x, self.y-40, 30, self.color, (3,8), (4,10), (20,40), 360, 0, gravity=0)

    def apply_domain_effect(self, opponent):
        if not self.domain_active:
            return
        effect = self.domain_active['effect']
        etype = effect['type']
        timer = self.domain_active['timer']
        if timer <= 0:
            self.domain_active = None
            self.transformed = False
            self.buffs.pop('damage_boost', None)
            self.buffs.pop('speed_boost', None)
            self.buffs.pop('defense_boost', None)
            return
        self.domain_active['timer'] = timer - 1
        if etype == 'stun_domain':
            if timer == effect.get('duration', 240) - 1:
                opponent.stun_timer = effect['stun_duration']
                opponent.cursed_energy = max(0, opponent.cursed_energy - effect.get('ce_drain', 0))
                opponent.take_damage(effect.get('dmg', 30), 0, 0)
            if timer > 30:
                opponent.stun_timer = max(opponent.stun_timer, 5)
        elif etype == 'zone_damage':
            if timer % 20 == 0 and abs(self.x - opponent.x) < 300:
                opponent.take_damage(effect['dps'] * 10, 0, 0)
        elif etype == 'summon_zone':
            if timer % 30 == 0 and abs(self.x - opponent.x) < 350:
                opponent.take_damage(effect['dmg_per_tick'] * 8, 3, -2)
        elif etype == 'zone_heal':
            if timer % 30 == 0:
                self.health = min(self.max_health, self.health + effect['hps'] * 10)
                if abs(self.x - opponent.x) < 250:
                    opponent.take_damage(effect['dps'] * 8, 0, 0)
        elif etype == 'self_buff':
            if timer == effect.get('duration', 480) - 1:
                self.buffs['damage_boost'] = effect['damage_boost']
                self.buffs['speed_boost'] = effect['speed_boost']
            self.buffs['damage_boost'] = effect['damage_boost']
            self.buffs['speed_boost'] = effect['speed_boost']
        elif etype == 'transform':
            if timer == effect.get('duration', 480) - 1:
                self.transformed = True
            self.buffs['damage_boost'] = effect['damage_boost']

    def apply_combo_hit(self, opponent):
        domain = DOMAIN_EFFECTS.get(self.name)
        if not domain or domain['type'] != 'combo' or not opponent:
            return
        if self.state == ULTIMATE and self.state_frame > self.attack_startup:
            frame = self.state_frame - self.attack_startup
            if frame % 8 == 0 and frame < domain['hits'] * 8:
                hit_num = frame // 8
                d = 1 if self.facing_right else -1
                opponent.take_damage(domain['dmg_per_hit'], d*8, -5)
                self.particles.emit(opponent.x, opponent.y-40, 15, (255,200,50), (4,8), (3,6), (8,15), 360, 0, gravity=0)
                if hit_num == domain['hits'] - 1:
                    self.buffs['damage_boost'] = domain['buff_after']['damage_boost']

    def take_damage(self, damage, kb_x, kb_y, blocked=False):
        if self.invincible > 0:
            return False
        if self.buffs.get('defense_boost', 0) > 0:
            damage = int(damage * self.buffs['defense_boost'])
        if blocked:
            self.health -= max(1, damage * 0.15)
            self.blockstun = 8
            self.vx = kb_x * 0.3
            self.particles.emit(self.x, self.y-40, 6, (100,100,255), (2,4), (2,4), (5,12), 120, 180 if kb_x > 0 else 0)
            return False
        self.health -= damage
        self.hitstun = 12 + int(damage * 0.4)
        self.vx = kb_x
        self.vy = kb_y
        self.state = HIT
        self.state_frame = 0
        self.on_ground = False
        self.hitboxes = []
        self.particles.emit(self.x, self.y-40, 12, (255,100,100), (3,7), (3,6), (10,20), 180, 180 if kb_x > 0 else 0)
        if self.health <= 0:
            self.health = 0
            self.state = KNOCKDOWN
        return True

    def update(self, screen_width):
        self.state_frame += 1
        self.anim_frame += 1
        self.squash += (1.0 - self.squash) * 0.15
        self.stretch += (1.0 - self.stretch) * 0.15
        if not self.on_ground:
            self.vy += GRAVITY
            if self.vy > 2:
                self.stretch = 1.15
                self.squash = 0.9
        self.x += self.vx
        self.y += self.vy
        if self.y >= GROUND_Y:
            if self.vy > 5:
                self.squash = 1.3
                self.stretch = 0.7
            self.y = GROUND_Y
            self.vy = 0
            self.on_ground = True
            if self.state == JUMP: self.state = IDLE
            if self.state == HIT: self.state = IDLE; self.hitstun = 0
        self.x = max(FIGHTER_WIDTH//2, min(screen_width-FIGHTER_WIDTH//2, self.x))
        if self.hitstun > 0: self.hitstun -= 1
        if self.blockstun > 0: self.blockstun -= 1
        if self.invincible > 0: self.invincible -= 1
        if self.stun_timer > 0: self.stun_timer -= 1
        if self.combo_timer > 0: self.combo_timer -= 1
        else: self.combo_count = 0

        if self.domain_active:
            if self.domain_active['timer'] > 0:
                self.domain_active['timer'] -= 1
                if self.domain_active['timer'] % 5 == 0:
                    self.particles.emit(self.x+random.randint(-100,100), self.y-random.randint(20,80), 3, self.color, (1,3), (2,5), (15,30), 360, 0, gravity=-0.05)
            else:
                self.domain_active = None
                self.transformed = False
                for b in ('damage_boost','speed_boost','defense_boost'): self.buffs.pop(b, None)

        if self.state in (ATTACK, ULTIMATE):
            ts = self.attack_startup
            ta = ts + self.attack_active
            tr = ta + self.attack_recovery
            if self.state_frame <= ts:
                if self.state_frame % 2 == 0:
                    d = 1 if self.facing_right else -1
                    self.particles.emit(self.x+d*25, self.y-40, 2, self.color, (1,3), (2,4), (5,10), 60, 0 if self.facing_right else 180)
            elif self.state_frame <= ta:
                if not self.hitboxes and self._pending_hitbox:
                    d = 1 if self.facing_right else -1
                    dmg, kb_x, kb_y, w, h = self._pending_hitbox
                    self.hitboxes = [Hitbox(self.x+d*25, self.y-45, w, h, dmg, d*kb_x, kb_y)]
                if self.hitboxes:
                    d = 1 if self.facing_right else -1
                    self.hitboxes[0].rect.centerx = int(self.x+d*25)
                    self.hitboxes[0].rect.centery = int(self.y-45)
            elif self.state_frame <= tr:
                self.hitboxes = []
            else:
                self.state = IDLE
                self.hitboxes = []
                self.current_attack = None
                self.current_move_name = None

        self.cursed_energy = min(self.max_cursed_energy, self.cursed_energy + 0.3)
        self.active_effects = [e for e in self.active_effects if e.alive]
        for eff in self.active_effects: eff.update()
        self.particles.update()

    def get_hitboxes(self):
        return [h for h in self.hitboxes if not h.has_hit]

    def get_hurtbox(self):
        return pygame.Rect(self.x-FIGHTER_WIDTH//2, self.y-FIGHTER_HEIGHT, FIGHTER_WIDTH, FIGHTER_HEIGHT)

    def register_hit(self, hitbox, opponent):
        hitbox.has_hit = True
        self.combo_count += 1
        self.combo_timer = 60
        self.cursed_energy = min(self.max_cursed_energy, self.cursed_energy + 10)
        return opponent.take_damage(hitbox.damage, hitbox.kb_x, hitbox.kb_y)

    # ======================== DRAWING ========================
    def draw(self, surface):
        for eff in self.active_effects: eff.draw(surface)
        color = self.color
        if self.invincible > 0 and self.invincible % 4 < 2: color = WHITE
        if self.transformed: color = (min(255,color[0]+50), min(255,color[1]+30), min(255,color[2]+50))
        cx, cy = int(self.x), int(self.y)
        d = 1 if self.facing_right else -1
        bw = int(FIGHTER_WIDTH * self.squash)
        bh = int(FIGHTER_HEIGHT * self.stretch)
        lean = 0
        if self.state == ATTACK and self.state_frame > self.attack_startup: lean = d*15
        elif self.state == ULTIMATE and self.state_frame > self.attack_startup: lean = d*22
        bob = math.sin(self.anim_frame*0.08)*3 if self.state == IDLE and self.on_ground else 0
        hurt = self.state == HIT and self.state_frame < 4
        bc = (255,255,255) if hurt else color

        # Legs
        if self.on_ground and self.state == WALK:
            wc = math.sin(self.anim_frame*0.35)
            lax = cx-10+lean+int(wc*10); lay = cy-int(abs(wc)*5)
            rax = cx+10+lean-int(wc*10); ray = cy+int(abs(wc)*5)
            pygame.draw.line(surface, bc, (cx-8+lean,cy-18), (lax,lay), 5)
            pygame.draw.circle(surface, bc, (lax,lay), 4)
            pygame.draw.line(surface, bc, (cx+8+lean,cy-18), (rax,ray), 5)
            pygame.draw.circle(surface, bc, (rax,ray), 4)
        elif self.state == JUMP:
            pygame.draw.line(surface, bc, (cx-10,cy-18), (cx-15,cy-5), 5)
            pygame.draw.line(surface, bc, (cx+10,cy-18), (cx+5,cy-5), 5)
        elif self.state == BLOCK:
            pygame.draw.line(surface, bc, (cx-8,cy-18), (cx-16,cy), 5)
            pygame.draw.line(surface, bc, (cx+4,cy-18), (cx+2,cy), 5)
        else:
            pygame.draw.line(surface, bc, (cx-8+lean,cy-18), (cx-10,cy), 5)
            pygame.draw.line(surface, bc, (cx+8+lean,cy-18), (cx+10,cy), 5)

        # Body
        bt = cy-bh+int(bob); bb = cy-18
        br = pygame.Rect(cx-bw//2+lean, bt, bw, bb-bt)
        pygame.draw.rect(surface, bc, br, border_radius=8)
        pygame.draw.line(surface, self._dk(color,40), (cx-bw//3+lean,bb-5), (cx+bw//3+lean,bb-5), 2)
        self._draw_detail(surface, cx+lean, bt, bb, d, bob, bw)

        # Arms
        ay = bt+22
        if self.state in (ATTACK, ULTIMATE) and self.state_frame > self.attack_startup:
            self._draw_attack_arm(surface, cx, ay, lean, d, bc)
        elif self.state == BLOCK:
            pygame.draw.line(surface, bc, (cx-16+lean,ay), (cx+5+lean,ay-18), 5)
            pygame.draw.line(surface, bc, (cx+16+lean,ay), (cx-5+lean,ay-18), 5)
        else:
            sw = math.sin(self.anim_frame*0.06)*4
            pygame.draw.line(surface, bc, (cx-20+lean,ay), (cx-26+lean,ay+28+int(sw)), 5)
            pygame.draw.line(surface, bc, (cx+20+lean,ay), (cx+26+lean,ay+28-int(sw)), 5)

        # Head
        hr = 17; hy = bt-hr+int(bob*0.5)
        pygame.draw.line(surface, bc, (cx+lean,bt+2), (cx+lean,hy+hr-3), 5)
        pygame.draw.circle(surface, bc, (cx+lean,hy), hr)
        self._draw_face(surface, cx+lean, hy, d, hurt)
        pygame.draw.circle(surface, (255,150,150) if hurt else WHITE, (cx+lean,hy), hr, 2)
        pygame.draw.rect(surface, (255,150,150) if hurt else WHITE, br, 1, border_radius=8)

        if self.state == BLOCK:
            sh = pygame.Surface((65,85), pygame.SRCALPHA)
            pygame.draw.ellipse(sh, (*self.color,60), (0,0,65,85))
            pygame.draw.ellipse(sh, (*self.color,160), (0,0,65,85), 3)
            surface.blit(sh, (cx-32+lean, bt-8))
        if self.domain_active:
            ar = 80+int(math.sin(self.anim_frame*0.1)*10)
            aura = pygame.Surface((ar*2,ar*2), pygame.SRCALPHA)
            pygame.draw.circle(aura, (*self.color,25), (ar,ar), ar)
            pygame.draw.circle(aura, (*self.color,50), (ar,ar), ar-15)
            surface.blit(aura, (cx-ar, cy-60-ar))
        # Current move name popup
        if self.current_move_name and self.state_frame < 20 and self.state in (ATTACK, ULTIMATE):
            mf = pygame.font.SysFont('arial', 14, bold=True)
            mt = mf.render(self.current_move_name.replace('_',' ').title(), True, (255,255,200))
            surface.blit(mt, (cx-mt.get_width()//2+lean, bt-30))
        self.particles.draw(surface)

    def _draw_attack_arm(self, surface, cx, ay, lean, d, bc):
        trail = self.atk_style.get('trail', self.color)
        atype = self.atk_style.get('light', 'punch')
        if self.current_attack == 'heavy': atype = self.atk_style.get('heavy', 'kick')
        pl = 32 if self.current_attack == 'light' else 45
        if self.current_attack == 'ultimate': pl = 50

        if atype in ('punch','palm','hammer','blade','blood_cut'):
            fx = cx+d*(20+pl)+lean; fy = ay-5
            pygame.draw.line(surface, bc, (cx+d*20+lean,ay+3), (fx,fy), 5)
            pygame.draw.circle(surface, bc, (fx,fy), 6)
            for i in range(3):
                self.particles.emit(cx+d*(15+i*12)+lean, fy, 1, trail, (1,2), (2,3), (3,6), 60, 0 if d>0 else 180)
        elif atype in ('kick','slam','vine'):
            fx = cx+d*(15+pl); fy = ay+30
            pygame.draw.line(surface, bc, (cx+d*8,ay+20), (fx,fy), 5)
            pygame.draw.circle(surface, bc, (fx,fy), 5)
            self.particles.emit(fx, fy, 2, trail, (2,4), (2,4), (4,8), 60, 0 if d>0 else 180)
        elif atype in ('slash','shadow','blade_heavy'):
            fx = cx+d*(20+pl)+lean; fy = ay-15
            pygame.draw.line(surface, bc, (cx+d*20+lean,ay-20), (fx,fy+20), 4)
            pygame.draw.line(surface, bc, (fx,fy), (fx,fy+20), 4)
            for i in range(5):
                t = i/4
                self.particles.emit(cx+d*20+lean+d*int(t*pl), ay-20+int(t*30), 1, trail, (1,2), (2,4), (3,8), 60, 0)
        elif atype in ('stab',):
            fx = cx+d*(25+pl)+lean; fy = ay-2
            pygame.draw.line(surface, bc, (cx+d*20+lean,ay), (fx,fy), 4)
            pygame.draw.polygon(surface, trail, [(fx,fy-5),(fx+d*8,fy),(fx,fy+5)])
        elif atype in ('extend','reshape'):
            fx = cx+d*(20+pl*2)+lean; fy = ay-5
            pygame.draw.line(surface, bc, (cx+d*20+lean,ay), (fx,fy), 3)
            pygame.draw.circle(surface, trail, (fx,fy), 8)
            pygame.draw.circle(surface, bc, (fx,fy), 8, 2)
        elif atype in ('ember','fireball'):
            fx = cx+d*(25+pl)+lean; fy = ay-10
            pygame.draw.line(surface, bc, (cx+d*20+lean,ay), (fx,fy), 5)
            for i in range(4):
                self.particles.emit(fx+d*i*5, fy+random.randint(-5,5), 1, (255,150,30), (2,4), (3,5), (5,12), 60, 0 if d>0 else 180)
        elif atype in ('shout','blood_spray'):
            fx = cx+d*(15+pl)+lean
            for i in range(3):
                self.particles.emit(fx, ay-10+i*10, 2, trail, (3,6), (3,5), (5,12), 45, 0 if d>0 else 180)
        else:
            fx = cx+d*(20+pl)+lean; fy = ay-5
            pygame.draw.line(surface, bc, (cx+d*20+lean,ay), (fx,fy), 5)
            pygame.draw.circle(surface, bc, (fx,fy), 5)

    def _dk(self, c, n): return (max(0,c[0]-n), max(0,c[1]-n), max(0,c[2]-n))

    def _draw_detail(self, surface, cx, top, bot, d, bob, bw):
        mid = (top+bot)//2
        if self.name == 'nanami':
            pygame.draw.line(surface, (60,50,30), (cx,top+8),(cx,bot-3), 3)
            pygame.draw.line(surface, (50,45,25), (cx-8,top+8),(cx+8,top+8), 2)
            bx = cx-d*24
            pygame.draw.polygon(surface, (190,190,200), [(bx,top+2),(bx-5,top+18),(bx+5,top+18)])
            pygame.draw.line(surface, (120,100,60), (bx,top+18),(bx,bot-15), 3)
        elif self.name == 'gojo':
            pygame.draw.rect(surface, (15,15,15), (cx-20,top+2-int(bob),40,10))
            for i in range(-3,4):
                hx = cx+i*5; h = random.randint(10,18) if i%2==0 else random.randint(6,12)
                pygame.draw.line(surface, (220,220,235), (hx,top-2+int(bob)), (hx+i*3,top-h+int(bob)), 3)
        elif self.name == 'sukuna':
            for s in [-1,1]:
                sx = cx+s*12
                pygame.draw.line(surface, (180,25,25), (sx,top+6),(sx+s*8,top+14), 2)
                pygame.draw.line(surface, (180,25,25), (sx,top+6),(sx+s*6,top), 2)
                pygame.draw.line(surface, (180,25,25), (sx,top+6),(sx+s*10,top+8), 2)
        elif self.name == 'megumi':
            aura = pygame.Surface((55,bot-top+10), pygame.SRCALPHA)
            for i in range(3):
                pygame.draw.rect(aura, (60,20,120,max(0,20-i*7)), (i*3,i*3,55-i*6,bot-top+10-i*6), border_radius=8)
            surface.blit(aura, (cx-27,top-5))
        elif self.name == 'nobara':
            hx = cx+d*28
            pygame.draw.line(surface, (140,100,60), (hx,mid-5),(hx+d*18,mid-20), 3)
            pygame.draw.rect(surface, (90,90,90), (hx+d*14,mid-28,12,14))
        elif self.name == 'todo':
            pygame.draw.rect(surface, self.color, (cx-28,top,56,bot-top+6), border_radius=6)
            pygame.draw.rect(surface, WHITE, (cx-28,top,56,bot-top+6), 1, border_radius=6)
            pygame.draw.line(surface, (180,160,140), (cx-8,top+12),(cx+8,top+12), 2)
        elif self.name == 'inumaki':
            pygame.draw.line(surface, (50,50,50), (cx-18,top+5),(cx-22,top-5), 4)
            pygame.draw.line(surface, (50,50,50), (cx+18,top+5),(cx+22,top-5), 4)
        elif self.name == 'mahito':
            pts = [(cx-12,top+8),(cx+8,bot-12),(cx+3,top+15),(cx-7,bot-5)]
            for i in range(0,len(pts)-1,2): pygame.draw.line(surface, (90,90,110), pts[i],pts[i+1], 1)
        elif self.name == 'jogo':
            pts = [(cx-14,top-2),(cx-6,top-22),(cx,top-28),(cx+6,top-22),(cx+14,top-2)]
            pygame.draw.polygon(surface, (180,50,15), pts)
            glow = pygame.Surface((20,20), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255,120,20,100), (10,10), 8+int(math.sin(self.anim_frame*0.15)*3))
            surface.blit(glow, (cx-10,top-35))
        elif self.name == 'hanami':
            for s in [-1,1]:
                ax = cx+s*14
                pygame.draw.line(surface, (50,100,30), (ax,top),(ax+s*12,top-22), 3)
                pygame.draw.line(surface, (50,100,30), (ax+s*12,top-22),(ax+s*8,top-32), 2)
        elif self.name == 'choso':
            for s in [-1,1]:
                vx = cx+s*20
                pygame.draw.circle(surface, (160,15,15), (vx,top+6), 4)
        elif self.name == 'yuji':
            pygame.draw.arc(surface, (180,100,15), (cx-22,top-8+int(bob),44,28), 0.2, 2.94, 2)

    def _draw_face(self, surface, cx, hy, d, hurt):
        ey = hy-3; my = ey+8
        if hurt:
            for sx in [-1,1]:
                pygame.draw.line(surface, (50,50,50), (cx+sx*7,ey),(cx+sx*3,ey+2), 2)
                pygame.draw.line(surface, (50,50,50), (cx+sx*7,ey+2),(cx+sx*3,ey), 2)
            pygame.draw.arc(surface, (50,50,50), (cx-4,my,8,5), 3.14, 6.28, 1)
            return
        if self.name == 'gojo': return
        elif self.name == 'sukuna':
            pygame.draw.circle(surface, (255,220,50), (cx-6,ey-5), 3)
            pygame.draw.circle(surface, (255,220,50), (cx+6,ey-5), 3)
            pygame.draw.circle(surface, (255,200,30), (cx-6+d,ey+2), 3)
            pygame.draw.circle(surface, (255,200,30), (cx+6+d,ey+2), 3)
            pygame.draw.arc(surface, (150,20,20), (cx-5,my-2,10,6), 0, 3.14, 2)
        elif self.name == 'mahito':
            pygame.draw.circle(surface, (80,80,180), (cx-6+d,ey), 3)
            pygame.draw.circle(surface, (180,80,80), (cx+6+d,ey), 3)
            for i in range(4): pygame.draw.line(surface, (100,100,120), (cx-4+i*3,my-2),(cx-4+i*3,my+2), 1)
        elif self.name == 'jogo':
            pygame.draw.circle(surface, (255,40,0), (cx-6+d,ey), 3)
            pygame.draw.circle(surface, (255,40,0), (cx+6+d,ey), 3)
            pygame.draw.line(surface, (180,30,0), (cx-9,ey-6),(cx-3,ey-4), 2)
            pygame.draw.line(surface, (180,30,0), (cx+3,ey-4),(cx+9,ey-6), 2)
        elif self.name == 'hanami':
            pygame.draw.circle(surface, (200,200,40), (cx+d*7,ey), 5)
            pygame.draw.circle(surface, (60,30,10), (cx+d*7,ey), 2)
        elif self.name == 'inumaki':
            pygame.draw.circle(surface, WHITE, (cx-6+d,ey), 3)
            pygame.draw.circle(surface, WHITE, (cx+6+d,ey), 3)
            pygame.draw.rect(surface, (35,35,35), (cx-9,my-3,18,10), border_radius=3)
            sf = pygame.font.SysFont('arial', 7)
            st = sf.render("FISH", True, (180,180,180))
            surface.blit(st, (cx-st.get_width()//2, my-1))
        elif self.name == 'nanami':
            pygame.draw.circle(surface, WHITE, (cx-5+d,ey), 3)
            pygame.draw.circle(surface, WHITE, (cx+5+d,ey), 3)
            pygame.draw.rect(surface, (100,100,100), (cx-10,ey-5,9,7), 1)
            pygame.draw.rect(surface, (100,100,100), (cx+1,ey-5,9,7), 1)
            pygame.draw.line(surface, (100,100,100), (cx-1,ey-2),(cx+1,ey-2), 1)
        elif self.name == 'todo':
            pygame.draw.circle(surface, WHITE, (cx-6+d,ey), 4)
            pygame.draw.circle(surface, WHITE, (cx+6+d,ey), 4)
            pygame.draw.arc(surface, (80,40,40), (cx-6,my-2,12,8), 0, 3.14, 2)
        else:
            pygame.draw.circle(surface, WHITE, (cx-6+d,ey), 3)
            pygame.draw.circle(surface, WHITE, (cx+6+d,ey), 3)
            pygame.draw.circle(surface, (30,30,40), (cx-5+d*2,ey), 1)
            pygame.draw.circle(surface, (30,30,40), (cx+7+d*2,ey), 1)
