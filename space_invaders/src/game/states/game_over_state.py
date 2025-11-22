"""
Game Over State
Handles the game over screen and restart logic.
"""

import pygame
from src.game.game_state import GameState
from config.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER_X, SCREEN_CENTER_Y,
    BLACK, WHITE, GAME_OVER_COLOR, LARGE_FONT_SIZE, MEDIUM_FONT_SIZE, KEY_START
)

class GameOverState(GameState):
    """Game over screen state."""
    
    def __init__(self):
        """Initialize the game over state."""
        super().__init__()
        self.name = "game_over"
        self.final_score = 0
        self.high_score = 0
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, LARGE_FONT_SIZE)
        self.medium_font = pygame.font.Font(None, MEDIUM_FONT_SIZE)
        
        # Animation state
        self.blink_timer = 0.0
    
    def handle_events(self, event: pygame.event.Event):
        """
        Handle game over screen events.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            New state name to transition to, or None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_START:  # F key to restart
                return 'play'
        return None
    
    def update(self, dt: float) -> None:
        """
        Update the game over screen.
        
        Args:
            dt: Delta time in seconds
        """
        self.blink_timer += dt
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the game over screen.
        
        Args:
            surface: The pygame surface to render on
        """
        # Clear screen
        surface.fill(BLACK)
        
        # Draw "GAME OVER" title
        title_text = self.title_font.render("GAME OVER", True, GAME_OVER_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_CENTER_X, 150))
        surface.blit(title_text, title_rect)
        
        # Draw scores
        score_text = self.medium_font.render(f"Final Score: {self.final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_CENTER_X, 250))
        surface.blit(score_text, score_rect)
        
        high_score_text = self.medium_font.render(f"High Score: {self.high_score}", True, WHITE)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_CENTER_X, 290))
        surface.blit(high_score_text, high_score_rect)
        
        # Blink restart instruction
        if int(self.blink_timer * 2) % 2 == 0:  # Blink every 0.5 seconds
            restart_text = self.medium_font.render("Press F to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_CENTER_X, 400))
            surface.blit(restart_text, restart_rect)
    
    def on_enter(self, game_manager) -> None:
        """Called when entering the game over state."""
        # Get the final score from the play state
        if 'play' in game_manager.states and hasattr(game_manager.states['play'], 'score_manager'):
            self.final_score = game_manager.states['play'].score_manager.get_score()
        
        # Get high score from score manager
        if 'play' in game_manager.states and hasattr(game_manager.states['play'], 'score_manager'):
            self.high_score = game_manager.states['play'].score_manager.get_high_score()
        
        # Reset blink timer
        self.blink_timer = 0.0
    
    def on_exit(self) -> None:
        """Called when exiting the game over state."""
        pass