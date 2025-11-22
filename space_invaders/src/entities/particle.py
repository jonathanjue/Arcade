"""
Particle System Module
Provides visual effects for explosions, impacts, and sparks in the Space Invaders game.
"""

import pygame
import random
import math
from typing import List, Optional, Tuple
from src.base.game_object import GameObject
from config.constants import *


class ParticleType:
    """Constants for different particle types."""
    EXPLOSION = "explosion"
    IMPACT = "impact"
    SPARK = "spark"


class Particle(GameObject):
    """
    Individual particle for visual effects.
    
    Attributes:
        particle_type (str): Type of particle (explosion, impact, spark)
        lifetime (float): Total lifetime in seconds
        current_lifetime (float): Current lifetime remaining
        original_color (tuple): Original color of the particle
        color (tuple): Current color with alpha effect
        size (int): Size of the particle
        alpha (int): Alpha value for fade-out effect
        rotation (float): Rotation angle for the particle
        rotation_speed (float): Speed of rotation
        gravity (float): Gravity effect on the particle
        friction (float): Friction applied to velocity
    """
    
    def __init__(self, x: float, y: float, particle_type: str, color: Tuple[int, int, int]):
        """Initialize a particle with the specified type and color."""
        # Small size for particles
        size = random.randint(2, 6)
        super().__init__(x, y, size, size)
        
        self.particle_type = particle_type
        self.lifetime = 1.0
        self.current_lifetime = self.lifetime
        self.original_color = color
        self.color = color
        self.alpha = 255
        self.rotation = 0.0
        self.rotation_speed = random.uniform(-180, 180)  # degrees per second
        
        # Physics properties
        self.gravity = 0.0
        self.friction = 0.98
        
        # Initialize velocity and lifetime based on type
        self._initialize_particle_type()
        
    def _initialize_particle_type(self) -> None:
        """Initialize particle properties based on its type."""
        if self.particle_type == ParticleType.EXPLOSION:
            self.lifetime = EXPLOSION_PARTICLE_LIFETIME
            self.current_lifetime = self.lifetime
            
            # Radial explosion movement
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(EXPLOSION_PARTICLE_SPEED * 0.5, EXPLOSION_PARTICLE_SPEED * 1.5)
            self.velocity_x = math.cos(angle) * speed
            self.velocity_y = math.sin(angle) * speed
            
            # Explosion particles have gravity and larger size
            self.gravity = 200
            self.size = random.randint(3, 8)
            self.width = self.size
            self.height = self.size
            
        elif self.particle_type == ParticleType.IMPACT:
            self.lifetime = IMPACT_PARTICLE_LIFETIME
            self.current_lifetime = self.lifetime
            
            # Impact particles have less movement
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(IMPACT_PARTICLE_SPEED * 0.3, IMPACT_PARTICLE_SPEED * 0.8)
            self.velocity_x = math.cos(angle) * speed
            self.velocity_y = math.sin(angle) * speed
            
            # Impact particles have minimal gravity
            self.gravity = 50
            self.size = random.randint(1, 4)
            self.width = self.size
            self.height = self.size
            
        elif self.particle_type == ParticleType.SPARK:
            self.lifetime = 0.3  # Very short lifetime
            self.current_lifetime = self.lifetime
            
            # Sparks move very fast
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(150, 300)
            self.velocity_x = math.cos(angle) * speed
            self.velocity_y = math.sin(angle) * speed
            
            # Sparks have strong gravity
            self.gravity = 300
            self.size = random.randint(1, 3)
            self.width = self.size
            self.height = self.size
            
        self.current_lifetime = self.lifetime
        
    def update(self, dt: float) -> None:
        """Update the particle's state."""
        if not self.active:
            return
            
        # Update lifetime
        self.current_lifetime -= dt
        if self.current_lifetime <= 0:
            self.active = False
            return
            
        # Update position with velocity
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Apply gravity
        if self.gravity > 0:
            self.velocity_y += self.gravity * dt
            
        # Apply friction
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        
        # Update rotation
        self.rotation += self.rotation_speed * dt
        
        # Update alpha for fade-out effect
        life_ratio = self.current_lifetime / self.lifetime
        self.alpha = int(255 * life_ratio)
        
        # Create fade color with alpha
        r, g, b = self.original_color
        self.color = (r, g, b)
        
        # Update size based on lifetime (shrink over time)
        size_multiplier = life_ratio
        self.width = max(1, int(self.size * size_multiplier))
        self.height = max(1, int(self.size * size_multiplier))
        
    def render(self, surface: pygame.Surface) -> None:
        """Render the particle."""
        if not self.active or self.alpha <= 0:
            return
            
        # Create a temporary surface for alpha rendering
        particle_surface = pygame.Surface((self.width, self.height))
        particle_surface.set_alpha(self.alpha)
        particle_surface.fill(self.color)
        
        # Rotate the particle if it has significant rotation
        if abs(self.rotation) > 5:
            rotated_surface = pygame.transform.rotate(particle_surface, self.rotation)
            surface.blit(rotated_surface, (self.x, self.y))
        else:
            surface.blit(particle_surface, (self.x, self.y))
            
    def is_dead(self) -> bool:
        """Check if the particle is dead and should be removed."""
        return not self.active or self.current_lifetime <= 0


class ParticlePool:
    """Object pool for efficient particle management."""
    
    def __init__(self, initial_size: int = 100):
        """Initialize the particle pool."""
        self.pool: List[Particle] = []
        self.active_particles: List[Particle] = []
        
        # Pre-populate the pool
        for _ in range(initial_size):
            self.pool.append(Particle(0, 0, ParticleType.EXPLOSION, WHITE))
            
    def get_particle(self, x: float, y: float, particle_type: str, color: Tuple[int, int, int]) -> Particle:
        """Get a particle from the pool or create a new one."""
        if self.pool:
            particle = self.pool.pop()
            # Reset particle properties
            particle.x = x
            particle.y = y
            particle.particle_type = particle_type
            particle.original_color = color
            particle.color = color
            particle.active = True
            particle.rotation = 0.0
            particle._initialize_particle_type()
        else:
            particle = Particle(x, y, particle_type, color)
            
        self.active_particles.append(particle)
        return particle
        
    def release_particle(self, particle: Particle) -> None:
        """Return a particle to the pool."""
        if particle in self.active_particles:
            self.active_particles.remove(particle)
            particle.active = False
            self.pool.append(particle)
            
    def cleanup_dead_particles(self) -> None:
        """Remove and recycle dead particles."""
        dead_particles = [p for p in self.active_particles if p.is_dead()]
        for particle in dead_particles:
            self.release_particle(particle)
            
    def get_active_count(self) -> int:
        """Get the number of active particles."""
        return len(self.active_particles)


class ParticleSystem:
    """
    Manages all particle effects in the game.
    
    Attributes:
        pool (ParticlePool): Particle object pool for performance
        particles (List[Particle]): List of all active particles
    """
    
    def __init__(self):
        """Initialize the particle system."""
        self.pool = ParticlePool(initial_size=200)
        self.particles = []
        
        # Color schemes for different effects
        self.explosion_colors = [
            RED, YELLOW, ORANGE if ORANGE in globals() else (255, 165, 0), WHITE
        ]
        self.impact_colors = [
            WHITE, LIGHT_GRAY, GRAY
        ]
        self.spark_colors = [
            YELLOW, WHITE, CYAN, BLUE
        ]
        
    def create_explosion(self, x: float, y: float, intensity: float = 1.0) -> None:
        """Create an explosion effect at the specified position."""
        count = int(EXPLOSION_PARTICLE_COUNT * intensity)
        
        for _ in range(count):
            color = random.choice(self.explosion_colors)
            particle = self.pool.get_particle(x, y, ParticleType.EXPLOSION, color)
            self.particles.append(particle)
            
    def create_impact(self, x: float, y: float, intensity: float = 1.0) -> None:
        """Create an impact effect at the specified position."""
        count = int(IMPACT_PARTICLE_COUNT * intensity)
        
        for _ in range(count):
            color = random.choice(self.impact_colors)
            particle = self.pool.get_particle(x, y, ParticleType.IMPACT, color)
            self.particles.append(particle)
            
    def create_spark(self, x: float, y: float, direction: Tuple[float, float] = None, intensity: float = 1.0) -> None:
        """Create a spark effect at the specified position."""
        spark_count = int(3 * intensity)
        
        for _ in range(spark_count):
            color = random.choice(self.spark_colors)
            particle = self.pool.get_particle(x, y, ParticleType.SPARK, color)
            
            # Override default velocity if direction is provided
            if direction:
                speed = random.uniform(100, 200)
                particle.velocity_x = direction[0] * speed
                particle.velocity_y = direction[1] * speed
                
            self.particles.append(particle)
            
    def create_bullet_impact(self, x: float, y: float, is_player_bullet: bool = True) -> None:
        """Create impact effect when bullet hits something."""
        if is_player_bullet:
            # Player bullets create brighter impacts
            self.create_impact(x, y, intensity=1.5)
        else:
            # Enemy bullets create normal impacts
            self.create_impact(x, y, intensity=1.0)
            
    def create_alien_explosion(self, x: float, y: float, alien_row: int) -> None:
        """Create explosion effect when alien is destroyed."""
        # Color explosion based on alien row
        if alien_row == 0:  # Top row
            explosion_colors = [MAGENTA, WHITE, CYAN]
        elif alien_row == 1:  # Middle row
            explosion_colors = [CYAN, WHITE, YELLOW]
        else:  # Bottom row
            explosion_colors = [YELLOW, WHITE, ORANGE if ORANGE in globals() else (255, 165, 0)]
            
        intensity = random.uniform(0.8, 1.2)
        count = int(EXPLOSION_PARTICLE_COUNT * intensity)
        
        for _ in range(count):
            color = random.choice(explosion_colors)
            particle = self.pool.get_particle(x, y, ParticleType.EXPLOSION, color)
            self.particles.append(particle)
            
    def create_barrier_explosion(self, x: float, y: float) -> None:
        """Create explosion effect when barrier is destroyed."""
        # Barrier explosions use gray and dark colors
        explosion_colors = [GRAY, DARK_GRAY, WHITE, LIGHT_GRAY]
        intensity = random.uniform(0.6, 1.0)
        count = int(EXPLOSION_PARTICLE_COUNT * 0.7 * intensity)
        
        for _ in range(count):
            color = random.choice(explosion_colors)
            particle = self.pool.get_particle(x, y, ParticleType.EXPLOSION, color)
            self.particles.append(particle)
            
    def create_player_explosion(self, x: float, y: float) -> None:
        """Create explosion effect when player is destroyed."""
        # Player explosions are more intense
        explosion_colors = [RED, YELLOW, WHITE, ORANGE if ORANGE in globals() else (255, 165, 0)]
        count = int(EXPLOSION_PARTICLE_COUNT * 2.0)
        
        for _ in range(count):
            color = random.choice(explosion_colors)
            particle = self.pool.get_particle(x, y, ParticleType.EXPLOSION, color)
            self.particles.append(particle)
            
    def update(self, dt: float) -> None:
        """Update all particles in the system."""
        # Update all particles
        for particle in self.particles:
            particle.update(dt)
            
        # Cleanup dead particles
        self.pool.cleanup_dead_particles()
        
        # Remove dead particles from active list
        self.particles = [p for p in self.particles if not p.is_dead()]
        
    def render(self, surface: pygame.Surface) -> None:
        """Render all active particles."""
        for particle in self.particles:
            particle.render(surface)
            
    def clear(self) -> None:
        """Clear all particles from the system."""
        for particle in self.particles:
            self.pool.release_particle(particle)
        self.particles.clear()
        
    def get_particle_count(self) -> int:
        """Get the total number of active particles."""
        return len(self.particles)
        
    def is_max_capacity_reached(self, max_particles: int = 500) -> bool:
        """Check if particle system has reached maximum capacity."""
        return len(self.particles) >= max_particles