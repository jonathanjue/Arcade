"""
Alien Entity Classes
Defines the Alien entities and AlienFormation for managing alien formations in Space Invaders.
"""

import pygame
import random
import math
from typing import List, Optional, Tuple, Dict
from src.base.sprite_object import SpriteObject
from config.constants import *
from src.entities.bullet import Bullet, BulletPool

class Alien(SpriteObject):
    """
    Individual alien entity with different types and behaviors.
    
    Attributes:
        alien_type (str): Type of alien ('small', 'medium', 'large')
        score_value (int): Score awarded when destroyed
        animation_timer (float): Timer for animation frames
        current_frame (int): Current animation frame (0 or 1)
        animation_speed (float): Speed of animation in seconds
        row (int): Row position in formation (0=top, 4=bottom)
        is_alive (bool): Whether the alien is alive
        can_shoot (bool): Whether this alien can shoot (bottom row only)
    """
    
    def __init__(self, x: float, y: float, alien_type: str, row: int, formation_offset_x: float = 0, formation_offset_y: float = 0):
        """
        Initialize an alien.
        
        Args:
            x: Starting x position
            y: Starting y position
            alien_type: Type of alien ('small', 'medium', 'large')
            row: Row position in formation (0=top, 4=bottom)
            formation_offset_x: X offset from formation position
            formation_offset_y: Y offset from formation position
        """
        # Get size and speed for this alien type
        size = ALIEN_SIZES[alien_type]
        width, height = size
        
        # Get color based on row
        color = ALIEN_COLORS[row % len(ALIEN_COLORS)]
        
        super().__init__(x, y, width, height, color)
        
        self.alien_type = alien_type
        self.row = row
        self.score_value = ALIEN_SCORES[alien_type]
        self.base_speed = ALIEN_SPEEDS[alien_type]
        
        # Animation properties
        self.animation_timer = 0.0
        self.current_frame = 0
        self.animation_speed = 1.0 / (ALIEN_ANIMATION_SPEED / 60.0)  # Convert to seconds
        
        # Formation offset
        self.formation_offset_x = formation_offset_x
        self.formation_offset_y = formation_offset_y
        
        # Shooting properties
        self.can_shoot = (row >= FORMATION_ROWS - 2)  # Bottom 2 rows can shoot
        
        # State
        self.is_alive = True
        self.velocity_x = 0
        self.velocity_y = 0
    
    def update(self, dt: float, formation_x: float, formation_y: float, formation_direction: int) -> None:
        """
        Update the alien state.
        
        Args:
            dt: Delta time in seconds
            formation_x: X position of the formation
            formation_y: Y position of the formation
            formation_direction: Direction of formation movement (1=right, -1=left)
        """
        if not self.active or not self.is_alive:
            return
        
        # Update animation
        self._update_animation(dt)
        
        # Position is determined by formation + offset
        self.x = formation_x + self.formation_offset_x
        self.y = formation_y + self.formation_offset_y
        
        # Update velocity based on formation direction
        base_speed = self.base_speed * FORMATION_SPEED_MULTIPLIER
        self.velocity_x = base_speed * formation_direction
        self.velocity_y = 0
        
        self.update_rect()
    
    def _update_animation(self, dt: float) -> None:
        """Update the alien animation."""
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            self.current_frame = (self.current_frame + 1) % 2  # 2-frame animation
    
    def take_damage(self) -> None:
        """Handle the alien taking damage (being hit by a bullet)."""
        if self.is_alive:
            self.is_alive = False
            self.active = False
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the alien with different sprites for each type and animation frame.
        
        Args:
            surface: Surface to render on
        """
        if not self.active or not self.is_alive:
            return
        
        # Render different sprites based on alien type and animation frame
        if self.alien_type == 'small':
            self._render_small_alien(surface)
        elif self.alien_type == 'medium':
            self._render_medium_alien(surface)
        else:  # large
            self._render_large_alien(surface)
        
        self.update_rect()
    
    def _render_small_alien(self, surface: pygame.Surface) -> None:
        """Render small alien with 2-frame animation."""
        x, y = int(self.x), int(self.y)
        
        if self.current_frame == 0:
            # Frame 0: Compact form
            pygame.draw.rect(surface, self.color, (x + 6, y + 2, 12, 12))
            pygame.draw.rect(surface, self.color, (x + 2, y + 6, 20, 4))
            pygame.draw.rect(surface, self.color, (x + 4, y + 1, 4, 2))
            pygame.draw.rect(surface, self.color, (x + 16, y + 1, 4, 2))
        else:
            # Frame 1: Extended form
            pygame.draw.rect(surface, self.color, (x + 4, y + 3, 16, 10))
            pygame.draw.rect(surface, self.color, (x + 1, y + 7, 22, 2))
            pygame.draw.rect(surface, self.color, (x + 3, y + 1, 2, 4))
            pygame.draw.rect(surface, self.color, (x + 19, y + 1, 2, 4))
    
    def _render_medium_alien(self, surface: pygame.Surface) -> None:
        """Render medium alien with 2-frame animation."""
        x, y = int(self.x), int(self.y)
        
        if self.current_frame == 0:
            # Frame 0: Standard form
            pygame.draw.rect(surface, self.color, (x + 8, y + 4, 16, 16))
            pygame.draw.rect(surface, self.color, (x + 4, y + 8, 24, 8))
            pygame.draw.rect(surface, self.color, (x + 2, y + 6, 4, 4))
            pygame.draw.rect(surface, self.color, (x + 26, y + 6, 4, 4))
            pygame.draw.rect(surface, self.color, (x + 6, y + 2, 4, 2))
            pygame.draw.rect(surface, self.color, (x + 22, y + 2, 4, 2))
        else:
            # Frame 1: Spread form
            pygame.draw.rect(surface, self.color, (x + 6, y + 6, 20, 12))
            pygame.draw.rect(surface, self.color, (x + 2, y + 10, 28, 4))
            pygame.draw.rect(surface, self.color, (x, y + 8, 4, 8))
            pygame.draw.rect(surface, self.color, (x + 28, y + 8, 4, 8))
            pygame.draw.rect(surface, self.color, (x + 4, y + 4, 4, 4))
            pygame.draw.rect(surface, self.color, (x + 24, y + 4, 4, 4))
    
    def _render_large_alien(self, surface: pygame.Surface) -> None:
        """Render large alien with 2-frame animation."""
        x, y = int(self.x), int(self.y)
        
        if self.current_frame == 0:
            # Frame 0: Aggressive form
            pygame.draw.rect(surface, self.color, (x + 10, y + 6, 20, 20))
            pygame.draw.rect(surface, self.color, (x + 6, y + 12, 28, 8))
            pygame.draw.rect(surface, self.color, (x + 2, y + 10, 6, 12))
            pygame.draw.rect(surface, self.color, (x + 32, y + 10, 6, 12))
            pygame.draw.rect(surface, self.color, (x + 8, y + 2, 6, 4))
            pygame.draw.rect(surface, self.color, (x + 26, y + 2, 6, 4))
            pygame.draw.rect(surface, self.color, (x + 14, y + 1, 4, 2))
            pygame.draw.rect(surface, self.color, (x + 22, y + 1, 4, 2))
        else:
            # Frame 1: Defensive form
            pygame.draw.rect(surface, self.color, (x + 8, y + 8, 24, 16))
            pygame.draw.rect(surface, self.color, (x + 4, y + 14, 32, 6))
            pygame.draw.rect(surface, self.color, (x, y + 12, 6, 10))
            pygame.draw.rect(surface, self.color, (x + 34, y + 12, 6, 10))
            pygame.draw.rect(surface, self.color, (x + 6, y + 6, 6, 6))
            pygame.draw.rect(surface, self.color, (x + 28, y + 6, 6, 6))
            pygame.draw.rect(surface, self.color, (x + 12, y + 4, 4, 4))
            pygame.draw.rect(surface, self.color, (x + 24, y + 4, 4, 4))
    
    def get_score_value(self) -> int:
        """
        Get the score value for this alien.
        
        Returns:
            int: Score value for destroying this alien
        """
        return self.score_value if self.is_alive else 0
    
    def can_be_shooter(self) -> bool:
        """
        Check if this alien can shoot (bottom rows only).
        
        Returns:
            bool: True if this alien can shoot
        """
        return self.can_shoot and self.is_alive and self.active


class AlienFormation:
    """
    Manages a formation of aliens with collective movement and behaviors.
    
    Attributes:
        aliens (List[List[Alien]]): 2D grid of aliens
        formation_x (float): Current x position of formation
        formation_y (float): Current y position of formation
        direction (int): Movement direction (1=right, -1=left)
        base_speed (float): Base movement speed
        speed_multiplier (float): Speed multiplier (increases as aliens are destroyed)
        drop_distance (float): Distance to drop when hitting screen edge
        total_aliens (int): Total number of aliens in formation
        alive_aliens (int): Number of alive aliens
        shoot_timer (float): Timer for shooting
        last_shoot_time (float): Time of last shot
        bullet_pool (BulletPool): Pool for alien bullets
    """
    
    def __init__(self, bullet_pool: BulletPool):
        """
        Initialize the alien formation.
        
        Args:
            bullet_pool: Pool for managing alien bullets
        """
        self.bullet_pool = bullet_pool
        
        # Formation properties
        self.aliens = []
        self.formation_x = 0
        self.formation_y = FORMATION_START_Y
        self.direction = 1  # Start moving right
        self.base_speed = 30  # Base formation speed
        self.speed_multiplier = 1.0
        self.drop_distance = FORMATION_DROP_DISTANCE
        
        # Alien management
        self.total_aliens = 0
        self.alive_aliens = 0
        self.shoot_timer = 0.0
        self.last_shoot_time = 0.0
        
        # Create the formation
        self._create_formation()
    
    def _create_formation(self) -> None:
        """Create the initial 5x11 formation of aliens."""
        self.aliens = []
        
        # Calculate starting position to center the formation
        formation_width = (FORMATION_COLS - 1) * FORMATION_HORIZONTAL_SPACING
        self.formation_x = (SCREEN_WIDTH - formation_width) // 2
        
        for row in range(FORMATION_ROWS):
            alien_row = []
            
            # Determine alien type based on row
            if row <= 1:  # Top 2 rows
                alien_type = 'small'
            elif row <= 3:  # Middle 2 rows
                alien_type = 'medium'
            else:  # Bottom row
                alien_type = 'large'
            
            for col in range(FORMATION_COLS):
                # Calculate position with spacing
                offset_x = col * FORMATION_HORIZONTAL_SPACING
                offset_y = row * FORMATION_VERTICAL_SPACING
                
                # Create alien at formation position + offset
                alien_x = self.formation_x + offset_x
                alien_y = self.formation_y + offset_y
                
                alien = Alien(alien_x, alien_y, alien_type, row, offset_x, offset_y)
                alien_row.append(alien)
            
            self.aliens.append(alien_row)
        
        # Count total aliens
        self.total_aliens = FORMATION_ROWS * FORMATION_COLS
        self.alive_aliens = self.total_aliens
    
    def update(self, dt: float, screen_width: int, screen_height: int) -> None:
        """
        Update the entire alien formation.
        
        Args:
            dt: Delta time in seconds
            screen_width: Screen width for boundary checking
            screen_height: Screen height for boundary checking
        """
        # Update speed multiplier based on alive aliens
        self._update_speed_multiplier()
        
        # Handle movement and edge detection
        self._handle_movement(dt, screen_width)
        
        # Update all aliens
        self._update_aliens(dt)
        
        # Handle shooting
        self._handle_shooting(dt)
    
    def _update_speed_multiplier(self) -> None:
        """Update speed multiplier as aliens are destroyed."""
        if self.total_aliens > 0:
            # Increase speed as fewer aliens remain
            destruction_ratio = 1.0 - (self.alive_aliens / self.total_aliens)
            self.speed_multiplier = 1.0 + (destruction_ratio * 2.0)  # Max 3x speed
    
    def _handle_movement(self, dt: float, screen_width: int) -> None:
        """Handle formation movement and edge detection."""
        if self.alive_aliens == 0:
            return
        
        # Calculate current formation bounds
        leftmost_alien, rightmost_alien = self._get_formation_bounds()
        
        if leftmost_alien is None or rightmost_alien is None:
            return
        
        # Check if formation would hit screen edges
        formation_speed = self.base_speed * self.speed_multiplier
        next_left = leftmost_alien.formation_offset_x + (formation_speed * self.direction * dt)
        next_right = rightmost_alien.formation_offset_x + (formation_speed * self.direction * dt)
        
        # Calculate alien widths for boundary checking
        left_alien_width = ALIEN_SIZES[leftmost_alien.alien_type][0]
        right_alien_width = ALIEN_SIZES[rightmost_alien.alien_type][0]
        
        # Check if hitting left edge
        if self.direction < 0 and self.formation_x + next_left <= 0:
            self.direction = 1  # Change to right
            self.formation_y += self.drop_distance  # Drop down
            
        # Check if hitting right edge
        elif self.direction > 0 and self.formation_x + next_right + right_alien_width >= screen_width:
            self.direction = -1  # Change to left
            self.formation_y += self.drop_distance  # Drop down
        
        # Update formation position
        self.formation_x += formation_speed * self.direction * dt
    
    def _get_formation_bounds(self) -> Tuple[Optional[Alien], Optional[Alien]]:
        """
        Get the leftmost and rightmost alive aliens.
        
        Returns:
            Tuple[Optional[Alien], Optional[Alien]]: Leftmost and rightmost aliens
        """
        leftmost_alien = None
        rightmost_alien = None
        
        min_offset_x = float('inf')
        max_offset_x = float('-inf')
        
        for row in self.aliens:
            for alien in row:
                if alien.is_alive and alien.active:
                    if alien.formation_offset_x < min_offset_x:
                        min_offset_x = alien.formation_offset_x
                        leftmost_alien = alien
                    
                    if alien.formation_offset_x > max_offset_x:
                        max_offset_x = alien.formation_offset_x
                        rightmost_alien = alien
        
        return leftmost_alien, rightmost_alien
    
    def _update_aliens(self, dt: float) -> None:
        """Update all aliens in the formation."""
        for row in self.aliens:
            for alien in row:
                alien.update(dt, self.formation_x, self.formation_y, self.direction)
    
    def _handle_shooting(self, dt: float) -> None:
        """Handle formation shooting logic."""
        self.shoot_timer += dt
        
        # Check if we can shoot
        if self.shoot_timer >= self._get_shoot_interval():
            if random.random() < ALIEN_SHOOT_PROBABILITY:
                self._shoot()
                self.shoot_timer = 0.0
                self.last_shoot_time = pygame.time.get_ticks() / 1000.0
    
    def _get_shoot_interval(self) -> float:
        """
        Get the current shooting interval based on remaining aliens.
        
        Returns:
            float: Shooting interval in seconds
        """
        if self.total_aliens > 0:
            destruction_ratio = 1.0 - (self.alive_aliens / self.total_aliens)
            # Faster shooting as fewer aliens remain
            return max(0.3, ALIEN_SHOOT_INTERVAL * (1.0 - destruction_ratio * 0.7))
        return ALIEN_SHOOT_INTERVAL
    
    def _shoot(self) -> None:
        """Shoot a bullet from a random bottom-row alien."""
        shooter = self._get_random_shooter()
        
        if shooter:
            # Create bullet at shooter position
            bullet_x = shooter.x + shooter.width // 2 - BULLET_WIDTH // 2
            bullet_y = shooter.y + shooter.height
            
            # Get bullet from pool
            bullet = self.bullet_pool.get_bullet(bullet_x, bullet_y, False)  # False = enemy bullet
            
            if bullet:
                # Set bullet velocity downward
                bullet.velocity_y = ENEMY_BULLET_SPEED
    
    def _get_random_shooter(self) -> Optional[Alien]:
        """
        Get a random alien that can shoot (from bottom rows).
        
        Returns:
            Optional[Alien]: A random shooter or None if no shooters available
        """
        shooters = []
        
        # Get bottom 2 rows of alive aliens
        for row_idx in range(max(0, FORMATION_ROWS - 2), FORMATION_ROWS):
            for alien in self.aliens[row_idx]:
                if alien.can_be_shooter():
                    shooters.append(alien)
        
        return random.choice(shooters) if shooters else None
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the entire alien formation.
        
        Args:
            surface: Surface to render on
        """
        for row in self.aliens:
            for alien in row:
                alien.render(surface)
    
    def check_collision_with_bullet(self, bullet: Bullet) -> Optional[Alien]:
        """
        Check if a bullet collides with any alien.
        
        Args:
            bullet: Bullet to check collision with
            
        Returns:
            Optional[Alien]: The alien hit by the bullet, or None if no collision
        """
        for row in self.aliens:
            for alien in row:
                if alien.is_alive and alien.active and alien.rect.colliderect(bullet.rect):
                    alien.take_damage()
                    self.alive_aliens -= 1
                    return alien
        
        return None
    
    def check_collision_with_player(self, player_rect: pygame.Rect) -> bool:
        """
        Check if any alien collides with the player.
        
        Args:
            player_rect: Rectangle representing the player
            
        Returns:
            bool: True if any alien collides with the player
        """
        for row in self.aliens:
            for alien in row:
                if alien.is_alive and alien.active and alien.rect.colliderect(player_rect):
                    return True
        
        return False
    
    def check_reached_bottom(self, screen_height: int) -> bool:
        """
        Check if any alien has reached the bottom of the screen.
        
        Args:
            screen_height: Screen height for comparison
            
        Returns:
            bool: True if any alien has reached the bottom
        """
        for row in self.aliens:
            for alien in row:
                if alien.is_alive and alien.active and alien.y + alien.height >= screen_height - 50:
                    return True
        
        return False
    
    def get_alive_aliens(self) -> List[Alien]:
        """
        Get all alive aliens.
        
        Returns:
            List[Alien]: List of all alive aliens
        """
        alive = []
        for row in self.aliens:
            for alien in row:
                if alien.is_alive and alien.active:
                    alive.append(alien)
        return alive
    
    def get_total_score(self) -> int:
        """
        Get the total score value of all remaining aliens.
        
        Returns:
            int: Total score value
        """
        total_score = 0
        for row in self.aliens:
            for alien in row:
                total_score += alien.get_score_value()
        return total_score
    
    def is_defeated(self) -> bool:
        """
        Check if the formation is completely defeated.
        
        Returns:
            bool: True if all aliens are destroyed
        """
        return self.alive_aliens == 0
    
    def reset(self) -> None:
        """Reset the formation to initial state."""
        self.formation_x = 0
        self.formation_y = FORMATION_START_Y
        self.direction = 1
        self.speed_multiplier = 1.0
        self.shoot_timer = 0.0
        self.last_shoot_time = 0.0
        
        # Recreate formation
        self._create_formation()