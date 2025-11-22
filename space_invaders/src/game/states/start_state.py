"""
Start State
Handles the start screen and menu navigation.
"""

import pygame
from src.game.game_state import GameState
from config.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER_X, SCREEN_CENTER_Y,
    BLACK, WHITE, UI_COLOR, TITLE_FONT_SIZE, LARGE_FONT_SIZE, 
    MEDIUM_FONT_SIZE, KEY_START
)

class StartState(GameState):
    """Start screen state with title and instructions."""
    
    def __init__(self):
        """Initialize the start state."""
        super().__init__()
        self.name = "start"
        
        # Animation state
        self.animation_timer = 0.0
        self.blink_timer = 0.0
        self.show_title = True
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.large_font = pygame.font.Font(None, LARGE_FONT_SIZE)
        self.medium_font = pygame.font.Font(None, MEDIUM_FONT_SIZE)
    
    def handle_events(self, event: pygame.event.Event):
        """
        Handle start screen events.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            New state name to transition to, or None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_START:  # F key to start game
                return 'play'
        return None
    
    def update(self, dt: float) -> None:
        """
        Update the start screen.
        
        Args:
            dt: Delta time in seconds
        """
        # Update animation timers
        self.animation_timer += dt
        self.blink_timer += dt
        
        # Toggle title visibility every 2 seconds
        if self.animation_timer >= 2.0:
            self.show_title = not self.show_title
            self.animation_timer = 0.0
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the start screen.
        
        Args:
            surface: The pygame surface to render on
        """
        # Clear screen
        surface.fill(BLACK)
        
        # Draw title
        if self.show_title:
            title_text = self.title_font.render("SPACE INVADERS", True, UI_COLOR)
            title_rect = title_text.get_rect(center=(SCREEN_CENTER_X, 150))
            surface.blit(title_text, title_rect)
        
        # Draw instructions
        instructions = [
            "Press F to Start",
            "Use ARROW KEYS to move",
            "Press B to shoot",
            "Press ESC to pause"
        ]
        
        y_pos = 300
        for instruction in instructions:
            if instruction == "Press F to Start":
                # Blink the start instruction
                if int(self.blink_timer * 2) % 2 == 0:  # Blink every 0.5 seconds
                    text = self.large_font.render(instruction, True, WHITE)
                    text_rect = text.get_rect(center=(SCREEN_CENTER_X, y_pos))
                    surface.blit(text, text_rect)
            else:
                text = self.medium_font.render(instruction, True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_CENTER_X, y_pos))
                surface.blit(text, text_rect)
            
            y_pos += 50
        
        # Draw footer
        footer_text = self.medium_font.render("A Classic Arcade Game", True, UI_COLOR)
        footer_rect = footer_text.get_rect(center=(SCREEN_CENTER_X, SCREEN_HEIGHT - 100))
        surface.blit(footer_text, footer_rect)
    
    def on_enter(self, game_manager) -> None:
        """Called when entering the start state."""
        pass
    
    def on_exit(self) -> None:
        """Called when exiting the start state."""
        # Reset animation state
        self.animation_timer = 0.0
        self.blink_timer = 0.0
        self.show_title = True