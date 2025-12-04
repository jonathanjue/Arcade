import pygame
from ..base.sprite_object import SpriteObject
from pygame.math import Vector2

class Bullet(SpriteObject):
    """
    Fast-moving bullet projectile that travels in a straight line.
    """

    def __init__(self, position, direction, speed=500):
        """
        Initialize a bullet.

        Args:
            position (tuple): Starting position (x, y)
            direction (tuple): Direction vector (normalized)
            speed (float): Speed of the bullet. Defaults to 500.
        """
        super().__init__(position, (8, 8), (255, 255, 255))  # Small white dot
        self.direction = Vector2(direction)
        self.speed = speed
        self.active = True
        self.lifetime = 2.0  # 2 seconds max lifetime
        self.time_alive = 0.0

    def update(self, dt):
        """
        Update bullet position.

        Args:
            dt (float): Delta time in seconds
        """
        # Move bullet in direction
        self.position += self.direction * self.speed * dt
        self.time_alive += dt

        # Deactivate if lifetime exceeded
        if self.time_alive >= self.lifetime:
            self.active = False

        # Keep bullet within screen bounds
        self._keep_in_bounds()

    def _keep_in_bounds(self):
        """
        Ensure bullet stays within screen boundaries.
        Deactivate if it goes out of bounds.
        """
        screen_width = 800
        screen_height = 600

        # Deactivate if out of bounds
        if (self.position.x < 0 or self.position.x > screen_width or
            self.position.y < 0 or self.position.y > screen_height):
            self.active = False

    def render(self, screen):
        """
        Render the bullet as a small white dot.

        Args:
            screen: Pygame surface to render on
        """
        if self.active:
            # Draw small white circle for bullet
            center_x = self.position[0] + self.size[0] // 2
            center_y = self.position[1] + self.size[1] // 2
            pygame.draw.circle(screen, self.color, (int(center_x), int(center_y)), 4)

            # Optional: draw direction indicator for debugging
            # end_x = center_x + self.direction.x * 10
            # end_y = center_y + self.direction.y * 10
            # pygame.draw.line(screen, (255, 0, 0), (center_x, center_y), (end_x, end_y), 2)