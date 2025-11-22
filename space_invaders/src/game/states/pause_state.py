"""
Pause State
Handles the pause menu and unpausing.
"""

import pygame
from src.game.game_state import GameState
from config.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER_X, SCREEN_CENTER_Y,
    BLACK, WHITE, UI_COLOR, LARGE_FONT_SIZE, MEDIUM_FONT_SIZE, KEY_PAUSE
)

class PauseState(GameState):
    """Pause screen state with pause menu."""
    
    def __init__(self):
        """Initialize the pause state."""
        super().__init__()
        self.name = "pause"
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, LARGE_FONT_SIZE)
        self.medium_font = pygame.font.Font(None, MEDIUM_FONT_SIZE)
    
    def handle_events(self, event: pygame.event.Event):
        """
        Handle pause screen events.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            New state name to transition to, or None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_PAUSE:  # ESC key to unpause
                return 'play'
        return None
    
    def update(self, dt: float) -> None:
        """Update the pause screen (no game logic when paused)."""
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the pause screen.
        
        Args:
            surface: The pygame surface to render on
        """
        # Clear screen
        surface.fill(BLACK)
        
        # Draw "PAUSED" title
        title_text = self.title_font.render("PAUSED", True, UI_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_CENTER_X, SCREEN_CENTER_Y - 50))
        surface.blit(title_text, title_rect)
        
        # Draw instructions
        instructions = [
            "Press ESC to continue",
            "Game is paused"
        ]
        
        y_pos = SCREEN_CENTER_Y + 50
        for instruction in instructions:
            text = self.medium_font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_CENTER_X, y_pos))
            surface.blit(text, text_rect)
            y_pos += 40
    
    def on_enter(self, game_manager) -> None:
        """Called when entering the pause state."""
        pass
    
    def on_exit(self) -> None:
        """Called when exiting the pause state."""
        pass