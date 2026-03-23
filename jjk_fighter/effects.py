import pygame
import math
import random
from particles import ParticleSystem

# Color palette
BLUE_Cursed = (30, 100, 255)
RED_Cursed = (255, 50, 50)
PURPLE_Cursed = (180, 50, 255)
ORANGE_Cursed = (255, 150, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHIBUYA_BG = (25, 20, 35)

class CurseEffect:
    """Base class for curse technique visual effects"""
    def __init__(self, x, y, facing_right=True):
        self.x = x
        self.y = y
        self.facing_right = facing_right
        self.frame = 0
        self.alive = True
        self.particles = ParticleSystem()

    def update(self):
        self.frame += 1
        self.particles.update()

    def draw(self, surface):
        self.particles.draw(surface)


class DivergentFist(CurseEffect):
    """Yuji's punch shockwave effect"""
    def __init__(self, x, y, facing_right):
        super().__init__(x, y, facing_right)
        self.shockwave_radius = 0
        self.max_radius = 80

    def update(self):
        super().update()
        dir = 1 if self.facing_right else -1
        self.x += dir * 8
        self.shockwave_radius = min(self.max_radius, self.shockwave_radius + 6)
        self.particles.emit(self.x, self.y, 3, ORANGE_Cursed, (2, 6), (3, 8), (10, 25), 60, 0 if self.facing_right else 180)
        if self.frame > 20:
            self.alive = False

    def draw(self, surface):
        super().draw(surface)
        if self.shockwave_radius > 0:
            alpha = max(0, 200 - self.frame * 10)
            # Draw expanding ring
            ring_surf = pygame.Surface((self.shockwave_radius * 2 + 10, self.shockwave_radius * 2 + 10), pygame.SRCALPHA)
            for i in range(3):
                r = self.shockwave_radius - i * 5
                if r > 0:
                    color = (255, 150 + i * 30, 30, max(0, alpha - i * 60))
                    pygame.draw.circle(ring_surf, color, (self.shockwave_radius + 5, self.shockwave_radius + 5), int(r), 3)
            surface.blit(ring_surf, (int(self.x) - self.shockwave_radius - 5, int(self.y) - self.shockwave_radius - 5))


class BlackFlash(CurseEffect):
    """Yuji's Black Flash - critical hit burst"""
    def __init__(self, x, y, facing_right):
        super().__init__(x, y, facing_right)
        self.flash_alpha = 255
        self.lightning_bolts = [(x, y) for _ in range(5)]

    def update(self):
        super().update()
        self.flash_alpha = max(0, self.flash_alpha - 12)
        # Generate lightning
        for i in range(len(self.lightning_bolts)):
            self.lightning_bolts[i] = (
                self.x + random.randint(-60, 60),
                self.y + random.randint(-60, 60)
            )
        self.particles.emit(self.x, self.y, 8, (255, 255, 200), (5, 12), (2, 5), (5, 15), 360, 0, gravity=0)
        self.particles.emit(self.x, self.y, 5, ORANGE_Cursed, (3, 8), (4, 10), (15, 30), 360, 0, gravity=0.05)
        if self.frame > 30:
            self.alive = False

    def draw(self, surface):
        # White flash overlay
        if self.flash_alpha > 0:
            flash = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            flash.fill((255, 255, 255, int(self.flash_alpha)))
            surface.blit(flash, (0, 0))
        # Lightning bolts
        for _ in range(3):
            points = [(self.x, self.y)]
            cx, cy = self.x, self.y
            for _ in range(6):
                cx += random.randint(-30, 30)
                cy += random.randint(-30, 30)
                points.append((cx, cy))
            if len(points) > 1:
                color = (255, 255, 200) if random.random() > 0.5 else ORANGE_Cursed
                pygame.draw.lines(surface, color, False, points, 2)
        super().draw(surface)


class InfinityShield(CurseEffect):
    """Gojo's Infinity - protective barrier"""
    def __init__(self, x, y, facing_right, duration=60):
        super().__init__(x, y, facing_right)
        self.duration = duration
        self.radius = 40

    def update(self):
        super().update()
        self.particles.emit_ring(self.x, self.y, 2, BLUE_Cursed, self.radius, (1, 3), (5, 15))
        if self.frame % 10 == 0:
            self.particles.emit_spiral(self.x, self.y, 8, BLUE_Cursed, True, (2, 4), (20, 40))
        if self.frame > self.duration:
            self.alive = False

    def draw(self, surface):
        super().draw(surface)
        # Multiple concentric rings
        for i in range(4):
            r = self.radius + i * 8
            alpha = 150 - i * 30
            ring_surf = pygame.Surface((r * 2 + 10, r * 2 + 10), pygame.SRCALPHA)
            color = (30, 100, 255, alpha)
            pygame.draw.circle(ring_surf, color, (r + 5, r + 5), r, 2)
            surface.blit(ring_surf, (int(self.x) - r - 5, int(self.y) - r - 5))
        # Inner glow
        glow_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (100, 150, 255, 80 + int(40 * math.sin(self.frame * 0.1))), (30, 30), 25)
        surface.blit(glow_surf, (int(self.x) - 30, int(self.y) - 30))


class HollowPurple(CurseEffect):
    """Gojo's Hollow Purple - massive energy blast"""
    def __init__(self, x, y, facing_right):
        super().__init__(x, y, facing_right)
        self.blast_radius = 10
        self.max_radius = 120
        self.expanding = True

    def update(self):
        super().update()
        dir = 1 if self.facing_right else -1
        if self.expanding:
            self.blast_radius = min(self.max_radius, self.blast_radius + 4)
            if self.blast_radius >= self.max_radius:
                self.expanding = False
        else:
            self.x += dir * 15
            self.particles.emit(self.x, self.y, 10, PURPLE_Cursed, (3, 8), (4, 10), (15, 35), 90, 90 if self.facing_right else 270)
            self.particles.emit(self.x, self.y, 5, (100, 30, 200), (2, 5), (3, 7), (10, 25), 120, 90 if self.facing_right else 270)
        self.particles.emit(self.x, self.y, 4, PURPLE_Cursed, (1, 4), (2, 6), (10, 25), 360, 0, gravity=0)
        if self.frame > 80:
            self.alive = False

    def draw(self, surface):
        super().draw(surface)
        if self.expanding:
            # Charging phase - pulsing orb
            pulse = 1 + 0.15 * math.sin(self.frame * 0.3)
            r = int(self.blast_radius * pulse)
            orb_surf = pygame.Surface((r * 2 + 20, r * 2 + 20), pygame.SRCALPHA)
            for i in range(5):
                alpha = 200 - i * 40
                color = (180 - i * 20, 50, 255, alpha)
                pygame.draw.circle(orb_surf, color, (r + 10, r + 10), r - i * 5, 3)
            # Core glow
            pygame.draw.circle(orb_surf, (220, 150, 255, 180), (r + 10, r + 10), r // 3)
            surface.blit(orb_surf, (int(self.x) - r - 10, int(self.y) - r - 10))
        else:
            # Travelling blast
            r = 30
            blast_surf = pygame.Surface((r * 2 + 20, r * 2 + 20), pygame.SRCALPHA)
            for i in range(4):
                color = (180 - i * 30, 50, 255, 200 - i * 50)
                pygame.draw.circle(blast_surf, color, (r + 10, r + 10), r - i * 5)
            surface.blit(blast_surf, (int(self.x) - r - 10, int(self.y) - r - 10))


class CleaveSlash(CurseEffect):
    """Sukuna's Cleave - slashing wave"""
    def __init__(self, x, y, facing_right):
        super().__init__(x, y, facing_right)
        self.slash_length = 0
        self.max_length = 200

    def update(self):
        super().update()
        dir = 1 if self.facing_right else -1
        self.x += dir * 12
        self.slash_length = min(self.max_length, self.slash_length + 15)
        self.particles.emit_line(
            self.x - (self.slash_length / 2 if self.facing_right else 0),
            self.y,
            self.x + (0 if self.facing_right else self.slash_length / 2),
            self.y, 5, RED_Cursed, (2, 4), (5, 15)
        )
        if self.frame > 30:
            self.alive = False

    def draw(self, surface):
        super().draw(surface)
        dir = 1 if self.facing_right else -1
        # Multiple slash lines
        for i in range(3):
            offset = (i - 1) * 8
            start_x = self.x - dir * self.slash_length / 2
            end_x = self.x + dir * self.slash_length / 2
            y = self.y + offset + math.sin(self.frame * 0.3 + i) * 5
            alpha = 255 - i * 60
            color = (255, 50 + i * 30, 50)
            pygame.draw.line(surface, color, (int(start_x), int(y)), (int(end_x), int(y)), 3 - i)


class MalevolentShrine(CurseEffect):
    """Sukuna's Domain Expansion - screen-filling shrine effect"""
    def __init__(self, x, y, facing_right, screen_size):
        super().__init__(x, y, facing_right)
        self.screen_w, self.screen_h = screen_size
        self.duration = 120
        self.shrine_lines = []
        for _ in range(20):
            self.shrine_lines.append({
                'x1': random.randint(0, self.screen_w),
                'y1': 0,
                'x2': random.randint(0, self.screen_w),
                'y2': self.screen_h,
                'speed': random.uniform(2, 6)
            })

    def update(self):
        super().update()
        # Cursed energy particles everywhere
        self.particles.emit(
            random.randint(0, self.screen_w),
            random.randint(0, self.screen_h),
            3, RED_Cursed, (1, 3), (2, 4), (10, 30), 360, 0, gravity=-0.05
        )
        # Slash lines
        for line in self.shrine_lines:
            line['x1'] += line['speed']
            line['x2'] += line['speed']
            if line['x1'] > self.screen_w:
                line['x1'] = -50
                line['x2'] = random.randint(0, self.screen_w)
        if self.frame > self.duration:
            self.alive = False

    def draw(self, surface):
        # Dark red overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        alpha = min(100, self.frame * 3)
        overlay.fill((80, 0, 0, int(alpha)))
        surface.blit(overlay, (0, 0))
        # Shrine structure lines
        for line in self.shrine_lines:
            color = (255, 50, 50, 150)
            pygame.draw.line(surface, RED_Cursed, (int(line['x1']), line['y1']), (int(line['x2']), line['y2']), 2)
        super().draw(surface)


class ShadowDogs(CurseEffect):
    """Megumi's shadow dog summons"""
    def __init__(self, x, y, facing_right):
        super().__init__(x, y, facing_right)
        self.dogs = []
        for i in range(3):
            self.dogs.append({
                'x': x + random.randint(-30, 30),
                'y': y + random.randint(-20, 20),
                'target_x': x + (1 if self.facing_right else -1) * (200 + i * 50),
                'speed': random.uniform(4, 7),
                'frame_offset': i * 10
            })

    def update(self):
        super().update()
        for dog in self.dogs:
            if self.frame > dog['frame_offset']:
                dir = 1 if self.facing_right else -1
                dog['x'] += dir * dog['speed']
                dog['y'] += math.sin(self.frame * 0.2) * 2
                self.particles.emit(dog['x'], dog['y'], 2, PURPLE_Cursed, (1, 3), (2, 4), (8, 20), 180, 270 if self.facing_right else 90, gravity=-0.1)
        if self.frame > 60:
            self.alive = False

    def draw(self, surface):
        super().draw(surface)
        for dog in self.dogs:
            if self.frame > dog['frame_offset']:
                # Shadow dog silhouette
                dx, dy = int(dog['x']), int(dog['y'])
                # Body
                points = [(dx-15, dy), (dx+15, dy-5), (dx+20, dy+5), (dx-10, dy+10)]
                pygame.draw.polygon(surface, (30, 20, 50), points)
                pygame.draw.polygon(surface, PURPLE_Cursed, points, 2)
                # Eyes
                eye_x = dx + 10 if self.facing_right else dx - 10
                pygame.draw.circle(surface, PURPLE_Cursed, (eye_x, dy - 3), 3)


class NueLightning(CurseEffect):
    """Megumi's Nue lightning strike"""
    def __init__(self, x, y, facing_right):
        super().__init__(x, y, facing_right)
        self.lightning_path = [(x, 0)]
        cx, cy = x, 0
        while cy < y:
            cx += random.randint(-40, 40)
            cy += random.randint(20, 50)
            self.lightning_path.append((cx, min(cy, y)))
        self.flash_alpha = 255

    def update(self):
        super().update()
        self.flash_alpha = max(0, self.flash_alpha - 10)
        for point in self.lightning_path:
            self.particles.emit(point[0], point[1], 2, (200, 200, 255), (2, 5), (2, 4), (5, 15), 360, 0, gravity=0)
        if self.frame > 20:
            self.alive = False

    def draw(self, surface):
        if self.flash_alpha > 0:
            flash = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            flash.fill((200, 200, 255, int(self.flash_alpha * 0.3)))
            surface.blit(flash, (0, 0))
        # Lightning bolt
        if len(self.lightning_path) > 1:
            pygame.draw.lines(surface, (200, 200, 255), False, self.lightning_path, 4)
            pygame.draw.lines(surface, WHITE, False, self.lightning_path, 2)
        super().draw(surface)


class DomainExpansionOverlay:
    """Full-screen domain expansion visual effect"""
    def __init__(self, character_name, screen_size):
        self.character_name = character_name
        self.screen_w, self.screen_h = screen_size
        self.frame = 0
        self.duration = 180
        self.alive = True
        self.particles = ParticleSystem()
        self.colors = {
            'gojo': BLUE_Cursed,
            'sukuna': RED_Cursed,
            'megumi': PURPLE_Cursed,
            'yuji': ORANGE_Cursed
        }
        self.color = self.colors.get(character_name, WHITE)

    def update(self):
        self.frame += 1
        self.particles.update()
        # Spawn particles based on domain type
        if self.character_name == 'gojo':
            # Infinite Void - floating cubes
            self.particles.emit(
                random.randint(0, self.screen_w),
                random.randint(0, self.screen_h),
                2, BLUE_Cursed, (0.5, 2), (3, 8), (30, 60), 360, 0, gravity=0
            )
        elif self.character_name == 'sukuna':
            # Malevolent Shrine - red slashes everywhere
            self.particles.emit(
                random.randint(0, self.screen_w),
                random.randint(0, self.screen_h),
                3, RED_Cursed, (2, 5), (2, 5), (15, 30), 360, 0, gravity=0
            )
        if self.frame > self.duration:
            self.alive = False

    def draw(self, surface):
        # Overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        alpha = min(120, self.frame * 4)
        color = self.color + (int(alpha),)
        overlay.fill(color)
        surface.blit(overlay, (0, 0))
        # Domain text
        if 30 < self.frame < 90:
            font = pygame.font.SysFont('arial', 48, bold=True)
            text = font.render("DOMAIN EXPANSION", True, WHITE)
            rect = text.get_rect(center=(self.screen_w // 2, self.screen_h // 3))
            text_alpha = min(255, (self.frame - 30) * 8)
            text_surf = pygame.Surface(text.get_size(), pygame.SRCALPHA)
            text_surf.blit(text, (0, 0))
            text_surf.set_alpha(int(text_alpha))
            surface.blit(text_surf, rect)
        self.particles.draw(surface)


# Effect factory
def create_effect(effect_name, x, y, facing_right, screen_size=(1280, 720)):
    effects = {
        'divergent_fist': DivergentFist,
        'black_flash': BlackFlash,
        'infinity': InfinityShield,
        'hollow_purple': HollowPurple,
        'cleave': CleaveSlash,
        'malevolent_shrine': lambda x, y, fr: MalevolentShrine(x, y, fr, screen_size),
        'shadow_dogs': ShadowDogs,
        'nue_lightning': NueLightning,
    }
    factory = effects.get(effect_name)
    if factory:
        return factory(x, y, facing_right)
    return None
