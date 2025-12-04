"""
GameManager Class

Main game manager that handles the game loop and state management.
"""

import pygame
import sys
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, TARGET_FPS
from .game_state import GameState
from .states.menu_state import MenuState
from ..managers.input_manager import InputManager

class GameManager:
    """Main game manager that controls the game loop and state management."""

    def __init__(self):
        """Initialize the game manager."""
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)

        # Set up game clock
        self.clock = pygame.time.Clock()
        self.running = False
        self.delta_time = 0
        self.paused = False

        # Initialize managers
        self.input_manager = InputManager()

        # Initialize game state
        self.current_state = None
        self.change_state(MenuState(self))

        print("GameManager initialized")

    def run(self):
        """Main game loop."""
        self.running = True

        try:
            while self.running:
                # Calculate delta time
                self.delta_time = self.clock.tick(TARGET_FPS) / 1000.0

                # Handle events
                self.handle_events()

                # Update game state
                self.update(self.delta_time)

                # Render game state
                self.render()

                # Update display
                pygame.display.flip()

        except Exception as e:
            print(f"Game error: {e}")
            self.cleanup()
            raise

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle_pause()
            else:
                # Pass events to input manager
                self.input_manager.handle_event(event)

                # Pass events to current state if it exists
                if self.current_state:
                    self.current_state.handle_event(event)

    def update(self, dt):
        """Update the game state.

        Args:
            dt: Delta time in seconds since last update
        """
        if self.current_state:
            self.current_state.update(dt)

    def render(self):
        """Render the current game state."""
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Render current state if it exists
        if self.current_state:
            self.current_state.render(self.screen)

    def change_state(self, new_state):
        """Change the current game state.

        Args:
            new_state: New GameState instance to switch to
        """
        # Exit current state if it exists
        if self.current_state:
            self.current_state.exit()

        # Set new state
        self.current_state = new_state

        # Enter new state
        if self.current_state:
            self.current_state.enter()

    def cleanup(self):
        """Clean up game resources."""
        pygame.quit()
        print("GameManager cleaned up")

    def get_screen(self):
        """Get the game screen surface."""
        return self.screen

    def get_delta_time(self):
        """Get the current delta time."""
        return self.delta_time

    def is_running(self):
        """Check if the game is running."""
        return self.running

    def is_paused(self):
        """Check if the game is paused."""
        return self.paused

    def toggle_pause(self):
        """Toggle the pause state of the game."""
        self.paused = not self.paused
        print(f"Game {'paused' if self.paused else 'resumed'}")

        # Notify current state about pause change
        if self.current_state:
            self.current_state.on_pause_changed(self.paused)