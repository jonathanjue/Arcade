"""
GameState Base Class

Abstract base class for all game states.
"""

from abc import ABC, abstractmethod

class GameState(ABC):
    """Abstract base class for all game states."""

    def __init__(self, game_manager):
        """
        Initialize a game state.

        Args:
            game_manager: Reference to the GameManager instance
        """
        self.game_manager = game_manager
        self.name = "BaseState"

    @abstractmethod
    def enter(self):
        """Called when entering this state."""
        pass

    @abstractmethod
    def exit(self):
        """Called when exiting this state."""
        pass

    @abstractmethod
    def handle_event(self, event):
        """
        Handle pygame events.

        Args:
            event: Pygame event to handle
        """
        pass

    @abstractmethod
    def update(self, dt):
        """
        Update the game state.

        Args:
            dt: Delta time in seconds since last update
        """
        pass

    @abstractmethod
    def render(self, screen):
        """
        Render the game state.

        Args:
            screen: Pygame surface to render on
        """
        pass

    def get_game_manager(self):
        """Get the game manager reference."""
        return self.game_manager

    def set_name(self, name):
        """Set the name of this state."""
        self.name = name

    def get_name(self):
        """Get the name of this state."""
        return self.name

    def on_pause_changed(self, is_paused):
        """
        Called when the game pause state changes.

        Args:
            is_paused (bool): True if game is paused, False if resumed
        """
        pass