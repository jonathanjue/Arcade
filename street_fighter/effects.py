"""
Special move visual effects for Street Fighter-style game.
Projectile, ZoneEffect, GrabEffect, and EffectManager classes.
Uses particles.py ParticleEmitter for particle effects.
"""

import pygame
import math
import random
from typing import Optional, Callable, List, Tuple

# Try to import particles module if available
try:
    from particles import ParticleEmitter
    HAS_PARTICLES = True
except ImportError:
    HAS_PARTICLES = False


# --- Constants ---
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
GROUND_Y = 520  # Must match fighter.py and stages.py


class Projectile:
    """
    A moving projectile (fireball, energy ball, etc.).
    Moves horizontally, has damage/hitbox, disappears on hit or off-screen.
    """

    def __init__(
        self,
        x: float,
        y: float,
        direction: int,  # 1 for right, -1 for left
        speed: float = 8.0,
        damage: int = 15,
        hitstun: int = 20,
        knockback: float = 5.0,
        radius: int = 20,
        color: Tuple[int, int, int] = (255, 100, 0),
        inner_color: Optional[Tuple[int, int, int]] = None,
        max_range: float = 800.0,
        projectile_type: str = "fireball",
        owner_id: int = 0,
    ):
        self.x = float(x)
        self.y = float(y)
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.hitstun = hitstun
        self.knockback = knockback
        self.radius = radius
        self.color = color
        self.inner_color = inner_color or self._lighten(color)
        self.max_range = max_range
        self.projectile_type = projectile_type
        self.owner_id = owner_id

        self.start_x = self.x
        self.alive = True
        self.has_hit = False
        self.age = 0
        self.rotation = 0.0
        self.pulse_timer = 0.0

        # Particle trail
        self.particles: List[dict] = []
        self.max_particles = 30

        # Hitbox rect (updated each frame)
        self.hitbox = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    @staticmethod
    def _lighten(color: Tuple[int, int, int], amount: int = 100) -> Tuple[int, int, int]:
        return tuple(min(255, c + amount) for c in color)

    def get_hitbox(self) -> pygame.Rect:
        return self.hitbox

    def _spawn_trail_particle(self):
        """Add a trail particle behind the projectile."""
        if len(self.particles) >= self.max_particles:
            return
        spread = self.radius * 0.6
        self.particles.append({
            "x": self.x - self.direction * random.uniform(0, self.radius),
            "y": self.y + random.uniform(-spread, spread),
            "vx": -self.direction * random.uniform(0.5, 2.0),
            "vy": random.uniform(-1.0, 1.0),
            "life": random.randint(10, 25),
            "max_life": 25,
            "size": random.randint(2, max(3, self.radius // 3)),
            "color": self.color,
        })

    def update(self):
        """Move projectile and update particles."""
        if not self.alive:
            return

        self.age += 1
        self.pulse_timer += 0.15
        self.rotation += 5.0 * self.direction

        # Move
        self.x += self.speed * self.direction

        # Update hitbox
        self.hitbox.center = (int(self.x), int(self.y))

        # Trail particles
        if self.age % 2 == 0:
            self._spawn_trail_particle()

        # Update particles
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1
        self.particles = [p for p in self.particles if p["life"] > 0]

        # Check out of bounds or max range
        dist_traveled = abs(self.x - self.start_x)
        if self.x < -self.radius * 2 or self.x > SCREEN_WIDTH + self.radius * 2:
            self.alive = False
        if dist_traveled > self.max_range:
            self.alive = False

    def on_hit(self):
        """Called when projectile hits an opponent."""
        self.has_hit = True
        # Burst of particles on hit
        for _ in range(15):
            spread = self.radius * 1.5
            self.particles.append({
                "x": self.x + random.uniform(-spread, spread),
                "y": self.y + random.uniform(-spread, spread),
                "vx": random.uniform(-4.0, 4.0),
                "vy": random.uniform(-4.0, 2.0),
                "life": random.randint(10, 30),
                "max_life": 30,
                "size": random.randint(3, 8),
                "color": self.inner_color,
            })
        # Mark for cleanup next frame (allow hit particles to draw)
        self.alive = False

    def draw(self, surface: pygame.Surface):
        """Draw projectile and particles."""
        if not self.alive and not self.particles:
            return

        # Draw trail particles
        for p in self.particles:
            alpha = p["life"] / max(p["max_life"], 1)
            size = max(1, int(p["size"] * alpha))
            color = tuple(int(c * alpha) for c in p["color"])
            pygame.draw.circle(surface, color, (int(p["x"]), int(p["y"])), size)

        if not self.alive:
            return

        # Pulsing size
        pulse = 1.0 + 0.15 * math.sin(self.pulse_timer)
        draw_radius = int(self.radius * pulse)

        # Outer glow
        for i in range(3, 0, -1):
            glow_r = draw_radius + i * 4
            glow_color = tuple(max(0, c - 60 * i) for c in self.color)
            alpha_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
            pygame.draw.circle(alpha_surf, (*glow_color, 60), (glow_r, glow_r), glow_r)
            surface.blit(alpha_surf, (int(self.x) - glow_r, int(self.y) - glow_r))

        # Draw based on type
        if self.projectile_type == "fireball":
            self._draw_fireball(surface, draw_radius)
        elif self.projectile_type == "energy":
            self._draw_energy_ball(surface, draw_radius)
        elif self.projectile_type == "hadouken":
            self._draw_hadouken(surface, draw_radius)
        else:
            self._draw_generic(surface, draw_radius)

    def _draw_fireball(self, surface: pygame.Surface, radius: int):
        """Draw a fireball with flickering flames."""
        # Core
        pygame.draw.circle(surface, self.inner_color, (int(self.x), int(self.y)), radius)
        # Flame tips
        for _ in range(4):
            angle = random.uniform(0, 2 * math.pi)
            dist = radius * random.uniform(0.6, 1.3)
            fx = self.x + math.cos(angle) * dist
            fy = self.y + math.sin(angle) * dist
            fsize = random.randint(2, max(3, radius // 2))
            flame_color = (
                min(255, self.color[0] + random.randint(0, 50)),
                max(0, self.color[1] - random.randint(0, 50)),
                self.color[2],
            )
            pygame.draw.circle(surface, flame_color, (int(fx), int(fy)), fsize)
        # Bright center
        pygame.draw.circle(surface, (255, 255, 200), (int(self.x), int(self.y)), max(2, radius // 3))

    def _draw_energy_ball(self, surface: pygame.Surface, radius: int):
        """Draw an energy/ki ball with rings."""
        # Core
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), radius)
        pygame.draw.circle(surface, self.inner_color, (int(self.x), int(self.y)), int(radius * 0.6))
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), max(2, radius // 4))
        # Rotating ring
        ring_r = int(radius * 1.2)
        for i in range(8):
            angle = math.radians(self.rotation) + i * (math.pi / 4)
            px = self.x + math.cos(angle) * ring_r
            py = self.y + math.sin(angle) * ring_r
            pygame.draw.circle(surface, self.inner_color, (int(px), int(py)), 3)

    def _draw_hadouken(self, surface: pygame.Surface, radius: int):
        """Draw a hadouken-style blue energy ball."""
        # Blue-white core
        pygame.draw.circle(surface, (50, 100, 255), (int(self.x), int(self.y)), radius)
        pygame.draw.circle(surface, (150, 200, 255), (int(self.x), int(self.y)), int(radius * 0.7))
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), max(2, radius // 3))
        # Elongated shape hint
        elongation = int(radius * 0.4 * self.direction)
        pygame.draw.ellipse(
            surface,
            (100, 150, 255),
            (int(self.x) - radius + elongation, int(self.y) - int(radius * 0.6),
             radius * 2, int(radius * 1.2)),
            2,
        )

    def _draw_generic(self, surface: pygame.Surface, radius: int):
        """Generic projectile draw."""
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), radius)
        pygame.draw.circle(surface, self.inner_color, (int(self.x), int(self.y)), int(radius * 0.5))
        pygame.draw.circle(
            surface, (255, 255, 255), (int(self.x), int(self.y)), max(2, radius // 4)
        )


class ZoneEffect:
    """
    An area damage zone (storm cloud, fire patch, etc.) with duration and tick damage.
    Deals damage at regular intervals to anyone inside.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: float = 200,
        height: float = 100,
        duration: int = 180,  # frames (approx 3 seconds at 60fps)
        tick_interval: int = 30,  # frames between damage ticks
        damage_per_tick: int = 5,
        zone_type: str = "fire",
        color: Tuple[int, int, int] = (255, 80, 0),
        owner_id: int = 0,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.duration = duration
        self.tick_interval = tick_interval
        self.damage_per_tick = damage_per_tick
        self.zone_type = zone_type
        self.color = color
        self.owner_id = owner_id

        self.alive = True
        self.age = 0
        self.tick_timer = 0

        # Hitbox for zone
        self.hitbox = pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height),
            int(self.width),
            int(self.height),
        )

        # Internal particles
        self.particles: List[dict] = []
        self.max_particles = 40

    def get_hitbox(self) -> pygame.Rect:
        return self.hitbox

    def should_damage(self) -> bool:
        """Returns True on the frame when damage should be applied."""
        return self.age > 0 and self.age % self.tick_interval == 0

    def _spawn_zone_particle(self):
        """Spawn a particle within the zone."""
        if len(self.particles) >= self.max_particles:
            return

        px = random.uniform(self.hitbox.left, self.hitbox.right)
        py = random.uniform(self.hitbox.top, self.hitbox.bottom)

        if self.zone_type == "fire":
            self.particles.append({
                "x": px, "y": py,
                "vx": random.uniform(-0.5, 0.5),
                "vy": random.uniform(-3.0, -0.5),
                "life": random.randint(15, 35),
                "max_life": 35,
                "size": random.randint(3, 8),
                "color": (
                    min(255, self.color[0] + random.randint(-20, 50)),
                    max(0, self.color[1] + random.randint(-20, 20)),
                    self.color[2],
                ),
            })
        elif self.zone_type == "storm":
            self.particles.append({
                "x": px, "y": self.hitbox.top + random.uniform(0, self.height * 0.3),
                "vx": random.uniform(-1.0, 1.0),
                "vy": random.uniform(1.0, 4.0),
                "life": random.randint(20, 40),
                "max_life": 40,
                "size": random.randint(2, 5),
                "color": (150, 150, 200),
            })
        elif self.zone_type == "poison":
            self.particles.append({
                "x": px, "y": py,
                "vx": random.uniform(-1.0, 1.0),
                "vy": random.uniform(-2.0, 0.5),
                "life": random.randint(20, 40),
                "max_life": 40,
                "size": random.randint(4, 10),
                "color": (
                    random.randint(50, 100),
                    random.randint(180, 255),
                    random.randint(50, 100),
                ),
            })
        else:
            self.particles.append({
                "x": px, "y": py,
                "vx": random.uniform(-1.0, 1.0),
                "vy": random.uniform(-2.0, 0.5),
                "life": random.randint(15, 30),
                "max_life": 30,
                "size": random.randint(3, 7),
                "color": self.color,
            })

    def update(self):
        """Update zone lifetime and particles."""
        if not self.alive:
            return

        self.age += 1
        self.tick_timer += 1

        if self.age >= self.duration:
            self.alive = False

        # Spawn particles
        if self.age % 2 == 0:
            self._spawn_zone_particle()

        # Update particles
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1
        self.particles = [p for p in self.particles if p["life"] > 0]

    def draw(self, surface: pygame.Surface):
        """Draw the zone effect."""
        # Draw particles even if dead (fade out)
        for p in self.particles:
            alpha = p["life"] / max(p["max_life"], 1)
            size = max(1, int(p["size"] * alpha))
            color = tuple(int(c * alpha) for c in p["color"])
            pygame.draw.circle(surface, color, (int(p["x"]), int(p["y"])), size)

        if not self.alive:
            return

        # Fade in/out
        fade_in = min(1.0, self.age / 20.0)
        fade_out = min(1.0, (self.duration - self.age) / 30.0) if self.age > self.duration - 30 else 1.0
        alpha_mult = fade_in * fade_out

        # Semi-transparent zone overlay
        zone_surf = pygame.Surface((int(self.width), int(self.height)), pygame.SRCALPHA)

        if self.zone_type == "fire":
            base_alpha = int(50 * alpha_mult)
            pygame.draw.rect(
                zone_surf,
                (*self.color, base_alpha),
                (0, 0, int(self.width), int(self.height)),
                border_radius=8,
            )
            # Flickering top edge
            for i in range(int(self.width) // 10):
                fx = i * 10 + random.randint(-3, 3)
                fh = random.randint(5, 20)
                fcolor = (
                    min(255, self.color[0] + random.randint(0, 50)),
                    min(255, self.color[1] + random.randint(0, 30)),
                    0,
                )
                pygame.draw.rect(
                    zone_surf,
                    (*fcolor, int(100 * alpha_mult)),
                    (fx, 0, 8, fh),
                )
        elif self.zone_type == "storm":
            base_alpha = int(40 * alpha_mult)
            pygame.draw.rect(
                zone_surf,
                (40, 40, 80, base_alpha),
                (0, 0, int(self.width), int(self.height)),
                border_radius=12,
            )
            # Cloud at top
            cloud_y = 10
            for cx in range(20, int(self.width) - 20, 30):
                cr = random.randint(15, 25)
                pygame.draw.circle(
                    zone_surf,
                    (80, 80, 100, int(80 * alpha_mult)),
                    (cx, cloud_y),
                    cr,
                )
            # Lightning flash
            if self.age % self.tick_interval < 3:
                flash_alpha = int(150 * alpha_mult)
                zone_surf.fill((255, 255, 200, flash_alpha))
        elif self.zone_type == "poison":
            base_alpha = int(45 * alpha_mult)
            pygame.draw.rect(
                zone_surf,
                (40, 120, 40, base_alpha),
                (0, 0, int(self.width), int(self.height)),
                border_radius=10,
            )
            # Bubbles
            for _ in range(3):
                bx = random.randint(10, int(self.width) - 10)
                by = random.randint(10, int(self.height) - 10)
                br = random.randint(3, 8)
                pygame.draw.circle(
                    zone_surf,
                    (100, 200, 100, int(80 * alpha_mult)),
                    (bx, by), br, 1,
                )
        else:
            base_alpha = int(50 * alpha_mult)
            pygame.draw.rect(
                zone_surf,
                (*self.color, base_alpha),
                (0, 0, int(self.width), int(self.height)),
                border_radius=6,
            )

        # Border
        border_alpha = int(120 * alpha_mult)
        pygame.draw.rect(
            zone_surf,
            (*self.color, border_alpha),
            (0, 0, int(self.width), int(self.height)),
            2,
            border_radius=8,
        )

        surface.blit(zone_surf, (self.hitbox.left, self.hitbox.top))


class GrabEffect:
    """
    Short-range grab that pulls opponent in for combo.
    Active for a brief window, then resolves (hit or whiff).
    """

    def __init__(
        self,
        x: float,
        y: float,
        direction: int,  # 1 for right, -1 for left
        grab_range: float = 80.0,
        grab_height: float = 60.0,
        duration: int = 12,  # frames of active grab
        damage: int = 10,
        pull_distance: float = 50.0,
        color: Tuple[int, int, int] = (200, 200, 50),
        owner_id: int = 0,
    ):
        self.x = x
        self.y = y
        self.direction = direction
        self.grab_range = grab_range
        self.grab_height = grab_height
        self.duration = duration
        self.damage = damage
        self.pull_distance = pull_distance
        self.color = color
        self.owner_id = owner_id

        self.alive = True
        self.age = 0
        self.grab_hit = False
        self.pull_target: Optional[Tuple[float, float]] = None

        # Hitbox extends in front of the character
        hx = self.x if direction == 1 else self.x - self.grab_range
        self.hitbox = pygame.Rect(
            int(hx),
            int(self.y - self.grab_height / 2),
            int(self.grab_range),
            int(self.grab_height),
        )

        # Visual particles
        self.particles: List[dict] = []
        self.max_particles = 20

    def get_hitbox(self) -> pygame.Rect:
        return self.hitbox

    def on_grab_hit(self, target_x: float, target_y: float):
        """Called when grab connects with a target."""
        self.grab_hit = True
        # Pull point: pull target toward the grabber
        pull_x = self.x + self.direction * self.pull_distance
        self.pull_target = (pull_x, self.y)

        # Impact particles
        for _ in range(12):
            self.particles.append({
                "x": target_x + random.uniform(-20, 20),
                "y": target_y + random.uniform(-20, 20),
                "vx": random.uniform(-3.0, 3.0),
                "vy": random.uniform(-5.0, -1.0),
                "life": random.randint(10, 25),
                "max_life": 25,
                "size": random.randint(3, 7),
                "color": (255, 255, 100),
            })

    def update(self):
        """Update grab effect."""
        if not self.alive:
            return

        self.age += 1

        if self.age >= self.duration:
            self.alive = False

        # Spawn grab visual particles while active
        if self.age % 2 == 0 and not self.grab_hit:
            grab_x = self.x + self.direction * self.grab_range * 0.5
            self.particles.append({
                "x": grab_x + random.uniform(-10, 10),
                "y": self.y + random.uniform(-self.grab_height / 3, self.grab_height / 3),
                "vx": -self.direction * random.uniform(1.0, 3.0),
                "vy": random.uniform(-1.0, 1.0),
                "life": random.randint(8, 15),
                "max_life": 15,
                "size": random.randint(2, 5),
                "color": self.color,
            })

        # Update particles
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1
        self.particles = [p for p in self.particles if p["life"] > 0]

    def draw(self, surface: pygame.Surface):
        """Draw grab effect."""
        # Draw particles
        for p in self.particles:
            alpha = p["life"] / max(p["max_life"], 1)
            size = max(1, int(p["size"] * alpha))
            color = tuple(int(c * alpha) for c in p["color"])
            pygame.draw.circle(surface, color, (int(p["x"]), int(p["y"])), size)

        if not self.alive:
            return

        # Grab range indicator (fading)
        alpha = 1.0 - (self.age / self.duration) * 0.5
        grab_color = tuple(int(c * alpha) for c in self.color)

        # Draw grab arc / hand shape
        grab_cx = self.x + self.direction * self.grab_range * 0.5
        grab_cy = self.y

        # Grabbing hand/claw shape
        spread = 15
        for i in range(3):
            angle_offset = (i - 1) * 0.3
            finger_x = grab_cx + self.direction * (self.grab_range * 0.3 + i * 5)
            finger_y = grab_cy + math.sin(angle_offset) * spread
            pygame.draw.circle(surface, grab_color, (int(finger_x), int(finger_y)), 5)

        # Curved lines suggesting grab
        for i in range(4):
            curve_y = grab_cy + (i - 1.5) * 10
            curve_x1 = self.x + self.direction * 5
            curve_x2 = grab_cx + self.direction * self.grab_range * 0.3
            # Use lines to approximate arc
            steps = 5
            points = []
            for s in range(steps + 1):
                t = s / steps
                px = curve_x1 + (curve_x2 - curve_x1) * t
                py = curve_y + math.sin(t * math.pi) * 8 * (1 - abs(t - 0.5) * 2)
                points.append((int(px), int(py)))
            if len(points) >= 2:
                pygame.draw.lines(surface, grab_color, False, points, 2)

        # Grab hit indicator
        if self.grab_hit and self.pull_target:
            # Exclamation mark
            ex_x = int(self.pull_target[0])
            ex_y = int(self.pull_target[1] - 40)
            pygame.draw.line(surface, (255, 255, 0), (ex_x, ex_y - 15), (ex_x, ex_y), 3)
            pygame.draw.circle(surface, (255, 255, 0), (ex_x, ex_y + 8), 3)

        # Hitbox debug (subtle)
        hitbox_surf = pygame.Surface((self.hitbox.width, self.hitbox.height), pygame.SRCALPHA)
        hitbox_alpha = int(30 * alpha)
        pygame.draw.rect(
            hitbox_surf,
            (*self.color, hitbox_alpha),
            (0, 0, self.hitbox.width, self.hitbox.height),
            1,
            border_radius=4,
        )
        surface.blit(hitbox_surf, (self.hitbox.left, self.hitbox.top))


class EffectManager:
    """
    Tracks all active effects, updates them, draws them, and cleans up expired ones.
    """

    def __init__(self):
        self.projectiles: List[Projectile] = []
        self.zones: List[ZoneEffect] = []
        self.grabs: List[GrabEffect] = []
        # Generic visual-only particles (explosions, sparks, etc.)
        self.visual_effects: List[dict] = []

    def add_projectile(self, projectile: Projectile):
        self.projectiles.append(projectile)

    def add_zone(self, zone: ZoneEffect):
        self.zones.append(zone)

    def add_grab(self, grab: GrabEffect):
        self.grabs.append(grab)

    def add_explosion(
        self,
        x: float,
        y: float,
        color: Tuple[int, int, int] = (255, 200, 50),
        particle_count: int = 20,
        lifetime: int = 30,
    ):
        """Add a one-shot explosion effect at a position."""
        particles = []
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2.0, 8.0)
            particles.append({
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed - 2.0,
                "life": random.randint(lifetime // 2, lifetime),
                "max_life": lifetime,
                "size": random.randint(3, 8),
                "color": (
                    min(255, color[0] + random.randint(-30, 30)),
                    min(255, color[1] + random.randint(-30, 30)),
                    max(0, color[2] + random.randint(-30, 30)),
                ),
            })
        self.visual_effects.append({
            "type": "explosion",
            "particles": particles,
            "alive": True,
        })

    def add_spark(
        self,
        x: float,
        y: float,
        color: Tuple[int, int, int] = (255, 255, 200),
        count: int = 10,
    ):
        """Add spark particles (e.g., on block)."""
        particles = []
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3.0, 10.0)
            particles.append({
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.randint(8, 20),
                "max_life": 20,
                "size": random.randint(1, 4),
                "color": color,
            })
        self.visual_effects.append({
            "type": "spark",
            "particles": particles,
            "alive": True,
        })

    def update(self):
        """Update all effects and clean up dead ones."""
        # Update projectiles
        for proj in self.projectiles:
            proj.update()
        self.projectiles = [p for p in self.projectiles if p.alive or p.particles]

        # Update zones
        for zone in self.zones:
            zone.update()
        self.zones = [z for z in self.zones if z.alive or z.particles]

        # Update grabs
        for grab in self.grabs:
            grab.update()
        self.grabs = [g for g in self.grabs if g.alive or g.particles]

        # Update visual effects
        for vfx in self.visual_effects:
            for p in vfx["particles"]:
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["vy"] += 0.15  # gravity
                p["life"] -= 1
            vfx["particles"] = [p for p in vfx["particles"] if p["life"] > 0]
            if not vfx["particles"]:
                vfx["alive"] = False

        self.visual_effects = [v for v in self.visual_effects if v["alive"]]

    def draw(self, surface: pygame.Surface):
        """Draw all effects."""
        # Draw zones first (background)
        for zone in self.zones:
            zone.draw(surface)

        # Draw projectiles
        for proj in self.projectiles:
            proj.draw(surface)

        # Draw grabs
        for grab in self.grabs:
            grab.draw(surface)

        # Draw visual effects
        for vfx in self.visual_effects:
            for p in vfx["particles"]:
                alpha = p["life"] / max(p["max_life"], 1)
                size = max(1, int(p["size"] * alpha))
                color = tuple(int(c * alpha) for c in p["color"])
                pygame.draw.circle(surface, color, (int(p["x"]), int(p["y"])), size)

    def get_projectiles_by_owner(self, owner_id: int) -> List[Projectile]:
        """Get all projectiles belonging to a specific owner."""
        return [p for p in self.projectiles if p.owner_id == owner_id]

    def get_zones_by_owner(self, owner_id: int) -> List[ZoneEffect]:
        """Get all zones belonging to a specific owner."""
        return [z for z in self.zones if z.owner_id == owner_id]

    def get_grabs_by_owner(self, owner_id: int) -> List[GrabEffect]:
        """Get all grabs belonging to a specific owner."""
        return [g for g in self.grabs if g.owner_id == owner_id]

    def clear_all(self):
        """Remove all effects."""
        self.projectiles.clear()
        self.zones.clear()
        self.grabs.clear()
        self.visual_effects.clear()

    def clear_by_owner(self, owner_id: int):
        """Remove all effects belonging to a specific owner."""
        self.projectiles = [p for p in self.projectiles if p.owner_id != owner_id]
        self.zones = [z for z in self.zones if z.owner_id != owner_id]
        self.grabs = [g for g in self.grabs if g.owner_id != owner_id]

    @property
    def active_count(self) -> int:
        """Total number of active effects."""
        return (
            len(self.projectiles)
            + len(self.zones)
            + len(self.grabs)
            + len(self.visual_effects)
        )


def draw_domain_overlay(
    surface: pygame.Surface,
    color: Tuple[int, int, int],
    timer: float,
    max_timer: float,
):
    """
    Creates a domain/super background color shift overlay.
    Used during super moves or ultimate abilities.

    Args:
        surface: The pygame surface to draw on.
        color: The dominant color of the domain/super effect.
        timer: Current timer value (decreases from max_timer to 0).
        max_timer: Maximum duration of the effect.
    """
    if timer <= 0:
        return

    progress = timer / max_timer  # 1.0 at start, 0.0 at end

    # Fade in for first 15%, sustain, fade out in last 30%
    if progress > 0.85:
        fade = (1.0 - progress) / 0.15  # fade in
    elif progress > 0.30:
        fade = 1.0  # full
    else:
        fade = progress / 0.30  # fade out

    fade = max(0.0, min(1.0, fade))

    # Background color wash
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    wash_alpha = int(80 * fade)
    overlay.fill((*color, wash_alpha))
    surface.blit(overlay, (0, 0))

    # Pulsing border
    border_thickness = int(20 * fade)
    if border_thickness > 0:
        pulse = 0.7 + 0.3 * math.sin(timer * 0.2)
        border_color = tuple(int(c * pulse) for c in color)
        border_alpha = int(180 * fade)
        border_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Top and bottom bars
        pygame.draw.rect(border_surf, (*border_color, border_alpha), (0, 0, SCREEN_WIDTH, border_thickness))
        pygame.draw.rect(
            border_surf,
            (*border_color, border_alpha),
            (0, SCREEN_HEIGHT - border_thickness, SCREEN_WIDTH, border_thickness),
        )
        # Left and right bars
        pygame.draw.rect(border_surf, (*border_color, border_alpha), (0, 0, border_thickness, SCREEN_HEIGHT))
        pygame.draw.rect(
            border_surf,
            (*border_color, border_alpha),
            (SCREEN_WIDTH - border_thickness, 0, border_thickness, SCREEN_HEIGHT),
        )
        surface.blit(border_surf, (0, 0))

    # Scan lines
    if fade > 0.1:
        scan_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for y in range(0, SCREEN_HEIGHT, 4):
            pygame.draw.line(scan_surf, (0, 0, 0, int(20 * fade)), (0, y), (SCREEN_WIDTH, y))
        surface.blit(scan_surf, (0, 0))

    # Energy particles floating
    num_particles = int(15 * fade)
    for i in range(num_particles):
        seed = int(timer * 3 + i * 137.5)  # deterministic pseudo-random
        px = (seed * 7 + i * 97) % SCREEN_WIDTH
        py = (seed * 13 + i * 53) % SCREEN_HEIGHT
        psize = 2 + (seed % 3)
        flicker = 0.5 + 0.5 * math.sin(timer * 0.3 + i)
        pcolor = tuple(int(c * flicker * fade) for c in color)
        pygame.draw.circle(surface, pcolor, (px, py), psize)

    # Corner accents
    corner_size = int(60 * fade)
    if corner_size > 5:
        accent_color = tuple(min(255, int(c * 1.3)) for c in color)
        accent_alpha = int(200 * fade)
        accent_surf = pygame.Surface((corner_size * 2, corner_size * 2), pygame.SRCALPHA)

        # Four corners with diamond shapes
        corners = [
            (corner_size, corner_size),  # top-left
            (SCREEN_WIDTH - corner_size, corner_size),  # top-right
            (corner_size, SCREEN_HEIGHT - corner_size),  # bottom-left
            (SCREEN_WIDTH - corner_size, SCREEN_HEIGHT - corner_size),  # bottom-right
        ]
        for cx, cy in corners:
            points = [
                (cx, cy - corner_size // 2),
                (cx + corner_size // 2, cy),
                (cx, cy + corner_size // 2),
                (cx - corner_size // 2, cy),
            ]
            pygame.draw.polygon(surface, (*accent_color, accent_alpha), points)


# --- Pre-built effect factory functions ---

def create_fireball(
    x: float, y: float, direction: int, owner_id: int = 0
) -> Projectile:
    """Create a standard red/orange fireball."""
    return Projectile(
        x=x, y=y, direction=direction,
        speed=7.0, damage=12, radius=18,
        color=(255, 80, 0), projectile_type="fireball",
        owner_id=owner_id,
    )


def create_hadouken(
    x: float, y: float, direction: int, owner_id: int = 0
) -> Projectile:
    """Create a blue hadouken-style projectile."""
    return Projectile(
        x=x, y=y, direction=direction,
        speed=8.0, damage=15, radius=22,
        color=(50, 100, 255), inner_color=(150, 200, 255),
        projectile_type="hadouken", owner_id=owner_id,
    )


def create_energy_ball(
    x: float, y: float, direction: int, owner_id: int = 0
) -> Projectile:
    """Create a purple energy ball."""
    return Projectile(
        x=x, y=y, direction=direction,
        speed=6.0, damage=18, radius=20,
        color=(180, 50, 255), inner_color=(220, 150, 255),
        projectile_type="energy", owner_id=owner_id,
    )


def create_fire_patch(
    x: float, y: float, owner_id: int = 0
) -> ZoneEffect:
    """Create a fire damage zone on the ground."""
    return ZoneEffect(
        x=x, y=y, width=180, height=60,
        duration=180, tick_interval=25, damage_per_tick=4,
        zone_type="fire", color=(255, 80, 0),
        owner_id=owner_id,
    )


def create_storm_cloud(
    x: float, y: float, owner_id: int = 0
) -> ZoneEffect:
    """Create a storm cloud zone that drops lightning."""
    return ZoneEffect(
        x=x, y=y - 80, width=200, height=160,
        duration=240, tick_interval=40, damage_per_tick=8,
        zone_type="storm", color=(100, 100, 200),
        owner_id=owner_id,
    )


def create_poison_cloud(
    x: float, y: float, owner_id: int = 0
) -> ZoneEffect:
    """Create a poison gas zone."""
    return ZoneEffect(
        x=x, y=y - 40, width=160, height=100,
        duration=200, tick_interval=30, damage_per_tick=3,
        zone_type="poison", color=(80, 200, 80),
        owner_id=owner_id,
    )


def create_command_grab(
    x: float, y: float, direction: int, owner_id: int = 0
) -> GrabEffect:
    """Create a command grab effect."""
    return GrabEffect(
        x=x, y=y, direction=direction,
        grab_range=90.0, grab_height=70.0,
        duration=14, damage=20, pull_distance=60.0,
        color=(255, 200, 50), owner_id=owner_id,
    )
