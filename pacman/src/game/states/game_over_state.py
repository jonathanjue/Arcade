"""
GameOverState Class

Handles the game over state.
"""

import pygame
from ..game_state import GameState
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from constants import BLACK, WHITE, YELLOW, RED

class GameOverState(GameState):
    """Game over state for the game."""

    def __init__(self, game_manager, final_score):
        """
        Initialize the game over state.

        Args:
            game_manager: Reference to the GameManager instance
            final_score: The final score achieved in the game
        """
        super().__init__(game_manager)
        self.set_name("GameOverState")
        self.final_score = final_score
        self.font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 24)
        self.selected_option = 0  # 0: Retry, 1: Quit

    def enter(self):
        """Called when entering the game over state."""
        print(f"Entering GameOverState with score: {self.final_score}")

    def exit(self):
        """Called when exiting the game over state."""
        print("Exiting GameOverState")

    def handle_event(self, event):
        """
        Handle pygame events.

        Args:
            event: Pygame event to handle
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = 0  # Retry
            elif event.key == pygame.K_DOWN:
                self.selected_option = 1  # Quit
            elif event.key == pygame.K_RETURN:
                # Handle selection
                if self.selected_option == 0:  # Retry
                    from .play_state import PlayState
                    self.get_game_manager().change_state(PlayState(self.get_game_manager()))
                else:  # Quit
                    self.get_game_manager().running = False
            elif event.key == pygame.K_ESCAPE:
                # Quit game
                self.get_game_manager().running = False

    def update(self, dt):
        """
        Update the game over state.

        Args:
            dt: Delta time in seconds since last update
        """
        # Game over state doesn't need complex updates
        pass

    def render(self, screen):
        """
        Render the game over state.

        Args:
            screen: Pygame surface to render on
        """
        # Clear screen
        screen.fill(BLACK)

        # Render "You die" message
        die_text = self.font.render("YOU DIE", True, RED)
        die_rect = die_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(die_text, die_rect)

        # Render final score
        score_text = self.font.render(f"Final Score: {self.final_score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(score_text, score_rect)

        # Render retry/quit options with selection
        retry_text = self.small_font.render("RETRY", True, WHITE)
        quit_text = self.small_font.render("QUIT", True, WHITE)

        # Highlight the selected option
        retry_color = YELLOW if self.selected_option == 0 else WHITE
        quit_color = YELLOW if self.selected_option == 1 else WHITE

        retry_surface = self.small_font.render("RETRY", True, retry_color)
        quit_surface = self.small_font.render("QUIT", True, quit_color)

        retry_rect = retry_surface.get_rect(center=(screen.get_width() // 2, 300))
        quit_rect = quit_surface.get_rect(center=(screen.get_width() // 2, 350))

        screen.blit(retry_surface, retry_rect)
        screen.blit(quit_surface, quit_rect)

        # Render instructions
        instructions = self.small_font.render("Use UP/DOWN to select, ENTER to confirm", True, WHITE)
        instructions_rect = instructions.get_rect(center=(screen.get_width() // 2, 400))
        screen.blit(instructions, instructions_rect)