"""
Collision Manager
Handles collision detection and resolution for the Space Invaders game.
"""

import pygame
from typing import List, Optional

class CollisionManager:
    """
    Manages collision detection between game objects.
    
    This is a simplified collision manager that can be extended
    with more sophisticated collision detection algorithms.
    """
    
    def __init__(self):
        """Initialize the collision manager."""
        pass
        
    def check_rect_collision(self, rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
        """Check if two rectangles collide."""
        return rect1.colliderect(rect2)
        
    def check_circle_collision(self, center1: tuple, radius1: float, center2: tuple, radius2: float) -> bool:
        """Check if two circles collide."""
        dx = center1[0] - center2[0]
        dy = center1[1] - center2[1]
        distance = (dx * dx + dy * dy) ** 0.5
        return distance <= (radius1 + radius2)
        
    def get_collision_depth(self, rect1: pygame.Rect, rect2: pygame.Rect) -> tuple:
        """Get the collision depth between two rectangles."""
        if not rect1.colliderect(rect2):
            return (0, 0)
            
        # Calculate overlap in both x and y directions
        overlap_x = min(rect1.right - rect2.left, rect2.right - rect1.left)
        overlap_y = min(rect1.bottom - rect2.top, rect2.bottom - rect1.top)
        
        return (overlap_x, overlap_y)
        
    def resolve_collision(self, rect1: pygame.Rect, rect2: pygame.Rect) -> tuple:
        """Resolve collision between two rectangles. Returns new positions."""
        if not rect1.colliderect(rect2):
            return rect1.x, rect1.y
            
        # Get collision depth
        overlap_x, overlap_y = self.get_collision_depth(rect1, rect2)
        
        # Move rect1 away from rect2 based on smallest overlap
        new_x, new_y = rect1.x, rect1.y
        
        if overlap_x < overlap_y:
            # Horizontal collision
            if rect1.centerx < rect2.centerx:
                new_x -= overlap_x
            else:
                new_x += overlap_x
        else:
            # Vertical collision
            if rect1.centery < rect2.centery:
                new_y -= overlap_y
            else:
                new_y += overlap_y
                
        return (new_x, new_y)
        
    def is_point_in_rect(self, point: tuple, rect: pygame.Rect) -> bool:
        """Check if a point is inside a rectangle."""
        return rect.collidepoint(point)
        
    def get_overlapping_objects(self, target_rect: pygame.Rect, object_rects: List[pygame.Rect]) -> List[int]:
        """Get indices of objects that overlap with the target rectangle."""
        overlapping_indices = []
        for i, rect in enumerate(object_rects):
            if rect.colliderect(target_rect):
                overlapping_indices.append(i)
        return overlapping_indices