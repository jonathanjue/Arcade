"""
Meteor Defender - A fast-paced arcade survival game
Defend Earth from waves of meteors!
"""

import pygame
import random
import math
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()

# =============================================================================
# CONSTANTS
# =============================================================================

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
COLOR_BACKGROUND = (10, 10, 26)  # Deep Space Blue
COLOR_STARS = (255, 255, 255)
COLOR_PLAYER = (0, 255, 255)  # Cyan
COLOR_BULLET = (255, 255, 0)  # Yellow
COLOR_METEOR_SMALL = (255, 102, 0)  # Orange
COLOR_METEOR_MEDIUM = (255, 68, 0)  # Red-orange
COLOR_METEOR_LARGE = (204, 34, 0)  # Dark Red
COLOR_POWERUP_RAPID = (0, 255, 0)  # Green
COLOR_POWERUP_SHIELD = (0, 136, 255)  # Blue
COLOR_POWERUP_MULTISHOT = (170, 0, 255)  # Purple
COLOR_POWERUP_EXTRALIFE = (255, 0, 170)  # Pink
COLOR_TEXT = (255, 255, 255)
COLOR_SCORE = (255, 255, 0)
COLOR_LIVES = (255, 0, 0)
COLOR_TIME_SLOW = (100, 100, 255)  # Blue tint for time slow effect
COLOR_DASH = (255, 200, 100)  # Orange for dash effects

# Game settings
PLAYER_SPEED = 6
BULLET_SPEED = 10
BULLET_COOLDOWN = 250  # milliseconds (pistol default)
METEOR_BASE_SPEED = 2.0
POWERUP_SPEED = 2
POWERUP_DROP_CHANCE = 0.15

# Dash settings
DASH_SPEED = 20
DASH_DURATION = 0.15  # seconds
DASH_COOLDOWN = 4.0  # seconds

# Time slow settings
TIME_SLOW_MULTIPLIER = 0.3  # 30% speed
TIME_SLOW_DURATION = 4.0  # seconds
TIME_SLOW_COOLDOWN = 12.0  # seconds

# Meteor settings
class MeteorSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

METEOR_HEALTH = {
    MeteorSize.SMALL: 1,
    MeteorSize.MEDIUM: 2,
    MeteorSize.LARGE: 3
}

METEOR_POINTS = {
    MeteorSize.SMALL: 10,
    MeteorSize.MEDIUM: 25,
    MeteorSize.LARGE: 50
}

METEOR_SPEED_MULTIPLIER = {
    MeteorSize.SMALL: 1.5,
    MeteorSize.MEDIUM: 1.0,
    MeteorSize.LARGE: 0.7
}

METEOR_RADIUS = {
    MeteorSize.SMALL: 15,
    MeteorSize.MEDIUM: 25,
    MeteorSize.LARGE: 40
}

# Power-up types
class PowerUpType(Enum):
    RAPID_FIRE = 1
    SHIELD = 2
    MULTI_SHOT = 3
    EXTRA_LIFE = 4

POWERUP_COLORS = {
    PowerUpType.RAPID_FIRE: COLOR_POWERUP_RAPID,
    PowerUpType.SHIELD: COLOR_POWERUP_SHIELD,
    PowerUpType.MULTI_SHOT: COLOR_POWERUP_MULTISHOT,
    PowerUpType.EXTRA_LIFE: COLOR_POWERUP_EXTRALIFE
}

POWERUP_ICONS = {
    PowerUpType.RAPID_FIRE: "R",
    PowerUpType.SHIELD: "S",
    PowerUpType.MULTI_SHOT: "M",
    PowerUpType.EXTRA_LIFE: "+"
}

POWERUP_DURATION = 5000  # 5 seconds for timed power-ups

# Gun types for shop
class GunType(Enum):
    PISTOL = 1
    SMG = 2
    RIFLE = 3

GUN_NAMES = {
    GunType.PISTOL: "Pistol",
    GunType.SMG: "SMG",
    GunType.RIFLE: "Rifle"
}

GUN_COOLDOWNS = {
    GunType.PISTOL: 250,  # milliseconds
    GunType.SMG: 150,
    GunType.RIFLE: 80
}

GUN_PRICES = {
    GunType.PISTOL: 0,  # Starting gun, free
    GunType.SMG: 500,
    GunType.RIFLE: 1200
}

# Shop items
class ShopItemType(Enum):
    GUN_SMG = 1
    GUN_RIFLE = 2
    POWERUP_RAPID_FIRE = 3
    POWERUP_SHIELD = 4
    POWERUP_MULTI_SHOT = 5
    POWERUP_EXTRA_LIFE = 6

SHOP_ITEMS = {
    ShopItemType.GUN_SMG: {"name": "SMG (Fast Fire)", "price": 500, "description": "Faster fire rate"},
    ShopItemType.GUN_RIFLE: {"name": "Rifle (Rapid)", "price": 1200, "description": "Very fast fire rate"},
    ShopItemType.POWERUP_RAPID_FIRE: {"name": "Rapid Fire", "price": 200, "description": "5s of fast shooting"},
    ShopItemType.POWERUP_SHIELD: {"name": "Shield", "price": 300, "description": "Blocks one hit"},
    ShopItemType.POWERUP_MULTI_SHOT: {"name": "Multi-Shot", "price": 350, "description": "5s of 3-way fire"},
    ShopItemType.POWERUP_EXTRA_LIFE: {"name": "Extra Life", "price": 500, "description": "+1 Life (max 5)"}
}

# Game states
class GameState(Enum):
    TITLE_SCREEN = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    SHOP = 5


# =============================================================================
# STAR BACKGROUND
# =============================================================================

@dataclass
class Star:
    x: float
    y: float
    size: int
    brightness: int
    twinkle_speed: float
    twinkle_offset: float


class StarField:
    def __init__(self, num_stars: int = 100):
        self.stars: List[Star] = []
        for _ in range(num_stars):
            self.stars.append(Star(
                x=random.randint(0, SCREEN_WIDTH),
                y=random.randint(0, SCREEN_HEIGHT),
                size=random.randint(1, 3),
                brightness=random.randint(100, 255),
                twinkle_speed=random.uniform(0.02, 0.05),
                twinkle_offset=random.uniform(0, math.pi * 2)
            ))
        self.time = 0
    
    def update(self, dt: float):
        self.time += dt
        for star in self.stars:
            star.y += star.size * 0.3  # Parallax effect
            if star.y > SCREEN_HEIGHT:
                star.y = 0
                star.x = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, surface: pygame.Surface):
        for star in self.stars:
            twinkle = math.sin(self.time * star.twinkle_speed + star.twinkle_offset)
            alpha = int(star.brightness * (0.7 + 0.3 * twinkle))
            alpha = max(50, min(255, alpha))
            color = (alpha, alpha, alpha)
            pygame.draw.circle(surface, color, (int(star.x), int(star.y)), star.size)


# =============================================================================
# PARTICLE SYSTEM
# =============================================================================

@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    color: Tuple[int, int, int]
    life: float
    max_life: float
    size: float


class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []
    
    def create_explosion(self, x: float, y: float, color: Tuple[int, int, int], 
                         num_particles: int = 15, speed: float = 5.0):
        for _ in range(num_particles):
            angle = random.uniform(0, math.pi * 2)
            velocity = random.uniform(speed * 0.5, speed * 1.5)
            self.particles.append(Particle(
                x=x, y=y,
                vx=math.cos(angle) * velocity,
                vy=math.sin(angle) * velocity,
                color=color,
                life=random.uniform(0.3, 0.8),
                max_life=0.8,
                size=random.uniform(2, 5)
            ))
    
    def create_dash_trail(self, x: float, y: float, color: Tuple[int, int, int]):
        """Create trail particles for dash effect"""
        for _ in range(5):
            self.particles.append(Particle(
                x=x + random.uniform(-10, 10),
                y=y + random.uniform(-5, 5),
                vx=random.uniform(-1, 1),
                vy=random.uniform(-1, 1),
                color=color,
                life=random.uniform(0.2, 0.4),
                max_life=0.4,
                size=random.uniform(3, 6)
            ))
    
    def update(self, dt: float, time_multiplier: float = 1.0):
        for particle in self.particles[:]:
            particle.x += particle.vx * time_multiplier
            particle.y += particle.vy * time_multiplier
            particle.life -= dt
            particle.size *= 0.98
            if particle.life <= 0:
                self.particles.remove(particle)
    
    def draw(self, surface: pygame.Surface):
        for particle in self.particles:
            alpha = int(255 * (particle.life / particle.max_life))
            alpha = max(0, min(255, alpha))
            # Create a surface with per-pixel alpha
            size = max(1, int(particle.size))
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            color_with_alpha = (*particle.color, alpha)
            pygame.draw.circle(particle_surface, color_with_alpha, (size, size), size)
            surface.blit(particle_surface, (int(particle.x - size), int(particle.y - size)))


# =============================================================================
# PLAYER
# =============================================================================

class Player:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 35
        self.speed = PLAYER_SPEED
        self.last_shot = 0
        
        # Gun system
        self.current_gun = GunType.PISTOL
        self.owned_guns = {GunType.PISTOL}  # Start with pistol
        
        # Power-up states
        self.rapid_fire = False
        self.rapid_fire_end = 0
        self.shield = False
        self.multi_shot = False
        self.multi_shot_end = 0
        
        # Animation
        self.engine_flame = 0
        self.moving = False
        self.move_direction = 0  # -1 left, 0 none, 1 right
        
        # Dash system
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.dash_direction = 0
        self.dash_trail_positions: List[Tuple[float, float, float]] = []  # x, y, alpha
    
    @property
    def bullet_cooldown(self) -> int:
        return GUN_COOLDOWNS[self.current_gun]
    
    def update(self, dt: float, keys_pressed: pygame.key.ScancodeWrapper):
        # Update dash cooldown
        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= dt
        
        # Handle dashing
        if self.is_dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.is_dashing = False
            else:
                # Move quickly in dash direction
                self.x += self.dash_direction * DASH_SPEED
                # Add trail position
                self.dash_trail_positions.append((self.x, self.y, 1.0))
                # Keep player on screen
                self.x = max(self.width // 2, min(SCREEN_WIDTH - self.width // 2, self.x))
                return
        
        # Fade trail positions
        new_trail = []
        for tx, ty, alpha in self.dash_trail_positions:
            new_alpha = alpha - dt * 5
            if new_alpha > 0:
                new_trail.append((tx, ty, new_alpha))
        self.dash_trail_positions = new_trail
        
        self.moving = False
        self.move_direction = 0
        
        # Movement
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.x -= self.speed
            self.moving = True
            self.move_direction = -1
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.x += self.speed
            self.moving = True
            self.move_direction = 1
        
        # Keep player on screen
        self.x = max(self.width // 2, min(SCREEN_WIDTH - self.width // 2, self.x))
        
        # Update power-up timers
        current_time = pygame.time.get_ticks()
        if self.rapid_fire and current_time > self.rapid_fire_end:
            self.rapid_fire = False
        if self.multi_shot and current_time > self.multi_shot_end:
            self.multi_shot = False
        
        # Engine flame animation
        self.engine_flame += dt * 10
    
    def can_dash(self) -> bool:
        return self.dash_cooldown_timer <= 0 and not self.is_dashing and self.move_direction != 0
    
    def dash(self) -> bool:
        if self.can_dash():
            self.is_dashing = True
            self.dash_timer = DASH_DURATION
            self.dash_cooldown_timer = DASH_COOLDOWN
            self.dash_direction = self.move_direction
            return True
        return False
    
    def can_shoot(self) -> bool:
        current_time = pygame.time.get_ticks()
        cooldown = self.bullet_cooldown // 2 if self.rapid_fire else self.bullet_cooldown
        return current_time - self.last_shot >= cooldown
    
    def shoot(self) -> List['Bullet']:
        if not self.can_shoot():
            return []
        
        self.last_shot = pygame.time.get_ticks()
        bullets = []
        
        if self.multi_shot:
            # Create 3 bullets in a spread pattern
            for angle_offset in [-15, 0, 15]:
                angle = -90 + angle_offset  # -90 is straight up
                rad = math.radians(angle)
                vx = math.cos(rad) * BULLET_SPEED
                vy = math.sin(rad) * BULLET_SPEED
                bullets.append(Bullet(self.x, self.y - 20, vx, vy))
        else:
            bullets.append(Bullet(self.x, self.y - 20, 0, -BULLET_SPEED))
        
        return bullets
    
    def apply_powerup(self, powerup_type: PowerUpType):
        current_time = pygame.time.get_ticks()
        
        if powerup_type == PowerUpType.RAPID_FIRE:
            self.rapid_fire = True
            self.rapid_fire_end = current_time + POWERUP_DURATION
        elif powerup_type == PowerUpType.SHIELD:
            self.shield = True
        elif powerup_type == PowerUpType.MULTI_SHOT:
            self.multi_shot = True
            self.multi_shot_end = current_time + POWERUP_DURATION
        elif powerup_type == PowerUpType.EXTRA_LIFE:
            pass  # Handled by game
    
    def buy_gun(self, gun_type: GunType) -> bool:
        if gun_type not in self.owned_guns:
            self.owned_guns.add(gun_type)
            return True
        return False
    
    def equip_gun(self, gun_type: GunType) -> bool:
        if gun_type in self.owned_guns:
            self.current_gun = gun_type
            return True
        return False
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                          self.width, self.height)
    
    def draw(self, surface: pygame.Surface):
        # Draw dash trail
        for tx, ty, alpha in self.dash_trail_positions:
            trail_surface = pygame.Surface((30, 35), pygame.SRCALPHA)
            trail_alpha = int(alpha * 100)
            points = [
                (15, 5),      # Top point
                (0, 30),      # Bottom left
                (30, 30)      # Bottom right
            ]
            pygame.draw.polygon(trail_surface, (*COLOR_DASH, trail_alpha), points)
            surface.blit(trail_surface, (int(tx - 15), int(ty - 17)))
        
        # Draw shield if active
        if self.shield:
            shield_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (*COLOR_POWERUP_SHIELD, 100), (30, 30), 28)
            pygame.draw.circle(shield_surface, (*COLOR_POWERUP_SHIELD, 150), (30, 30), 28, 2)
            surface.blit(shield_surface, (int(self.x - 30), int(self.y - 30)))
        
        # Draw ship body (triangle pointing up)
        points = [
            (self.x, self.y - 20),      # Top point
            (self.x - 15, self.y + 15), # Bottom left
            (self.x + 15, self.y + 15)  # Bottom right
        ]
        
        # Change color if dashing
        ship_color = COLOR_DASH if self.is_dashing else COLOR_PLAYER
        pygame.draw.polygon(surface, ship_color, points)
        
        # Draw ship outline
        pygame.draw.polygon(surface, (255, 255, 255), points, 2)
        
        # Draw engine flame when moving
        if self.moving or self.is_dashing:
            flame_height = 8 + math.sin(self.engine_flame) * 4
            flame_points = [
                (self.x - 8, self.y + 15),
                (self.x, self.y + 15 + flame_height),
                (self.x + 8, self.y + 15)
            ]
            pygame.draw.polygon(surface, (255, 150, 0), flame_points)


# =============================================================================
# BULLET
# =============================================================================

class Bullet:
    def __init__(self, x: float, y: float, vx: float, vy: float):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.width = 4
        self.height = 12
        self.active = True
    
    def update(self, dt: float, time_multiplier: float = 1.0):
        self.x += self.vx * time_multiplier
        self.y += self.vy * time_multiplier
        
        # Deactivate if off screen
        if self.y < -self.height or self.y > SCREEN_HEIGHT + self.height:
            self.active = False
        if self.x < -self.width or self.x > SCREEN_WIDTH + self.width:
            self.active = False
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                          self.width, self.height)
    
    def draw(self, surface: pygame.Surface):
        # Draw bullet with trail effect
        trail_rect = pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height + 4)
        pygame.draw.rect(surface, (255, 200, 0), trail_rect)
        
        bullet_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                                  self.width, self.height)
        pygame.draw.rect(surface, COLOR_BULLET, bullet_rect)


# =============================================================================
# METEOR
# =============================================================================

class Meteor:
    def __init__(self, x: float, y: float, size: MeteorSize, speed_multiplier: float = 1.0):
        self.x = x
        self.y = y
        self.size = size
        self.radius = METEOR_RADIUS[size]
        self.health = METEOR_HEALTH[size]
        self.max_health = self.health
        
        # Speed based on size and wave multiplier
        base_speed = METEOR_SPEED_MULTIPLIER[size] * METEOR_BASE_SPEED * speed_multiplier
        self.vy = base_speed + random.uniform(-0.5, 0.5)
        self.vx = random.uniform(-0.5, 0.5)
        
        # Rotation
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
        
        # Generate irregular polygon shape
        self.num_vertices = random.randint(5, 8)
        self.vertices = self._generate_vertices()
        
        self.active = True
    
    def _generate_vertices(self) -> List[Tuple[float, float]]:
        vertices = []
        for i in range(self.num_vertices):
            angle = (i / self.num_vertices) * math.pi * 2
            # Random radius variation for irregular shape
            r = self.radius * random.uniform(0.7, 1.0)
            vertices.append((r * math.cos(angle), r * math.sin(angle)))
        return vertices
    
    def update(self, dt: float, time_multiplier: float = 1.0):
        self.x += self.vx * time_multiplier
        self.y += self.vy * time_multiplier
        self.rotation += self.rotation_speed * time_multiplier
        
        # Keep within horizontal bounds
        if self.x < self.radius:
            self.x = self.radius
            self.vx = abs(self.vx)
        elif self.x > SCREEN_WIDTH - self.radius:
            self.x = SCREEN_WIDTH - self.radius
            self.vx = -abs(self.vx)
    
    def hit(self) -> bool:
        """Returns True if meteor is destroyed"""
        self.health -= 1
        return self.health <= 0
    
    def split(self, speed_multiplier: float) -> List['Meteor']:
        """Create smaller meteors when destroyed"""
        new_meteors = []
        
        if self.size == MeteorSize.LARGE:
            new_size = MeteorSize.MEDIUM
        elif self.size == MeteorSize.MEDIUM:
            new_size = MeteorSize.SMALL
        else:
            return new_meteors  # Small meteors don't split
        
        # Create 2 smaller meteors
        for _ in range(2):
            offset_x = random.uniform(-20, 20)
            offset_y = random.uniform(-20, 20)
            new_meteor = Meteor(self.x + offset_x, self.y + offset_y, new_size, speed_multiplier)
            new_meteor.vx = random.uniform(-1.5, 1.5)
            new_meteor.vy = random.uniform(1, 2)
            new_meteors.append(new_meteor)
        
        return new_meteors
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)
    
    def get_color(self) -> Tuple[int, int, int]:
        if self.size == MeteorSize.SMALL:
            return COLOR_METEOR_SMALL
        elif self.size == MeteorSize.MEDIUM:
            return COLOR_METEOR_MEDIUM
        return COLOR_METEOR_LARGE
    
    def draw(self, surface: pygame.Surface):
        # Calculate rotated vertices
        rotated_vertices = []
        angle_rad = math.radians(self.rotation)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        for vx, vy in self.vertices:
            rx = vx * cos_a - vy * sin_a
            ry = vx * sin_a + vy * cos_a
            rotated_vertices.append((self.x + rx, self.y + ry))
        
        # Draw meteor body
        pygame.draw.polygon(surface, self.get_color(), rotated_vertices)
        pygame.draw.polygon(surface, (100, 100, 100), rotated_vertices, 2)
        
        # Draw damage cracks if damaged
        if self.health < self.max_health:
            damage_ratio = self.health / self.max_health
            crack_color = (50, 50, 50)
            num_cracks = int((1 - damage_ratio) * 3) + 1
            for i in range(num_cracks):
                angle = (i / num_cracks) * math.pi * 2 + self.rotation * 0.01
                start = (self.x + math.cos(angle) * self.radius * 0.3,
                        self.y + math.sin(angle) * self.radius * 0.3)
                end = (self.x + math.cos(angle) * self.radius * 0.8,
                      self.y + math.sin(angle) * self.radius * 0.8)
                pygame.draw.line(surface, crack_color, start, end, 2)


# =============================================================================
# POWER-UP
# =============================================================================

class PowerUp:
    def __init__(self, x: float, y: float, powerup_type: PowerUpType):
        self.x = x
        self.y = y
        self.type = powerup_type
        self.radius = 15
        self.vy = POWERUP_SPEED
        self.active = True
        self.pulse_time = random.uniform(0, math.pi * 2)
    
    def update(self, dt: float, time_multiplier: float = 1.0):
        self.y += self.vy * time_multiplier
        self.pulse_time += dt * 5 * time_multiplier
        
        if self.y > SCREEN_HEIGHT + self.radius:
            self.active = False
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)
    
    def draw(self, surface: pygame.Surface):
        # Pulsing glow effect
        pulse = 0.8 + 0.2 * math.sin(self.pulse_time)
        glow_radius = int(self.radius * 1.3 * pulse)
        
        # Draw glow
        glow_surface = pygame.Surface((glow_radius * 2 + 10, glow_radius * 2 + 10), pygame.SRCALPHA)
        color = POWERUP_COLORS[self.type]
        pygame.draw.circle(glow_surface, (*color, 50), 
                          (glow_radius + 5, glow_radius + 5), glow_radius)
        surface.blit(glow_surface, (int(self.x - glow_radius - 5), int(self.y - glow_radius - 5)))
        
        # Draw main circle
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius, 2)
        
        # Draw icon
        font = pygame.font.Font(None, 24)
        icon_text = POWERUP_ICONS[self.type]
        text_surface = font.render(icon_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(text_surface, text_rect)


# =============================================================================
# GAME
# =============================================================================

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Meteor Defender")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        
        self.state = GameState.TITLE_SCREEN
        self.high_score = 0
        
        self.reset_game()
    
    def reset_game(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.bullets: List[Bullet] = []
        self.meteors: List[Meteor] = []
        self.powerups: List[PowerUp] = []
        self.particles = ParticleSystem()
        self.star_field = StarField()
        
        self.score = 0
        self.lives = 3
        self.wave = 1
        self.meteors_destroyed = 0
        self.meteors_per_wave = 10
        
        # Difficulty scaling
        self.spawn_timer = 0
        self.spawn_delay = 2.0  # Seconds between meteor spawns
        self.speed_multiplier = 1.0
        
        # Time slow system
        self.time_slow_active = False
        self.time_slow_timer = 0
        self.time_slow_cooldown_timer = 0
        
        # Shop state
        self.shop_selected = 0
        
        self.running = True
    
    @property
    def time_multiplier(self) -> float:
        """Returns the current time multiplier for game objects"""
        if self.time_slow_active:
            return TIME_SLOW_MULTIPLIER
        return 1.0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.TITLE_SCREEN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_q:
                        self.running = False
                
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_f:
                        # Shoot with F key
                        new_bullets = self.player.shoot()
                        self.bullets.extend(new_bullets)
                    elif event.key == pygame.K_SPACE:
                        # Dash with Space
                        self.player.dash()
                    elif event.key == pygame.K_h:
                        # Time slow
                        self.activate_time_slow()
                    elif event.key == pygame.K_t:
                        # Open shop
                        self.state = GameState.SHOP
                    elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.state = GameState.PAUSED
                
                elif self.state == GameState.SHOP:
                    if event.key == pygame.K_t or event.key == pygame.K_ESCAPE:
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_UP:
                        self.shop_selected = max(0, self.shop_selected - 1)
                    elif event.key == pygame.K_DOWN:
                        self.shop_selected = min(len(ShopItemType) - 1, self.shop_selected + 1)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.buy_shop_item(list(ShopItemType)[self.shop_selected])
                
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_q:
                        self.state = GameState.TITLE_SCREEN
                
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_q:
                        self.state = GameState.TITLE_SCREEN
            
            # Mouse button for shooting
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.PLAYING:
                    if event.button == 1:  # Left mouse button
                        new_bullets = self.player.shoot()
                        self.bullets.extend(new_bullets)
    
    def activate_time_slow(self):
        """Activate time slow if cooldown is ready"""
        if self.time_slow_cooldown_timer <= 0 and not self.time_slow_active:
            self.time_slow_active = True
            self.time_slow_timer = TIME_SLOW_DURATION
            self.time_slow_cooldown_timer = TIME_SLOW_COOLDOWN
    
    def buy_shop_item(self, item_type: ShopItemType) -> bool:
        """Attempt to buy an item from the shop"""
        item = SHOP_ITEMS[item_type]
        price = item["price"]
        
        if self.score < price:
            return False
        
        # Check what type of item it is
        if item_type == ShopItemType.GUN_SMG:
            if GunType.SMG in self.player.owned_guns:
                return False  # Already owned
            self.score -= price
            self.player.buy_gun(GunType.SMG)
            self.player.equip_gun(GunType.SMG)
        elif item_type == ShopItemType.GUN_RIFLE:
            if GunType.RIFLE in self.player.owned_guns:
                return False  # Already owned
            self.score -= price
            self.player.buy_gun(GunType.RIFLE)
            self.player.equip_gun(GunType.RIFLE)
        elif item_type == ShopItemType.POWERUP_RAPID_FIRE:
            self.score -= price
            self.player.apply_powerup(PowerUpType.RAPID_FIRE)
        elif item_type == ShopItemType.POWERUP_SHIELD:
            self.score -= price
            self.player.apply_powerup(PowerUpType.SHIELD)
        elif item_type == ShopItemType.POWERUP_MULTI_SHOT:
            self.score -= price
            self.player.apply_powerup(PowerUpType.MULTI_SHOT)
        elif item_type == ShopItemType.POWERUP_EXTRA_LIFE:
            if self.lives >= 5:
                return False  # Already at max lives
            self.score -= price
            self.lives = min(5, self.lives + 1)
        
        return True
    
    def update(self, dt: float):
        if self.state not in [GameState.PLAYING, GameState.SHOP]:
            self.star_field.update(dt)
            return
        
        # Update star field
        self.star_field.update(dt)
        
        # If in shop, don't update game objects
        if self.state == GameState.SHOP:
            return
        
        # Update time slow
        if self.time_slow_active:
            self.time_slow_timer -= dt
            if self.time_slow_timer <= 0:
                self.time_slow_active = False
        
        if self.time_slow_cooldown_timer > 0:
            self.time_slow_cooldown_timer -= dt
        
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Update player (player always moves at normal speed)
        self.player.update(dt, keys)
        
        # Continuous shooting while F or left mouse is held
        if keys[pygame.K_f] or pygame.mouse.get_pressed()[0]:
            new_bullets = self.player.shoot()
            self.bullets.extend(new_bullets)
        
        # Create dash trail particles
        if self.player.is_dashing:
            self.particles.create_dash_trail(self.player.x, self.player.y, COLOR_DASH)
        
        # Update bullets (affected by time slow)
        for bullet in self.bullets[:]:
            bullet.update(dt, self.time_multiplier)
            if not bullet.active:
                self.bullets.remove(bullet)
        
        # Update meteors (affected by time slow)
        for meteor in self.meteors[:]:
            meteor.update(dt, self.time_multiplier)
            
            # Check if meteor reached bottom
            if meteor.y > SCREEN_HEIGHT + meteor.radius:
                self.meteors.remove(meteor)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over()
                    return
        
        # Update power-ups (affected by time slow)
        for powerup in self.powerups[:]:
            powerup.update(dt, self.time_multiplier)
            if not powerup.active:
                self.powerups.remove(powerup)
        
        # Update particles
        self.particles.update(dt, self.time_multiplier)
        
        # Spawn meteors (affected by time slow)
        self.spawn_timer += dt * self.time_multiplier
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            self.spawn_meteor()
        
        # Check collisions
        self.check_collisions()
        
        # Check wave completion
        if self.meteors_destroyed >= self.meteors_per_wave:
            self.next_wave()
    
    def spawn_meteor(self):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = -50
        
        # Determine meteor size based on wave
        large_chance = min(0.3, self.wave * 0.02)
        medium_chance = min(0.5, 0.2 + self.wave * 0.03)
        
        rand = random.random()
        if rand < large_chance:
            size = MeteorSize.LARGE
        elif rand < large_chance + medium_chance:
            size = MeteorSize.MEDIUM
        else:
            size = MeteorSize.SMALL
        
        self.meteors.append(Meteor(x, y, size, self.speed_multiplier))
    
    def check_collisions(self):
        # Bullet-Meteor collisions
        for bullet in self.bullets[:]:
            if not bullet.active:
                continue
            
            bullet_rect = bullet.get_rect()
            
            for meteor in self.meteors[:]:
                if not meteor.active:
                    continue
                
                # Simple circle-rect collision
                meteor_rect = meteor.get_rect()
                if bullet_rect.colliderect(meteor_rect):
                    bullet.active = False
                    self.bullets.remove(bullet)
                    
                    if meteor.hit():
                        # Meteor destroyed
                        self.score += METEOR_POINTS[meteor.size]
                        self.meteors_destroyed += 1
                        
                        # Create explosion
                        self.particles.create_explosion(
                            meteor.x, meteor.y, meteor.get_color(),
                            num_particles=20, speed=6
                        )
                        
                        # Split meteor
                        new_meteors = meteor.split(self.speed_multiplier)
                        self.meteors.extend(new_meteors)
                        
                        # Maybe drop power-up
                        if random.random() < POWERUP_DROP_CHANCE:
                            self.spawn_powerup(meteor.x, meteor.y)
                        
                        self.meteors.remove(meteor)
                    else:
                        # Meteor damaged - small particle effect
                        self.particles.create_explosion(
                            bullet.x, bullet.y, (255, 200, 0),
                            num_particles=5, speed=3
                        )
                    break
        
        # Player-PowerUp collisions
        player_rect = self.player.get_rect()
        
        for powerup in self.powerups[:]:
            if player_rect.colliderect(powerup.get_rect()):
                self.score += 20  # Points for collecting power-up
                
                if powerup.type == PowerUpType.EXTRA_LIFE:
                    self.lives = min(5, self.lives + 1)  # Max 5 lives
                else:
                    self.player.apply_powerup(powerup.type)
                
                self.powerups.remove(powerup)
        
        # Player-Meteor collisions (with shield)
        if self.player.shield:
            for meteor in self.meteors[:]:
                dist = math.sqrt((self.player.x - meteor.x) ** 2 + 
                               (self.player.y - meteor.y) ** 2)
                if dist < meteor.radius + 25:  # Shield radius
                    self.player.shield = False
                    self.particles.create_explosion(
                        meteor.x, meteor.y, meteor.get_color(),
                        num_particles=20, speed=6
                    )
                    self.meteors.remove(meteor)
                    break
    
    def spawn_powerup(self, x: float, y: float):
        # Weight power-up types
        weights = {
            PowerUpType.RAPID_FIRE: 30,
            PowerUpType.SHIELD: 25,
            PowerUpType.MULTI_SHOT: 25,
            PowerUpType.EXTRA_LIFE: 10  # Rare
        }
        
        total = sum(weights.values())
        rand = random.randint(1, total)
        cumulative = 0
        
        for powerup_type, weight in weights.items():
            cumulative += weight
            if rand <= cumulative:
                self.powerups.append(PowerUp(x, y, powerup_type))
                break
    
    def next_wave(self):
        self.wave += 1
        self.meteors_destroyed = 0
        self.meteors_per_wave += 5
        
        # Increase difficulty
        self.spawn_delay = max(0.5, 2.0 - (self.wave * 0.1))
        self.speed_multiplier = 1.0 + (self.wave * 0.1)
        
        # Wave completion bonus
        self.score += self.wave * 100
    
    def game_over(self):
        self.state = GameState.GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score
    
    def draw(self):
        # Clear screen
        self.screen.fill(COLOR_BACKGROUND)
        
        # Draw time slow border effect
        if self.time_slow_active:
            # Draw blue tinted border
            border_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, (*COLOR_TIME_SLOW, 30), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(border_surface, (0, 0))
            # Draw border
            pygame.draw.rect(self.screen, COLOR_TIME_SLOW, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)
        
        # Draw star field (always)
        self.star_field.draw(self.screen)
        
        if self.state == GameState.TITLE_SCREEN:
            self.draw_title_screen()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.SHOP:
            self.draw_game()
            self.draw_shop_overlay()
        elif self.state == GameState.PAUSED:
            self.draw_game()
            self.draw_pause_overlay()
        elif self.state == GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over_overlay()
        
        pygame.display.flip()
    
    def draw_title_screen(self):
        # Title
        title_text = self.font_large.render("METEOR DEFENDER", True, COLOR_PLAYER)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_small.render("Defend Earth from the meteor storm!", True, COLOR_TEXT)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # High score
        if self.high_score > 0:
            hs_text = self.font_medium.render(f"High Score: {self.high_score}", True, COLOR_SCORE)
            hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, 270))
            self.screen.blit(hs_text, hs_rect)
        
        # Controls
        controls = [
            "Controls:",
            "A/D or Arrow Keys - Move",
            "F or Left Mouse - Shoot",
            "Space - Dash (in move direction)",
            "H - Time Slow",
            "T - Open Shop",
            "P/Escape - Pause",
            "",
            "Press SPACE to Start"
        ]
        
        y_offset = 330
        for line in controls:
            color = COLOR_SCORE if "SPACE" in line else COLOR_TEXT
            text = self.font_small.render(line, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30
    
    def draw_game(self):
        # Draw game objects
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        for meteor in self.meteors:
            meteor.draw(self.screen)
        
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        self.player.draw(self.screen)
        self.particles.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
    
    def draw_ui(self):
        # Score
        score_text = self.font_small.render(f"SCORE: {self.score}", True, COLOR_SCORE)
        self.screen.blit(score_text, (20, 20))
        
        # Wave
        wave_text = self.font_small.render(f"WAVE {self.wave}", True, COLOR_TEXT)
        wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(wave_text, wave_rect)
        
        # Lives (hearts)
        for i in range(self.lives):
            heart_x = SCREEN_WIDTH - 40 - (i * 35)
            self.draw_heart(heart_x, 25, 12)
        
        # Current gun indicator
        gun_text = self.font_tiny.render(f"Gun: {GUN_NAMES[self.player.current_gun]}", True, COLOR_TEXT)
        self.screen.blit(gun_text, (20, 50))
        
        # Dash cooldown
        y_offset = 75
        if self.player.dash_cooldown_timer > 0:
            dash_ready = max(0, self.player.dash_cooldown_timer)
            dash_text = self.font_tiny.render(f"Dash: {dash_ready:.1f}s", True, (150, 150, 150))
        else:
            dash_text = self.font_tiny.render("Dash: READY", True, COLOR_DASH)
        self.screen.blit(dash_text, (20, y_offset))
        y_offset += 20
        
        # Time slow cooldown
        if self.time_slow_active:
            time_text = self.font_tiny.render(f"Time Slow: {self.time_slow_timer:.1f}s", True, COLOR_TIME_SLOW)
        elif self.time_slow_cooldown_timer > 0:
            time_text = self.font_tiny.render(f"Time Slow: {self.time_slow_cooldown_timer:.1f}s", True, (150, 150, 150))
        else:
            time_text = self.font_tiny.render("Time Slow: READY", True, COLOR_TIME_SLOW)
        self.screen.blit(time_text, (20, y_offset))
        y_offset += 20
        
        # Active power-ups
        powerup_y = y_offset + 10
        if self.player.rapid_fire:
            self.draw_powerup_indicator("RAPID FIRE", COLOR_POWERUP_RAPID, powerup_y)
            powerup_y += 25
        if self.player.shield:
            self.draw_powerup_indicator("SHIELD", COLOR_POWERUP_SHIELD, powerup_y)
            powerup_y += 25
        if self.player.multi_shot:
            self.draw_powerup_indicator("MULTI-SHOT", COLOR_POWERUP_MULTISHOT, powerup_y)
    
    def draw_heart(self, x: float, y: float, size: float):
        """Draw a heart shape"""
        # Two circles for top of heart
        pygame.draw.circle(self.screen, COLOR_LIVES, (int(x - size/2), int(y)), int(size/2))
        pygame.draw.circle(self.screen, COLOR_LIVES, (int(x + size/2), int(y)), int(size/2))
        # Triangle for bottom of heart
        points = [
            (x - size, y),
            (x + size, y),
            (x, y + size)
        ]
        pygame.draw.polygon(self.screen, COLOR_LIVES, points)
    
    def draw_powerup_indicator(self, text: str, color: Tuple[int, int, int], y: int):
        indicator = self.font_small.render(text, True, color)
        self.screen.blit(indicator, (20, y))
    
    def draw_shop_overlay(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Shop title
        title_text = self.font_large.render("SHOP", True, COLOR_SCORE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
        self.screen.blit(title_text, title_rect)
        
        # Current score
        score_text = self.font_medium.render(f"Score: {self.score}", True, COLOR_SCORE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 110))
        self.screen.blit(score_text, score_rect)
        
        # Shop items
        y_offset = 160
        item_list = list(ShopItemType)
        
        for i, item_type in enumerate(item_list):
            item = SHOP_ITEMS[item_type]
            is_selected = i == self.shop_selected
            
            # Check if item can be bought
            can_buy = self.score >= item["price"]
            
            # Check if gun is already owned
            already_owned = False
            if item_type == ShopItemType.GUN_SMG and GunType.SMG in self.player.owned_guns:
                already_owned = True
                can_buy = False
            elif item_type == ShopItemType.GUN_RIFLE and GunType.RIFLE in self.player.owned_guns:
                already_owned = True
                can_buy = False
            
            # Check if at max lives
            if item_type == ShopItemType.POWERUP_EXTRA_LIFE and self.lives >= 5:
                can_buy = False
            
            # Draw selection highlight
            if is_selected:
                highlight_rect = pygame.Rect(150, y_offset - 5, 500, 50)
                pygame.draw.rect(self.screen, (50, 50, 80), highlight_rect, border_radius=5)
            
            # Item name and price
            if already_owned:
                color = (100, 100, 100)
                status = " [OWNED]"
            elif can_buy:
                color = COLOR_TEXT if not is_selected else COLOR_SCORE
                status = ""
            else:
                color = (150, 100, 100)
                status = ""
            
            name_text = self.font_small.render(f"{item['name']}{status}", True, color)
            self.screen.blit(name_text, (170, y_offset))
            
            price_text = self.font_small.render(f"{item['price']} pts", True, color)
            self.screen.blit(price_text, (500, y_offset))
            
            # Description
            desc_text = self.font_tiny.render(item['description'], True, (150, 150, 150))
            self.screen.blit(desc_text, (170, y_offset + 22))
            
            y_offset += 55
        
        # Instructions
        inst_text = self.font_tiny.render("UP/DOWN: Select | ENTER: Buy | T/ESC: Close", True, COLOR_TEXT)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        self.screen.blit(inst_text, inst_rect)
        
        # Current gun display
        gun_text = self.font_small.render(f"Equipped: {GUN_NAMES[self.player.current_gun]}", True, COLOR_PLAYER)
        gun_rect = gun_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        self.screen.blit(gun_text, gun_rect)
    
    def draw_pause_overlay(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, COLOR_TEXT)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        resume_text = self.font_small.render("Press P or ESC to Resume", True, COLOR_TEXT)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(resume_text, resume_rect)
        
        quit_text = self.font_small.render("Press Q to Quit to Title", True, COLOR_TEXT)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(quit_text, quit_rect)
    
    def draw_game_over_overlay(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        go_text = self.font_large.render("GAME OVER", True, COLOR_LIVES)
        go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(go_text, go_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, COLOR_SCORE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)
        
        # High score notification
        if self.score >= self.high_score and self.score > 0:
            hs_text = self.font_small.render("NEW HIGH SCORE!", True, COLOR_SCORE)
            hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(hs_text, hs_rect)
        
        # Wave reached
        wave_text = self.font_small.render(f"Wave Reached: {self.wave}", True, COLOR_TEXT)
        wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(wave_text, wave_rect)
        
        # Instructions
        restart_text = self.font_small.render("Press R to Restart", True, COLOR_TEXT)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(restart_text, restart_rect)
        
        quit_text = self.font_small.render("Press Q to Quit to Title", True, COLOR_TEXT)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160))
        self.screen.blit(quit_text, quit_rect)
    
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    game = Game()
    game.run()
