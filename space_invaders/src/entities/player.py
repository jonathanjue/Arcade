"""
Player Ship Entity
Represents the player-controlled ship with movement and shooting capabilities.
"""

import pygame
import math
from src.base.sprite_object import SpriteObject
from config.constants import *
from src.entities.bullet import Bullet

class Player(SpriteObject):
    """
    Player-controlled ship with 2D movement and shooting.
    
    Attributes:
        lives (int): Remaining lives
        shoot_timer (float): Timer for shooting cooldown
        max_speed (float): Maximum movement speed
        acceleration (float): Movement acceleration
        friction (float): Movement friction
    """
    
    def __init__(self, x: float, y: float):
        """Initialize the player ship."""
        super().__init__(x, y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR)
        
        # Player attributes
        self.lives = PLAYER_LIVES
        self.shoot_timer = 0.0
        self.max_speed = PLAYER_SPEED
        self.acceleration = PLAYER_ACCELERATION
        self.friction = PLAYER_FRICTION
        
        # Animation state
        self.animation_timer = 0.0
        self.current_frame = 0
        self.animation_speed = 1.0 / (PLAYER_ANIMATION_SPEED / 60.0)  # Convert to seconds
        
        # Movement state
        self.prev_x = x
        self.prev_y = y
    
    def update(self, dt: float, input_manager, screen_width: int, screen_height: int) -> None:
        """
        Update the player state.
        
        Args:
            dt: Delta time in seconds
            input_manager: The input manager for handling controls
            screen_width: Screen width for boundary checking
            screen_height: Screen height for boundary checking
        """
        if not self.active:
            return
        
        # Store previous position
        self.prev_x = self.x
        self.prev_y = self.y
        
        # Update movement based on input
        self._handle_movement(input_manager, dt)
        
        # Update shooting
        self._update_shooting(dt)
        
        # Update animation
        self._update_animation(dt)
        
        # Clamp to screen boundaries
        self._clamp_to_screen(screen_width, screen_height)
        
        # Update surface position
        self.update_rect()
    
    def _handle_movement(self, input_manager, dt: float) -> None:
        """Handle player movement based on input."""
        # Horizontal movement
        if input_manager.is_key_pressed(KEY_LEFT):
            self.velocity_x -= self.acceleration * dt
        elif input_manager.is_key_pressed(KEY_RIGHT):
            self.velocity_x += self.acceleration * dt
        else:
            # Apply horizontal friction
            if self.velocity_x > 0:
                self.velocity_x = max(0, self.velocity_x - self.friction * dt)
            elif self.velocity_x < 0:
                self.velocity_x = min(0, self.velocity_x + self.friction * dt)
        
        # Vertical movement
        if input_manager.is_key_pressed(KEY_UP):
            self.velocity_y -= self.acceleration * dt
        elif input_manager.is_key_pressed(KEY_DOWN):
            self.velocity_y += self.acceleration * dt
        else:
            # Apply vertical friction
            if self.velocity_y > 0:
                self.velocity_y = max(0, self.velocity_y - self.friction * dt)
            elif self.velocity_y < 0:
                self.velocity_y = min(0, self.velocity_y + self.friction * dt)
        
        # Clamp velocities
        self.velocity_x = max(-self.max_speed, min(self.max_speed, self.velocity_x))
        self.velocity_y = max(-self.max_speed, min(self.max_speed, self.velocity_y))
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
    
    def _update_shooting(self, dt: float) -> None:
        """Update shooting cooldown and timers."""
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
    
    def _update_animation(self, dt: float) -> None:
        """Update player animation."""
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            self.current_frame = (self.current_frame + 1) % 2  # Simple 2-frame animation
    
    def _clamp_to_screen(self, screen_width: int, screen_height: int) -> None:
        """Keep player within screen boundaries."""
        # Horizontal boundaries
        if self.x < 0:
            self.x = 0
            self.velocity_x = 0
        elif self.x + self.width > screen_width:
            self.x = screen_width - self.width
            self.velocity_x = 0
        
        # Vertical boundaries
        if self.y < 0:
            self.y = 0
            self.velocity_y = 0
        elif self.y + self.height > screen_height:
            self.y = screen_height - self.height
            self.velocity_y = 0
    
    def can_shoot(self) -> bool:
        """Check if the player can shoot."""
        return self.shoot_timer <= 0 and self.active
    
    def shoot(self) -> Bullet:
        """
        Create and return a player bullet.
        
        Returns:
            Bullet: The created bullet or None if cannot shoot
        """
        if not self.can_shoot():
            return None
        
        # Create bullet at player center-top
        bullet_x = self.x + self.width // 2 - BULLET_WIDTH // 2
        bullet_y = self.y - 5
        
        bullet = Bullet(bullet_x, bullet_y, True)  # True for player bullet
        self.shoot_timer = PLAYER_SHOOT_DELAY
        
        return bullet
    
    def take_damage(self) -> None:
        """Handle player taking damage."""
        if self.active:
            self.lives -= 1
            if self.lives <= 0:
                self.active = False
    
    def heal(self, amount: int = 1) -> None:
        """Heal the player."""
        self.lives += amount
    
    def get_movement_direction(self) -> tuple:
        """
        Get the current movement direction.
        
        Returns:
            tuple: (horizontal_direction, vertical_direction)
        """
        h_dir = 0
        v_dir = 0
        
        if self.velocity_x > 50:
            h_dir = 1
        elif self.velocity_x < -50:
            h_dir = -1
        
        if self.velocity_y > 50:
            v_dir = 1
        elif self.velocity_y < -50:
            v_dir = -1
        
        return (h_dir, v_dir)
    
    def is_moving(self) -> bool:
        """Check if the player is currently moving."""
        return abs(self.velocity_x) > 10 or abs(self.velocity_y) > 10
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the player ship."""
        if not self.active:
            return
        
        # Basic rectangle rendering (can be enhanced with sprites)
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw player details (simple pixel art style)
        center_x = self.x + self.width // 2
        
        # Ship body
        pygame.draw.rect(surface, PLAYER_COLOR, (self.x + 5, self.y + 8, self.width - 10, self.height - 16))
        
        # Cockpit
        pygame.draw.rect(surface, PLAYER_ACCENT_COLOR, (center_x - 3, self.y + 4, 6, 8))
        
        # Wing tips
        pygame.draw.rect(surface, PLAYER_ACCENT_COLOR, (self.x, self.y + 12, 3, 4))
        pygame.draw.rect(surface, PLAYER_ACCENT_COLOR, (self.x + self.width - 3, self.y + 12, 3, 4))
        
        # Engine glow effect when moving
        if self.is_moving():
            glow_color = (min(255, self.color[0] + 50), self.color[1], self.color[2])
            engine_y = self.y + self.height - 2
            pygame.draw.rect(surface, glow_color, (center_x - 2, engine_y, 4, 2))
        
        self.update_rect()
    
    def get_score_value(self) -> int:
        """Get the score value for this entity (not applicable to player)."""
        return 0
    
    def reset(self, x: float, y: float) -> None:
        """Reset the player to a new position."""
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.active = True
        self.lives = PLAYER_LIVES
        self.shoot_timer = 0.0