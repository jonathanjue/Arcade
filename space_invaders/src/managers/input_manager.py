"""
Input Manager
Handles all user input processing for the Space Invaders game.
"""

import pygame
from typing import Set

class InputManager:
    """
    Manages keyboard input for the game.
    
    Attributes:
        keys_pressed (Set[int]): Set of currently pressed keys
        keys_just_pressed (Set[int]): Set of keys pressed this frame
    """
    
    def __init__(self):
        """Initialize the input manager."""
        self.keys_pressed: Set[int] = set()
        self.keys_just_pressed: Set[int] = set()
        
    def update(self) -> None:
        """Update input state for the current frame."""
        # Clear just pressed keys from previous frame
        self.keys_just_pressed.clear()
        
        # Get current key states
        keys = pygame.key.get_pressed()
        
        # Update key states
        for key_code in range(pygame.K_LAST):
            if keys[key_code]:
                if key_code not in self.keys_pressed:
                    self.keys_just_pressed.add(key_code)
                self.keys_pressed.add(key_code)
            else:
                self.keys_pressed.discard(key_code)
                
    def is_key_pressed(self, key_code: int) -> bool:
        """Check if a key is currently pressed."""
        return key_code in self.keys_pressed
        
    def is_key_just_pressed(self, key_code: int) -> bool:
        """Check if a key was pressed this frame."""
        return key_code in self.keys_just_pressed
        
    def is_any_key_pressed(self, key_codes: list) -> bool:
        """Check if any of the specified keys is currently pressed."""
        return any(key_code in self.keys_pressed for key_code in key_codes)
        
    def was_any_key_just_pressed(self, key_codes: list) -> bool:
        """Check if any of the specified keys was just pressed."""
        return any(key_code in self.keys_just_pressed for key_code in key_codes)