import pygame
import random
import math

# Combat constants
HITSTUN_DECAY = 0.85
COMBO_DAMAGE_DECAY = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
BLACK_FLASH_BASE_CHANCE = 0.05
PARRY_WINDOW = 4  # frames
BURST_COST = 50

# Fighter states
ST_IDLE = "idle"
ST_WALK = "walk"
ST_CROUCH = "crouch"
ST_JUMP = "jump"
ST_ATTACK = "attack"
ST_BLOCK = "block"
ST_HIT = "hit"
ST_KNOCKDOWN = "knockdown"
ST_WAKEUP = "wakeup"
ST_SPECIAL = "special"
ST_SUPER = "super"
ST_DODGE = "dodge"
ST_BURST = "burst"
ST_BUFF = "buff"
ST_STUN = "stun"

class Hitbox:
    def __init__(self, x, y, w, h, damage, kb_x, kb_y, hitstun, owner, move_data=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.damage = damage
        self.kb_x = kb_x
        self.kb_y = kb_y
        self.hitstun = hitstun
        self.owner = owner
        self.move_data = move_data or {}
        self.has_hit = False
        self.frame_count = 0

    def update(self):
        self.frame_count += 1

    def active(self):
        active_frames = self.move_data.get("active", 5)
        return self.frame_count <= active_frames and not self.has_hit


class ComboTracker:
    def __init__(self):
        self.count = 0
        self.damage = 0
        self.timer = 0
        self.max_timer = 45  # frames before combo drops
        self.history = []

    def add_hit(self, damage, move_name):
        self.count += 1
        decay = COMBO_DAMAGE_DECAY[min(self.count - 1, len(COMBO_DAMAGE_DECAY) - 1)]
        scaled_damage = int(damage * decay)
        self.damage += scaled_damage
        self.timer = self.max_timer
        self.history.append(move_name)
        return scaled_damage

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        if self.timer <= 0 and self.count > 0:
            self.reset()

    def reset(self):
        self.count = 0
        self.damage = 0
        self.history = []

    def is_combo(self):
        return self.count > 1


class CombatSystem:
    def __init__(self):
        self.p1_combo = ComboTracker()
        self.p2_combo = ComboTracker()
        self.screen_shake = 0
        self.hit_freeze = 0
        self.slow_motion = 0
        self.effects_queue = []

    def check_hit(self, attacker, defender, hitbox):
        """Check if a hitbox connects and apply damage"""
        if hitbox.has_hit:
            return False

        hurtbox = defender.get_hurtbox()
        if not hitbox.active():
            return False

        if not hitbox.rect.colliderect(hurtbox):
            return False

        # Check invincibility
        if defender.invincible > 0:
            return False

        # Check if defender is blocking
        is_blocking = defender.state == ST_BLOCK or defender.state == ST_CROUCH
        is_parried = False

        if is_blocking:
            # Check parry
            if defender.parry_window > 0:
                is_parried = True
                defender.cursed_energy = min(defender.max_ce, defender.cursed_energy + 15)
                self.effects_queue.append(("parry", defender.x, defender.y - 40))
                hitbox.has_hit = True
                return False

            # Block reduces damage
            damage = int(hitbox.damage * 0.2)
            defender.take_damage(damage, hitbox.kb_x * 0.2, 0, blocked=True)
            self.effects_queue.append(("block", defender.x, defender.y - 40))
            hitbox.has_hit = True
            return True

        # Normal hit
        damage = hitbox.damage

        # Apply attacker buffs
        if attacker.active_buff.get("damage_boost"):
            damage = int(damage * attacker.active_buff["damage_boost"])
        if attacker.active_buff.get("transform"):
            damage = int(damage * 1.3)

        # Black flash check
        is_black_flash = False
        bf_chance = BLACK_FLASH_BASE_CHANCE
        if attacker.active_buff.get("next_black_flash"):
            bf_chance = 1.0
            attacker.active_buff.pop("next_black_flash", None)
        if attacker.story_progress >= 5:
            bf_chance += 0.07  # Story bonus
        if hitbox.move_data.get("guarantee_crit"):
            bf_chance = 1.0

        if random.random() < bf_chance:
            is_black_flash = True
            damage = int(damage * 2.5)
            self.screen_shake = 15
            self.hit_freeze = 8
            self.effects_queue.append(("black_flash", hitbox.rect.centerx, hitbox.rect.centery))
        else:
            # Normal hit effects
            self.screen_shake = max(self.screen_shake, min(10, damage // 15))
            if damage >= 60:
                self.hit_freeze = max(self.hit_freeze, 4)

        # Apply damage
        kb_x = hitbox.kb_x * (1.5 if is_black_flash else 1.0)
        kb_y = hitbox.kb_y * (1.5 if is_black_flash else 1.0)
        defender.take_damage(damage, kb_x, kb_y, blocked=False)

        # Track combo
        combo = self.p1_combo if attacker == attacker else self.p2_combo
        actual_damage = combo.add_hit(damage, hitbox.move_data.get("type", "hit"))

        # CE gain on hit
        attacker.cursed_energy = min(attacker.max_ce, attacker.cursed_energy + 8)

        # Hit effect
        effect_type = "black_flash" if is_black_flash else "hit"
        self.effects_queue.append((effect_type, hitbox.rect.centerx, hitbox.rect.centery))

        hitbox.has_hit = True
        return True

    def check_grab(self, attacker, defender, move_data):
        """Check command grab"""
        if defender.state == ST_BLOCK:
            return False  # Grabs beat blocks
        dist = abs(attacker.x - defender.x)
        grab_range = move_data.get("range", 45)
        if dist <= grab_range:
            damage = move_data.get("damage", 50)
            defender.take_damage(damage, move_data.get("kb_x", 10), move_data.get("kb_y", -10))
            self.screen_shake = 10
            self.hit_freeze = 6
            self.effects_queue.append(("grab", attacker.x, attacker.y - 40))
            return True
        return False

    def check_projectile(self, projectile, defender):
        """Check projectile collision"""
        if not projectile.alive:
            return False
        hurtbox = defender.get_hurtbox()
        proj_rect = pygame.Rect(projectile.x - 15, projectile.y - 15, 30, 30)
        if proj_rect.colliderect(hurtbox):
            if defender.invincible > 0:
                return False
            if defender.state == ST_BLOCK:
                damage = int(projectile.damage * 0.2)
                defender.take_damage(damage, projectile.kb_x * 0.2, 0, blocked=True)
            else:
                defender.take_damage(projectile.damage, projectile.kb_x, projectile.kb_y)
                combo = self.p1_combo if projectile.owner_id == 0 else self.p2_combo
                combo.add_hit(projectile.damage, projectile.name)
            self.screen_shake = max(self.screen_shake, 6)
            projectile.alive = False
            return True
        return False

    def check_trap(self, trap, defender):
        """Check if defender walks into trap"""
        if not trap.alive:
            return False
        trap_rect = pygame.Rect(trap.x - trap.width//2, trap.y - trap.height//2, trap.width, trap.height)
        hurtbox = defender.get_hurtbox()
        if trap_rect.colliderect(hurtbox):
            if defender.invincible > 0:
                return False
            defender.take_damage(trap.damage, trap.kb_x, trap.kb_y)
            if trap.effect == "freeze":
                defender.stun_timer = trap.effect_duration
            trap.alive = False
            return True
        return False

    def process_special_effect(self, move_data, attacker, defender):
        """Handle special move effects like heals, buffs, swaps"""
        effect = move_data.get("effect")
        if not effect:
            return

        if effect == "swap_positions":
            attacker.x, defender.x = defender.x, attacker.x
            self.effects_queue.append(("boogie_woogie", (attacker.x + defender.x) / 2, attacker.y - 40))

        elif effect == "heal":
            heal_amount = move_data.get("heal", 80)
            attacker.hp = min(attacker.max_hp, attacker.hp + heal_amount)
            self.effects_queue.append(("heal", attacker.x, attacker.y - 40))

        elif effect == "freeze":
            stun_frames = move_data.get("effect_duration", 120)
            defender.stun_timer = stun_frames
            self.effects_queue.append(("freeze", defender.x, defender.y - 40))

        elif effect == "speed_boost":
            attacker.active_buff["speed_boost"] = {"amount": 1.5, "duration": 300}

        elif effect == "damage_boost":
            attacker.active_buff["damage_boost"] = {"amount": 1.3, "duration": 600}

        elif effect == "defense_boost":
            attacker.active_buff["defense_boost"] = {"amount": 0.5, "duration": 360}

        elif effect == "transform":
            attacker.active_buff["transform"] = {"duration": 480}
            self.effects_queue.append(("transform", attacker.x, attacker.y - 60))

        elif effect == "reveal_moves":
            attacker.active_buff["revealed"] = {"duration": 600}

        elif effect == "next_black_flash":
            attacker.active_buff["next_black_flash"] = {"duration": 300}

    def update(self):
        self.p1_combo.update()
        self.p2_combo.update()
        if self.screen_shake > 0:
            self.screen_shake -= 1
        if self.hit_freeze > 0:
            self.hit_freeze -= 1
        if self.slow_motion > 0:
            self.slow_motion -= 1

    def get_effects(self):
        effects = self.effects_queue[:]
        self.effects_queue = []
        return effects
