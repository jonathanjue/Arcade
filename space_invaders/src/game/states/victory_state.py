"""
Victory State
Handles the victory screen and level progression.
"""

import pygame
from src.game.game_state import GameState
from config.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER_X, SCREEN_CENTER_Y,
    BLACK, WHITE, VICTORY_COLOR, LARGE_FONT_SIZE, MEDIUM_FONT_SIZE, KEY_START
)

class VictoryState(GameState):
    """Victory screen state."""
    
    def __init__(self):
        """Initialize the victory state."""
        super().__init__()
        self.name = "victory"
        self.current_level = 1
        self.final_score = 0
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, LARGE_FONT_SIZE)
        self.medium_font = pygame.font.Font(None, MEDIUM_FONT_SIZE)
        
        # Animation state
        self.blink_timer = 0.0
    
    def handle_events(self, event: pygame.event.Event):
        """
        Handle victory screen events.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            New state name to transition to, or None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_START:  # F key for next level or restart
                return 'play'
        return None
    
    def update(self, dt: float) -> None:
        """
        Update the victory screen.
        
        Args:
            dt: Delta time in seconds
        """
        self.blink_timer += dt
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the victory screen.
        
        Args:
            surface: The pygame surface to render on
        """
        # Clear screen
        surface.fill(BLACK)
        
        # Draw "VICTORY" title
        title_text = self.title_font.render("VICTORY!", True, VICTORY_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_CENTER_X, 150))
        surface.blit(title_text, title_rect)
        
        # Draw level and score information
        level_text = self.medium_font.render(f"Level {self.current_level} Complete!", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_CENTER_X, 250))
        surface.blit(level_text, level_rect)
        
        score_text = self.medium_font.render(f"Score: {self.final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_CENTER_X, 290))
        surface.blit(score_text, score_rect)
        
        # Blink next level instruction
        if int(self.blink_timer * 2) % 2 == 0:  # Blink every 0.5 seconds
            next_text = self.medium_font.render("Press F for next level", True, WHITE)
            next_rect = next_text.get_rect(center=(SCREEN_CENTER_X, 400))
            surface.blit(next_text, next_rect)
    
    def on_enter(self, game_manager) -> None:
        """Called when entering the victory state."""
        # Get the current level and score from the play state
        if 'play' in game_manager.states and hasattr(game_manager.states['play'], 'current_level'):
            self.current_level = game_manager.states['play'].current_level
        
        if 'play' in game_manager.states and hasattr(game_manager.states['play'], 'score_manager'):
            self.final_score = game_manager.states['play'].score_manager.get_score()
        
        # Reset blink timer
        self.blink_timer = 0.0
    
    def on_exit(self) -> None:
        """Called when exiting the victory state."""
        pass