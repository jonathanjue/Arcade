import pygame
import random
import math
from constants import PARTICLE_COUNT, PARTICLE_LIFETIME, PARTICLE_SPEED, PARTICLE_SIZE

class Particle:
    def __init__(self, x, y, color, angle=None, speed=None):
        self.x = x
        self.y = y
        self.color = color
        self.size = PARTICLE_SIZE

        # Set random angle if not provided
        self.angle = angle if angle is not None else random.uniform(0, 2 * math.pi)

        # Set random speed if not provided
        self.speed = speed if speed is not None else random.uniform(PARTICLE_SPEED * 0.5, PARTICLE_SPEED * 1.5)

        # Physics properties
        self.velocity_x = math.cos(self.angle) * self.speed
        self.velocity_y = math.sin(self.angle) * self.speed
        self.lifetime = PARTICLE_LIFETIME
        self.age = 0

        # Add some randomness to movement
        self.rotation_speed = random.uniform(-0.1, 0.1)

        # Gravity effect
        self.gravity = random.uniform(0.05, 0.2)

        # Friction
        self.friction = random.uniform(0.95, 0.99)

    def update(self):
        """Update particle position and physics"""
        # Apply physics-based movement
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction

        # Apply gravity
        self.velocity_y += self.gravity

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Rotate direction slightly
        self.angle += self.rotation_speed

        # Age the particle
        self.age += 1

        # Fade out over time
        self.size = max(1, self.size * (1 - self.age / self.lifetime))

    def is_dead(self):
        """Check if particle should be removed"""
        return self.age >= self.lifetime or self.size <= 0

    def draw(self, screen):
        """Draw the particle on screen"""
        # Calculate alpha based on age (fade out)
        alpha = max(0, 255 * (1 - self.age / self.lifetime))

        # Create a surface with per-pixel alpha
        particle_surface = pygame.Surface((int(self.size), int(self.size)), pygame.SRCALPHA)

        # Draw the particle with color and alpha
        color_with_alpha = (*self.color[:3], alpha)
        pygame.draw.circle(particle_surface, color_with_alpha, (int(self.size/2), int(self.size/2)), int(self.size/2))

        # Draw the particle on screen
        screen.blit(particle_surface, (int(self.x), int(self.y)))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def spawn_particles(self, x, y, color, count=PARTICLE_COUNT):
        """Spawn multiple particles at a position"""
        for _ in range(count):
            # Create particles with colors matching the target
            particle_color = self._get_varied_color(color)
            self.particles.append(Particle(x, y, particle_color))

    def _get_varied_color(self, base_color):
        """Get a color variation based on the target color"""
        # Extract RGB components
        r, g, b = base_color[:3]

        # Add some random variation
        r_variation = random.randint(-50, 50)
        g_variation = random.randint(-50, 50)
        b_variation = random.randint(-50, 50)

        # Ensure values stay within 0-255 range
        r = max(0, min(255, r + r_variation))
        g = max(0, min(255, g + g_variation))
        b = max(0, min(255, b + b_variation))

        return (r, g, b)

    def update(self):
        """Update all particles in the system"""
        # Update particles and remove dead ones
        self.particles = [particle for particle in self.particles if not particle.is_dead()]

        # Update remaining particles
        for particle in self.particles:
            particle.update()

    def draw(self, screen):
        """Draw all particles in the system"""
        for particle in self.particles:
            particle.draw(screen)

    def clear(self):
        """Clear all particles"""
        self.particles = []