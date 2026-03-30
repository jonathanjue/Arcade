"""
particles.py - 2D Particle System for Street Fighting Game

Provides Particle, ParticleEmitter classes and helper functions for visual effects.
Pygame-only implementation (no numpy).
"""

import math
import random
import pygame


class Particle:
    """A single particle with position, velocity, color, lifetime, size, and gravity."""

    __slots__ = (
        "x", "y", "vx", "vy", "color", "lifetime", "max_lifetime",
        "size", "start_size", "gravity", "alpha", "alive",
    )

    def __init__(self, x, y, vx, vy, color, lifetime, size, gravity=0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        # Store base color (RGB); alpha is managed separately
        self.color = (color[0], color[1], color[2])
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.start_size = size
        self.gravity = gravity
        self.alpha = 255
        self.alive = True

    def update(self, dt):
        """Update particle state. dt is in seconds."""
        if not self.alive:
            return

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False
            return

        # Apply gravity
        self.vy += self.gravity * dt

        # Move
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Fade alpha based on remaining lifetime ratio
        ratio = max(self.lifetime / self.max_lifetime, 0.0)
        self.alpha = int(255 * ratio)

        # Size decay
        self.size = max(self.start_size * ratio, 0.5)

    def draw(self, surface):
        """Draw the particle onto the given surface."""
        if not self.alive or self.alpha <= 0 or self.size < 1:
            return

        r = max(int(self.size), 1)
        # Create a temporary surface with per-pixel alpha
        particle_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        color_with_alpha = (self.color[0], self.color[1], self.color[2], self.alpha)
        pygame.draw.circle(particle_surf, color_with_alpha, (r, r), r)
        surface.blit(particle_surf, (int(self.x) - r, int(self.y) - r))


class ParticleEmitter:
    """Manages a pool of particles, supports emitting bursts and trails."""

    def __init__(self, max_particles=1000):
        self.max_particles = max_particles
        self.particles: list[Particle] = []

    def emit(
        self,
        x,
        y,
        count,
        color,
        speed_range=(50, 200),
        lifetime_range=(0.2, 0.8),
        size_range=(2, 6),
        gravity=0.0,
        angle_range=(0, 360),
    ):
        """
        Spawn particles at (x, y).

        Args:
            x, y: Spawn position.
            count: Number of particles to spawn.
            color: RGB tuple.
            speed_range: (min, max) speed in pixels/sec.
            lifetime_range: (min, max) lifetime in seconds.
            size_range: (min, max) starting radius in pixels.
            gravity: Downward acceleration in pixels/sec^2.
            angle_range: (min, max) angle in degrees for velocity direction.
        """
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                # Remove oldest particle to make room
                self.particles.pop(0)

            angle = math.radians(random.uniform(angle_range[0], angle_range[1]))
            speed = random.uniform(speed_range[0], speed_range[1])
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifetime = random.uniform(lifetime_range[0], lifetime_range[1])
            size = random.uniform(size_range[0], size_range[1])

            # Slight color variation
            r = min(255, max(0, color[0] + random.randint(-20, 20)))
            g = min(255, max(0, color[1] + random.randint(-20, 20)))
            b = min(255, max(0, color[2] + random.randint(-20, 20)))

            self.particles.append(Particle(x, y, vx, vy, (r, g, b), lifetime, size, gravity))

    def emit_trail(
        self,
        x,
        y,
        vx,
        vy,
        color,
        count=3,
        speed_range=(10, 50),
        lifetime_range=(0.1, 0.3),
        size_range=(1, 3),
        gravity=0.0,
    ):
        """Emit a small trail of particles moving opposite to the given velocity."""
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                self.particles.pop(0)

            # Particles drift opposite to movement direction
            angle = math.atan2(-vy, -vx) + random.uniform(-0.5, 0.5)
            speed = random.uniform(speed_range[0], speed_range[1])
            pvx = math.cos(angle) * speed
            pvy = math.sin(angle) * speed
            lifetime = random.uniform(lifetime_range[0], lifetime_range[1])
            size = random.uniform(size_range[0], size_range[1])

            r = min(255, max(0, color[0] + random.randint(-15, 15)))
            g = min(255, max(0, color[1] + random.randint(-15, 15)))
            b = min(255, max(0, color[2] + random.randint(-15, 15)))

            self.particles.append(Particle(x, y, pvx, pvy, (r, g, b), lifetime, size, gravity))

    def update(self, dt):
        """Update all particles; remove dead ones."""
        alive = []
        for p in self.particles:
            p.update(dt)
            if p.alive:
                alive.append(p)
        self.particles = alive

    def draw(self, surface):
        """Draw all living particles."""
        for p in self.particles:
            p.draw(surface)

    def clear(self):
        """Remove all particles."""
        self.particles.clear()

    @property
    def count(self):
        return len(self.particles)


# ---------------------------------------------------------------------------
# Global default emitter for convenience helpers
# ---------------------------------------------------------------------------
_default_emitter = ParticleEmitter(max_particles=2000)


def get_default_emitter() -> ParticleEmitter:
    """Return the module-level default emitter (useful for global effects)."""
    return _default_emitter


# ---------------------------------------------------------------------------
# Helper functions - common fighting-game visual effects
# ---------------------------------------------------------------------------

def hit_spark(x, y, color=(255, 255, 100)):
    """Bright sparks radiating outward on hit impact."""
    _default_emitter.emit(
        x, y,
        count=20,
        color=color,
        speed_range=(150, 400),
        lifetime_range=(0.15, 0.4),
        size_range=(2, 5),
        gravity=200,
        angle_range=(0, 360),
    )
    # Add a few larger slower sparks
    _default_emitter.emit(
        x, y,
        count=5,
        color=(255, 255, 255),
        speed_range=(50, 120),
        lifetime_range=(0.1, 0.25),
        size_range=(4, 7),
        gravity=100,
        angle_range=(0, 360),
    )


def dust_puff(x, y):
    """Ground dust puff, e.g. on landing or dashing."""
    _default_emitter.emit(
        x, y,
        count=12,
        color=(180, 160, 130),
        speed_range=(20, 80),
        lifetime_range=(0.3, 0.7),
        size_range=(3, 8),
        gravity=-30,  # Slight upward drift then settle
        angle_range=(-160, -20),  # Mostly upward arc
    )


def fire_trail(x, y):
    """Flickering fire trail particles."""
    # Hot core
    _default_emitter.emit(
        x, y,
        count=4,
        color=(255, 200, 50),
        speed_range=(10, 40),
        lifetime_range=(0.15, 0.35),
        size_range=(3, 6),
        gravity=-120,  # Rise upward
        angle_range=(-170, -10),
    )
    # Outer flame
    _default_emitter.emit(
        x, y,
        count=3,
        color=(255, 80, 10),
        speed_range=(15, 50),
        lifetime_range=(0.2, 0.5),
        size_range=(2, 5),
        gravity=-100,
        angle_range=(-160, -20),
    )


def energy_burst(x, y, color=(100, 150, 255)):
    """Large energy burst for special moves (ki blasts, etc.)."""
    # Inner bright burst
    _default_emitter.emit(
        x, y,
        count=30,
        color=(255, 255, 255),
        speed_range=(100, 350),
        lifetime_range=(0.2, 0.5),
        size_range=(2, 6),
        gravity=0,
        angle_range=(0, 360),
    )
    # Colored outer ring
    _default_emitter.emit(
        x, y,
        count=25,
        color=color,
        speed_range=(200, 450),
        lifetime_range=(0.3, 0.7),
        size_range=(3, 7),
        gravity=50,
        angle_range=(0, 360),
    )


def slash_effect(x, y, direction=1, color=(200, 220, 255)):
    """
    Arc-shaped slash effect.

    Args:
        x, y: Center of the slash arc.
        direction: 1 for rightward slash, -1 for leftward.
        color: RGB color of the slash.
    """
    if direction >= 0:
        angle_range = (-60, 60)  # Rightward arc
    else:
        angle_range = (120, 240)  # Leftward arc

    _default_emitter.emit(
        x, y,
        count=18,
        color=color,
        speed_range=(200, 400),
        lifetime_range=(0.1, 0.3),
        size_range=(2, 5),
        gravity=0,
        angle_range=angle_range,
    )
    # White streaks along the slash
    _default_emitter.emit(
        x, y,
        count=8,
        color=(255, 255, 255),
        speed_range=(300, 500),
        lifetime_range=(0.08, 0.2),
        size_range=(1, 3),
        gravity=0,
        angle_range=angle_range,
    )


def block_spark(x, y):
    """Defensive block spark effect."""
    _default_emitter.emit(
        x, y,
        count=15,
        color=(200, 200, 255),
        speed_range=(80, 250),
        lifetime_range=(0.1, 0.3),
        size_range=(2, 5),
        gravity=100,
        angle_range=(0, 360),
    )
    # Bright flash center
    _default_emitter.emit(
        x, y,
        count=6,
        color=(255, 255, 255),
        speed_range=(30, 80),
        lifetime_range=(0.05, 0.15),
        size_range=(5, 9),
        gravity=0,
        angle_range=(0, 360),
    )


# ---------------------------------------------------------------------------
# Demo / self-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Particle System Demo")
    clock = pygame.time.Clock()

    emitter = ParticleEmitter(max_particles=2000)
    running = True
    timer = 0.0
    demo_phase = 0
    demo_names = ["hit_spark", "dust_puff", "fire_trail", "energy_burst", "slash_effect", "block_spark"]

    font = pygame.font.SysFont(None, 28)

    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    demo_phase = (demo_phase + 1) % len(demo_names)
                    emitter.clear()
                    timer = 0

        timer += dt
        # Trigger effects periodically
        if timer > 0.5:
            timer = 0
            cx, cy = 400, 300
            name = demo_names[demo_phase]
            if name == "hit_spark":
                hit_spark(cx + random.randint(-100, 100), cy + random.randint(-50, 50))
            elif name == "dust_puff":
                dust_puff(cx + random.randint(-100, 100), cy + 80)
            elif name == "fire_trail":
                fire_trail(cx + random.randint(-50, 50), cy + random.randint(-50, 50))
            elif name == "energy_burst":
                energy_burst(cx + random.randint(-100, 100), cy + random.randint(-50, 50))
            elif name == "slash_effect":
                slash_effect(cx, cy, direction=random.choice([-1, 1]))
            elif name == "block_spark":
                block_spark(cx + random.randint(-80, 80), cy + random.randint(-40, 40))

        # Also use the module-level default emitter for helpers
        _default_emitter.update(dt)
        emitter.update(dt)

        screen.fill((20, 20, 30))
        emitter.draw(screen)
        _default_emitter.draw(screen)

        label = font.render(f"Effect: {demo_names[demo_phase]}  |  Particles: {emitter.count + _default_emitter.count}  |  SPACE to change", True, (200, 200, 200))
        screen.blit(label, (20, 20))

        pygame.display.flip()

    pygame.quit()
