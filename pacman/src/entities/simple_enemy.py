import pygame
import math
from ..base.sprite_object import SpriteObject
from pygame.math import Vector2

class SimpleEnemy(SpriteObject):
    """
    Simple enemy that chases the player (Pacman) with basic AI.
    """

    def __init__(self, position, target=None):
        """
        Initialize the simple enemy.

        Args:
            position (tuple): Initial position (x, y)
            target (tuple, optional): Initial target position. Defaults to None.
        """
        super().__init__(position, (30, 30), (255, 0, 0))  # Red enemy
        self.target = Vector2(target) if target else Vector2(0, 0)
        self.speed = 2.0
        self.chase_range = 300  # Distance at which enemy starts chasing
        self.game_manager = None

    def set_game_manager(self, game_manager):
        """
        Set the game manager reference for pause state checking.

        Args:
            game_manager: Reference to the GameManager instance
        """
        self.game_manager = game_manager

    def chase_target(self, target_position):
        """
        Calculate movement direction to chase the target.

        Args:
            target_position (tuple): Position of the target (Pacman)

        Returns:
            Vector2: Movement vector
        """
        if not target_position:
            return Vector2(0, 0)

        # Calculate direction to target
        direction = Vector2(target_position) - Vector2(self.position)

        # Only chase if target is within chase range
        if direction.length() > self.chase_range:
            return Vector2(0, 0)

        # Normalize direction and apply speed
        if direction.length() > 0:
            direction = direction.normalize()
        return direction * self.speed

    def update(self, dt, target_position=None):
        """
        Update the enemy's position based on target.

        Args:
            dt (float): Delta time since last update
            target_position (tuple, optional): Current target position
        """
        if self.game_manager and self.game_manager.is_paused():
            return  # Don't move when game is paused

        if target_position:
            self.target = Vector2(target_position)

        # Calculate movement
        movement = self.chase_target(self.target)
        self.position += movement * dt

        # Keep enemy within screen bounds
        self._keep_in_bounds()

    def _keep_in_bounds(self):
        """
        Ensure enemy stays within screen boundaries.
        """
        screen_width = 800
        screen_height = 600

        # Keep within screen bounds
        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x > screen_width - self.size[0]:
            self.position.x = screen_width - self.size[0]

        if self.position.y < 0:
            self.position.y = 0
        elif self.position.y > screen_height - self.size[1]:
            self.position.y = screen_height - self.size[1]

    def render(self, screen):
        """
        Render the enemy on screen.

        Args:
            screen: Pygame surface to render on
        """
        # Draw enemy as red rectangle
        rect = pygame.Rect(self.position, self.size)
        pygame.draw.rect(screen, self.color, rect)

        # Draw "enemy" text for clarity
        font = pygame.font.SysFont('Arial', 12)
        text = font.render("ENEMY", True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)