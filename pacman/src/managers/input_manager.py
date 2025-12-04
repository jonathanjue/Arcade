"""
InputManager Class

Handles all input processing for the game.
"""

import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from constants import INPUT_UP, INPUT_DOWN, INPUT_LEFT, INPUT_RIGHT, INPUT_ENTER, INPUT_ESCAPE

class InputManager:
    """Manages all game input processing."""

    def __init__(self):
        """Initialize the input manager."""
        self.current_direction = None
        self.keys_pressed = set()
        self.mouse_position = (0, 0)

    def handle_event(self, event):
        """
        Handle a pygame event.

        Args:
            event: Pygame event to handle
        """
        if event.type == pygame.KEYDOWN:
            self._handle_key_down(event)
        elif event.type == pygame.KEYUP:
            self._handle_key_up(event)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)

    def _handle_key_down(self, event):
        """Handle key down events."""
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.current_direction = INPUT_UP
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.current_direction = INPUT_DOWN
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.current_direction = INPUT_LEFT
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.current_direction = INPUT_RIGHT
        elif event.key == pygame.K_RETURN:
            self._handle_enter_key()
        elif event.key == pygame.K_ESCAPE:
            self._handle_escape_key()

        self.keys_pressed.add(event.key)

    def _handle_key_up(self, event):
        """Handle key up events."""
        if event.key in self.keys_pressed:
            self.keys_pressed.remove(event.key)

            # Clear direction if opposite key is pressed
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if pygame.K_DOWN in self.keys_pressed or pygame.K_s in self.keys_pressed:
                    self.current_direction = INPUT_DOWN
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if pygame.K_UP in self.keys_pressed or pygame.K_w in self.keys_pressed:
                    self.current_direction = INPUT_UP
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if pygame.K_RIGHT in self.keys_pressed or pygame.K_d in self.keys_pressed:
                    self.current_direction = INPUT_RIGHT
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if pygame.K_LEFT in self.keys_pressed or pygame.K_a in self.keys_pressed:
                    self.current_direction = INPUT_LEFT

    def _handle_mouse_motion(self, event):
        """Handle mouse motion events."""
        self.mouse_position = event.pos

    def _handle_enter_key(self):
        """Handle Enter key press."""
        print("Enter key pressed")

    def _handle_escape_key(self):
        """Handle Escape key press."""
        print("Escape key pressed")

    def get_current_direction(self):
        """Get the current movement direction."""
        return self.current_direction

    def is_key_pressed(self, key):
        """Check if a specific key is pressed."""
        return key in self.keys_pressed

    def get_mouse_position(self):
        """Get the current mouse position."""
        return self.mouse_position

    def reset(self):
        """Reset the input manager state."""
        self.current_direction = None
        self.keys_pressed.clear()
        self.mouse_position = (0, 0)