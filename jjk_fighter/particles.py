import pygame
import random
import math

class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime, gravity=0.1, fade=True):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.max_lifetime = lifetime
        self.lifetime = lifetime
        self.gravity = gravity
        self.fade = fade
        self.alive = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, surface):
        if not self.alive:
            return
        alpha = max(0, min(255, int(255 * (self.lifetime / self.max_lifetime)))) if self.fade else 255
        current_size = max(1, int(self.size * (self.lifetime / self.max_lifetime)))
        r, g, b = self.color
        color = (r, g, b)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), current_size)
        # Glow effect
        glow_surf = pygame.Surface((current_size * 4, current_size * 4), pygame.SRCALPHA)
        glow_color = (r, g, b, alpha // 3)
        pygame.draw.circle(glow_surf, glow_color, (current_size * 2, current_size * 2), current_size * 2)
        surface.blit(glow_surf, (int(self.x) - current_size * 2, int(self.y) - current_size * 2))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def update(self):
        self.particles = [p for p in self.particles if p.alive]
        for p in self.particles:
            p.update()

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

    def emit(self, x, y, count, color, speed_range=(1, 5), size_range=(2, 6),
             lifetime_range=(15, 40), spread=360, angle=0, gravity=0.1):
        for _ in range(count):
            a = math.radians(random.uniform(angle - spread/2, angle + spread/2))
            speed = random.uniform(*speed_range)
            vx = math.cos(a) * speed
            vy = math.sin(a) * speed
            size = random.uniform(*size_range)
            lifetime = random.randint(*lifetime_range)
            c = (
                min(255, max(0, color[0] + random.randint(-20, 20))),
                min(255, max(0, color[1] + random.randint(-20, 20))),
                min(255, max(0, color[2] + random.randint(-20, 20)))
            )
            self.particles.append(Particle(x, y, vx, vy, c, size, lifetime, gravity))

    def emit_line(self, x1, y1, x2, y2, count, color, size_range=(2, 4), lifetime_range=(10, 30)):
        for _ in range(count):
            t = random.random()
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            vx = random.uniform(-1, 1)
            vy = random.uniform(-2, 0)
            size = random.uniform(*size_range)
            lifetime = random.randint(*lifetime_range)
            self.particles.append(Particle(x, y, vx, vy, color, size, lifetime, gravity=0.05))

    def emit_ring(self, x, y, count, color, radius=50, size_range=(2, 5), lifetime_range=(20, 40)):
        for _ in range(count):
            a = random.uniform(0, math.pi * 2)
            px = x + math.cos(a) * radius
            py = y + math.sin(a) * radius
            vx = math.cos(a) * random.uniform(1, 3)
            vy = math.sin(a) * random.uniform(1, 3)
            size = random.uniform(*size_range)
            lifetime = random.randint(*lifetime_range)
            self.particles.append(Particle(px, py, vx, vy, color, size, lifetime, gravity=0))

    def emit_spiral(self, x, y, count, color, clockwise=True, size_range=(3, 7), lifetime_range=(30, 60)):
        for i in range(count):
            a = (i / count) * math.pi * 4
            if not clockwise:
                a = -a
            r = i * 2
            px = x + math.cos(a) * r
            py = y + math.sin(a) * r
            vx = math.cos(a) * 0.5
            vy = math.sin(a) * 0.5
            size = random.uniform(*size_range)
            lifetime = random.randint(*lifetime_range)
            self.particles.append(Particle(px, py, vx, vy, color, size, lifetime, gravity=0))
