"""
Game State Base Class
All game states inherit from this base class.
"""

import pygame
from abc import ABC, abstractmethod
from typing import Optional

class GameState(ABC):
    """
    Abstract base class for all game states.
    
    States handle different phases of the game:
    - Start screen
    - Active gameplay
    - Paused state
    - Game over
    - Victory
    """
    
    def __init__(self):
        """Initialize the game state."""
        self.transition_time = 0
        self.name = "base"
    
    @abstractmethod
    def handle_events(self, event: pygame.event.Event) -> Optional[str]:
        """
        Handle pygame events for this state.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            Optional[str]: New state name to transition to, or None
        """
        pass
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update the game state.
        
        Args:
            dt: Delta time in seconds
        """
        pass
    
    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the game state.
        
        Args:
            surface: The pygame surface to render on
        """
        pass
    
    def on_enter(self, game_manager) -> None:
        """
        Called when entering this state.
        
        Args:
            game_manager: The game manager instance
        """
        pass
    
    def on_exit(self) -> None:
        """Called when exiting this state."""
        pass