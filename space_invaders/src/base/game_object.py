"""
Base Game Object Class
All game objects inherit from this base class.
"""

import pygame
from abc import ABC, abstractmethod
from typing import Tuple

class GameObject(ABC):
    """
    Abstract base class for all game objects.
    
    Attributes:
        x (float): X coordinate of the object
        y (float): Y coordinate of the object
        width (int): Width of the object
        height (int): Height of the object
        velocity_x (float): Horizontal velocity
        velocity_y (float): Vertical velocity
        active (bool): Whether the object is active
    """
    
    def __init__(self, x: float, y: float, width: int, height: int):
        """Initialize the game object."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.active = True
    
    def get_rect(self) -> pygame.Rect:
        """Get the pygame.Rect for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_center(self) -> Tuple[int, int]:
        """Get the center point of the object."""
        return (int(self.x + self.width // 2), int(self.y + self.height // 2))
    
    def get_position(self) -> Tuple[float, float]:
        """Get the current position."""
        return (self.x, self.y)
    
    def set_position(self, x: float, y: float) -> None:
        """Set the position."""
        self.x = x
        self.y = y
    
    def set_velocity(self, velocity_x: float, velocity_y: float) -> None:
        """Set the velocity."""
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
    
    def is_off_screen(self, screen_width: int, screen_height: int) -> bool:
        """Check if the object is completely off screen."""
        return (self.x + self.width < 0 or 
                self.x > screen_width or 
                self.y + self.height < 0 or 
                self.y > screen_height)
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """Update the object's state."""
        pass
    
    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Render the object."""
        pass