"""
Base Sprite Object Class
Extends GameObject for sprite-based objects with pygame support.
"""

import pygame
from src.base.game_object import GameObject

class SpriteObject(GameObject):
    """
    Base class for sprite-based game objects.
    
    Attributes:
        surface (pygame.Surface): The sprite surface
        rect (pygame.Rect): The collision rectangle
        color (tuple): Default color for simple rendering
    """
    
    def __init__(self, x: float, y: float, width: int, height: int, color: tuple = None):
        """Initialize the sprite object."""
        super().__init__(x, y, width, height)
        self.surface = pygame.Surface((width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        
        # Fill with default color if provided
        if color:
            self.surface.fill(color)
    
    def set_color(self, color: tuple) -> None:
        """Set the object's color and update the surface."""
        self.color = color
        self.surface.fill(color)
    
    def update_rect(self) -> None:
        """Update the rect position to match x, y coordinates."""
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the sprite object."""
        if self.color:
            self.surface.fill(self.color)
        surface.blit(self.surface, (self.x, self.y))
        self.update_rect()