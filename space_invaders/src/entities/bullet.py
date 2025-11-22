"""
Bullet Entity
Represents projectiles fired by both player and enemies with pooling support.
"""

import pygame
from src.base.sprite_object import SpriteObject
from config.constants import *

class Bullet(SpriteObject):
    """
    Bullet projectile for both player and enemies.
    
    Attributes:
        is_player_bullet (bool): True if fired by player, False if by enemy
        speed (float): Bullet speed
        damage (int): Damage dealt by the bullet
    """
    
    def __init__(self, x: float, y: float, is_player_bullet: bool = True):
        """
        Initialize a bullet.
        
        Args:
            x: Starting x position
            y: Starting y position
            is_player_bullet: True for player bullets, False for enemy bullets
        """
        color = PLAYER_BULLET_COLOR if is_player_bullet else ENEMY_BULLET_COLOR
        super().__init__(x, y, BULLET_WIDTH, BULLET_HEIGHT, color)
        
        self.is_player_bullet = is_player_bullet
        self.damage = 1
        
        # Set speed and direction based on bullet type
        if is_player_bullet:
            self.speed = PLAYER_BULLET_SPEED
            self.velocity_y = -self.speed  # Move up
        else:
            self.speed = ENEMY_BULLET_SPEED
            self.velocity_y = self.speed  # Move down
    
    def update(self, dt: float) -> None:
        """
        Update bullet position.
        
        Args:
            dt: Delta time in seconds
        """
        if not self.active:
            return
        
        # Update position based on velocity
        self.y += self.velocity_y * dt
        
        # Deactivate if off screen
        if self.is_player_bullet:
            if self.y + self.height < 0:
                self.active = False
        else:
            if self.y > SCREEN_HEIGHT:
                self.active = False
        
        self.update_rect()
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the bullet."""
        if not self.active:
            return
        
        # Draw bullet as a rectangle
        pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.width, self.height))
        
        # Add a glow effect for player bullets
        if self.is_player_bullet:
            glow_rect = pygame.Rect(int(self.x) - 1, int(self.y) - 1, self.width + 2, self.height + 2)
            pygame.draw.rect(surface, self.color, glow_rect, 1)
    
    def reset(self, x: float, y: float, is_player_bullet: bool = True) -> None:
        """
        Reset bullet for reuse (pooling).
        
        Args:
            x: New x position
            y: New y position
            is_player_bullet: True for player bullets, False for enemy bullets
        """
        self.x = x
        self.y = y
        self.is_player_bullet = is_player_bullet
        self.active = True
        
        # Update color and velocity based on bullet type
        if is_player_bullet:
            self.color = PLAYER_BULLET_COLOR
            self.speed = PLAYER_BULLET_SPEED
            self.velocity_y = -self.speed
        else:
            self.color = ENEMY_BULLET_COLOR
            self.speed = ENEMY_BULLET_SPEED
            self.velocity_y = self.speed
        
        self.update_rect()


class BulletPool:
    """
    Object pool for bullets to improve performance.
    
    Attributes:
        bullets (list): List of all bullets in the pool
        max_bullets (int): Maximum number of bullets in the pool
    """
    
    def __init__(self, max_bullets: int = 50):
        """
        Initialize the bullet pool.
        
        Args:
            max_bullets: Maximum number of bullets to pool
        """
        self.bullets = []
        self.max_bullets = max_bullets
        
        # Pre-create bullets
        for _ in range(max_bullets):
            bullet = Bullet(0, 0, True)
            bullet.active = False
            self.bullets.append(bullet)
    
    def get_bullet(self, x: float, y: float, is_player_bullet: bool = True) -> Bullet:
        """
        Get an inactive bullet from the pool or create a new one.
        
        Args:
            x: Starting x position
            y: Starting y position
            is_player_bullet: True for player bullets, False for enemy bullets
            
        Returns:
            Bullet: An available bullet or None if pool is full
        """
        # Find an inactive bullet
        for bullet in self.bullets:
            if not bullet.active:
                bullet.reset(x, y, is_player_bullet)
                return bullet
        
        # If no inactive bullets and under max, create a new one
        if len(self.bullets) < self.max_bullets:
            bullet = Bullet(x, y, is_player_bullet)
            self.bullets.append(bullet)
            return bullet
        
        return None
    
    def update_all(self, dt: float) -> None:
        """
        Update all active bullets.
        
        Args:
            dt: Delta time in seconds
        """
        for bullet in self.bullets:
            if bullet.active:
                bullet.update(dt)
    
    def render_all(self, surface: pygame.Surface) -> None:
        """
        Render all active bullets.
        
        Args:
            surface: Surface to render on
        """
        for bullet in self.bullets:
            if bullet.active:
                bullet.render(surface)
    
    def get_active_bullets(self) -> list:
        """
        Get all active bullets.
        
        Returns:
            list: List of active bullets
        """
        return [bullet for bullet in self.bullets if bullet.active]
    
    def get_player_bullets(self) -> list:
        """
        Get all active player bullets.
        
        Returns:
            list: List of active player bullets
        """
        return [bullet for bullet in self.bullets if bullet.active and bullet.is_player_bullet]
    
    def get_enemy_bullets(self) -> list:
        """
        Get all active enemy bullets.
        
        Returns:
            list: List of active enemy bullets
        """
        return [bullet for bullet in self.bullets if bullet.active and not bullet.is_player_bullet]
    
    def clear_all(self) -> None:
        """Deactivate all bullets."""
        for bullet in self.bullets:
            bullet.active = False
    
    def clear_enemy_bullets(self) -> None:
        """Deactivate all enemy bullets."""
        for bullet in self.bullets:
            if not bullet.is_player_bullet:
                bullet.active = False
    
    def clear_player_bullets(self) -> None:
        """Deactivate all player bullets."""
        for bullet in self.bullets:
            if bullet.is_player_bullet:
                bullet.active = False
