"""
Formation Manager
Manages alien formation movement and behavior for the Space Invaders game.
"""

import math
from typing import List
from src.entities.alien import Alien
from config.constants import *

class FormationManager:
    """
    Manages alien formation movement and behavior.
    
    Attributes:
        formation_speed (float): Current speed of the formation
        direction (int): Direction of movement (1 for right, -1 for left)
        drop_distance (float): Distance to drop when hitting screen edge
        speed_multiplier (float): Speed multiplier based on remaining aliens
    """
    
    def __init__(self):
        """Initialize the formation manager."""
        self.formation_speed = 30.0  # Base speed
        self.direction = 1  # Start moving right
        self.drop_distance = FORMATION_DROP_DISTANCE
        self.speed_multiplier = 1.0
        
    def update_formation(self, dt: float, aliens: List[Alien], screen_width: int) -> None:
        """Update the alien formation movement."""
        if not aliens:
            return
            
        # Update speed multiplier based on remaining aliens
        total_aliens = len(aliens)
        if total_aliens <= 10:
            self.speed_multiplier = 1.5
        elif total_aliens <= 5:
            self.speed_multiplier = 2.0
        elif total_aliens <= 2:
            self.speed_multiplier = 2.5
        else:
            self.speed_multiplier = 1.0
            
        # Calculate formation bounds
        min_x, max_x = self._get_formation_bounds(aliens)
        
        # Check if formation needs to drop and reverse
        current_speed = self.formation_speed * self.speed_multiplier
        future_left = min_x + (current_speed * dt * self.direction)
        future_right = max_x + (current_speed * dt * self.direction)
        
        # If formation would go off screen, drop and reverse
        if future_left < 0 or future_right > screen_width:
            self._drop_formation(aliens)
            self.direction *= -1
        else:
            # Move formation horizontally
            for alien in aliens:
                alien.x += current_speed * dt * self.direction
                
    def _get_formation_bounds(self, aliens: List[Alien]) -> tuple:
        """Get the leftmost and rightmost positions of the formation."""
        if not aliens:
            return 0, 0
            
        min_x = min(alien.x for alien in aliens)
        max_x = max(alien.x + alien.width for alien in aliens)
        return min_x, max_x
        
    def _drop_formation(self, aliens: List[Alien]) -> None:
        """Drop the formation down and reverse direction."""
        for alien in aliens:
            alien.y += self.drop_distance
            
    def get_formation_direction(self) -> int:
        """Get the current direction of the formation."""
        return self.direction
        
    def is_formation_at_bottom(self, aliens: List[Alien], screen_height: int) -> bool:
        """Check if any alien in formation has reached the bottom."""
        if not aliens:
            return False
            
        return any(alien.y + alien.height >= screen_height - 50 for alien in aliens)