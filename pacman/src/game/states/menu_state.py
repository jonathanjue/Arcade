"""
MenuState Class

Handles the main menu state of the game.
"""

import pygame
from ..game_state import GameState
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from constants import WHITE, BLACK, YELLOW

class MenuState(GameState):
    """Main menu state for the game."""

    def __init__(self, game_manager):
        """
        Initialize the menu state.

        Args:
            game_manager: Reference to the GameManager instance
        """
        super().__init__(game_manager)
        self.set_name("MenuState")
        self.selected_option = 0
        self.options = ["Start Game", "Quit"]
        self.font = pygame.font.SysFont('Arial', 36)

    def enter(self):
        """Called when entering the menu state."""
        print("Entering MenuState")

    def exit(self):
        """Called when exiting the menu state."""
        print("Exiting MenuState")

    def handle_event(self, event):
        """
        Handle pygame events.

        Args:
            event: Pygame event to handle
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self._handle_selection()

    def _handle_selection(self):
        """Handle menu option selection."""
        if self.selected_option == 0:  # Start Game
            from .play_state import PlayState
            self.get_game_manager().change_state(PlayState(self.get_game_manager()))
        elif self.selected_option == 1:  # Quit
            self.get_game_manager().running = False

    def update(self, dt):
        """
        Update the menu state.

        Args:
            dt: Delta time in seconds since last update
        """
        # Menu state doesn't need complex updates
        pass

    def render(self, screen):
        """
        Render the menu state.

        Args:
            screen: Pygame surface to render on
        """
        # Clear screen
        screen.fill(BLACK)

        # Render title
        title_text = self.font.render("PACMAN", True, YELLOW)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_text, title_rect)

        # Render menu options
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_option else WHITE
            option_text = self.font.render(option, True, color)
            option_rect = option_text.get_rect(center=(screen.get_width() // 2, 250 + i * 60))
            screen.blit(option_text, option_rect)

        # Render instructions
        instructions = self.font.render("Use arrow keys to navigate, Enter to select", True, WHITE)
        instructions_rect = instructions.get_rect(center=(screen.get_width() // 2, 450))
        screen.blit(instructions, instructions_rect)