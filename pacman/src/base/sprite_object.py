"""
SpriteObject Base Class

Base class for all visual game entities that can be rendered.
"""

import pygame
from .game_object import GameObject

class SpriteObject(GameObject):
    """Base class for all sprite objects that can be rendered."""

    def __init__(self, position=(0, 0), size=(1, 1), color=(255, 255, 255)):
        """
        Initialize a sprite object.

        Args:
            position: Tuple (x, y) representing the object's position
            size: Tuple (width, height) representing the object's size
            color: Tuple (r, g, b) representing the object's color
        """
        super().__init__(position, size)
        self.color = color
        self.visible = True

    def render(self, surface):
        """
        Render the sprite object as a colored rectangle.

        Args:
            surface: Pygame surface to render on
        """
        if self.visible and self.active:
            # Create a rectangle surface
            rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
            pygame.draw.rect(surface, self.color, rect)

    def set_color(self, color):
        """Set the color of the sprite."""
        self.color = color

    def get_color(self):
        """Get the color of the sprite."""
        return self.color

    def set_visible(self, visible):
        """Set the visibility of the sprite."""
        self.visible = visible

    def is_visible(self):
        """Check if the sprite is visible."""
        return self.visible