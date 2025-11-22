"""
Barrier Entities
Represents destructible barriers in the Space Invaders game with individual block management.
"""

import pygame
from src.base.sprite_object import SpriteObject
from config.constants import *


class BarrierBlock(SpriteObject):
    """
    Individual destructible block within a barrier.
    
    Attributes:
        health (int): Current health (4 = 100%, 3 = 75%, 2 = 50%, 1 = 25%, 0 = 0%)
        max_health (int): Maximum health value
        grid_x (int): X position within the barrier grid
        grid_y (int): Y position within the barrier grid
        damage_timer (float): Timer for damage effects
    """
    
    def __init__(self, x: float, y: float, grid_x: int, grid_y: int):
        """Initialize a barrier block."""
        super().__init__(x, y, BARRIER_BLOCK_SIZE, BARRIER_BLOCK_SIZE, BARRIER_COLOR)
        
        # Health system
        self.max_health = 4
        self.health = self.max_health
        
        # Grid position
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        # Damage effects
        self.damage_timer = 0.0
        
        # Set initial color based on health
        self._update_color()
    
    def take_damage(self, damage: int = 1) -> bool:
        """
        Apply damage to the block.
        
        Args:
            damage: Amount of damage to apply
            
        Returns:
            bool: True if block was destroyed, False otherwise
        """
        if not self.active:
            return False
        
        self.health -= damage
        self.damage_timer = BARRIER_DAMAGE_INTERVAL
        
        if self.health <= 0:
            self.health = 0
            self.active = False
            return True
        else:
            self._update_color()
            return False
    
    def heal(self, amount: int = 1) -> None:
        """
        Heal the block.
        
        Args:
            amount: Amount of health to restore
        """
        if not self.active:
            return
        
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        
        if old_health != self.health:
            self._update_color()
    
    def is_destroyed(self) -> bool:
        """Check if the block is completely destroyed."""
        return not self.active or self.health <= 0
    
    def get_health_percentage(self) -> float:
        """Get current health as a percentage."""
        if self.max_health <= 0:
            return 0.0
        return max(0.0, min(1.0, self.health / self.max_health))
    
    def get_damage_state(self) -> int:
        """
        Get the current damage state for color mapping.
        
        Returns:
            int: 0 = perfect, 1 = 75%, 2 = 50%, 3 = 25%, 4 = destroyed
        """
        if self.is_destroyed():
            return 4
        
        percentage = self.get_health_percentage()
        if percentage >= 0.75:
            return 0
        elif percentage >= 0.5:
            return 1
        elif percentage >= 0.25:
            return 2
        else:
            return 3
    
    def _update_color(self) -> None:
        """Update the block color based on current health."""
        damage_state = self.get_damage_state()
        if damage_state < len(BARRIER_DAMAGE_COLORS):
            self.set_color(BARRIER_DAMAGE_COLORS[damage_state])
    
    def update(self, dt: float) -> None:
        """Update the block state."""
        if not self.active:
            return
        
        # Update damage timer
        if self.damage_timer > 0:
            self.damage_timer -= dt
            if self.damage_timer <= 0:
                self.damage_timer = 0
                self._update_color()
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the block with damage effects."""
        if not self.active:
            return
        
        # Draw the main block
        pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.width, self.height))
        
        # Add damage highlighting effect
        if self.damage_timer > 0:
            highlight_color = (min(255, self.color[0] + 100), 
                             min(255, self.color[1] + 100), 
                             min(255, self.color[2] + 100))
            pygame.draw.rect(surface, highlight_color, 
                           (int(self.x), int(self.y), self.width, self.height), 1)
        
        # Add border for intact blocks
        if self.health == self.max_health:
            pygame.draw.rect(surface, BARRIER_HIGHLIGHT, 
                           (int(self.x), int(self.y), self.width, self.height), 1)
        
        self.update_rect()
    
    def check_collision(self, other_rect: pygame.Rect) -> bool:
        """
        Check collision with another rectangle.
        
        Args:
            other_rect: Rectangle to check collision with
            
        Returns:
            bool: True if collision detected
        """
        if not self.active:
            return False
        
        return self.rect.colliderect(other_rect)


class Barrier(SpriteObject):
    """
    Collection of barrier blocks arranged in a grid formation.
    
    Attributes:
        blocks (list): 2D list of BarrierBlock objects
        total_blocks (int): Total number of blocks in the barrier
        active_blocks (int): Number of currently active blocks
        barrier_x (float): X position of the barrier
        barrier_y (float): Y position of the barrier
    """
    
    def __init__(self, x: float, y: float):
        """Initialize a barrier with a grid of blocks."""
        super().__init__(x, y, BARRIER_WIDTH, BARRIER_HEIGHT, BARRIER_COLOR)
        
        self.barrier_x = x
        self.barrier_y = y
        self.blocks = []
        self.total_blocks = 0
        self.active_blocks = 0
        
        # Create the grid of blocks
        self._create_blocks()
    
    def _create_blocks(self) -> None:
        """Create the grid of barrier blocks."""
        self.blocks = []
        
        for row in range(BARRIER_ROWS):
            block_row = []
            for col in range(BARRIER_COLS):
                # Calculate block position
                block_x = self.barrier_x + (col * BARRIER_BLOCK_SIZE)
                block_y = self.barrier_y + (row * BARRIER_BLOCK_SIZE)
                
                # Create block
                block = BarrierBlock(block_x, block_y, col, row)
                block_row.append(block)
            
            self.blocks.append(block_row)
        
        # Count total blocks
        self.total_blocks = sum(len(row) for row in self.blocks)
        self.active_blocks = self.total_blocks
    
    def update(self, dt: float) -> None:
        """Update all barrier blocks."""
        for row in self.blocks:
            for block in row:
                block.update(dt)
        
        # Update active block count
        self.active_blocks = sum(1 for row in self.blocks for block in row if block.active)
    
    def check_bullet_collision(self, bullet_rect: pygame.Rect) -> tuple:
        """
        Check collision with a bullet and return affected block.
        
        Args:
            bullet_rect: Rectangle representing the bullet
            
        Returns:
            tuple: (collision_detected, hit_block, bullet_destroyed)
        """
        collision_detected = False
        hit_block = None
        bullet_destroyed = False
        
        for row in self.blocks:
            for block in row:
                if block.check_collision(bullet_rect):
                    collision_detected = True
                    hit_block = block
                    
                    # Apply damage to the block
                    if block.take_damage(1):
                        self.active_blocks -= 1
                    
                    bullet_destroyed = True
                    break
            
            if collision_detected:
                break
        
        return collision_detected, hit_block, bullet_destroyed
    
    def get_intact_blocks(self) -> list:
        """
        Get all intact (non-destroyed) blocks.
        
        Returns:
            list: List of active BarrierBlock objects
        """
        return [block for row in self.blocks for block in row if block.active]
    
    def get_destroyed_percentage(self) -> float:
        """
        Get the percentage of destroyed blocks.
        
        Returns:
            float: Percentage destroyed (0.0 to 1.0)
        """
        if self.total_blocks <= 0:
            return 0.0
        
        destroyed_blocks = self.total_blocks - self.active_blocks
        return destroyed_blocks / self.total_blocks
    
    def is_completely_destroyed(self) -> bool:
        """Check if all blocks in the barrier are destroyed."""
        return self.active_blocks <= 0
    
    def get_integrity_level(self) -> str:
        """
        Get the overall integrity level of the barrier.
        
        Returns:
            str: "intact", "damaged", "heavily_damaged", or "destroyed"
        """
        if self.is_completely_destroyed():
            return "destroyed"
        
        percentage_destroyed = self.get_destroyed_percentage()
        
        if percentage_destroyed < 0.25:
            return "intact"
        elif percentage_destroyed < 0.5:
            return "damaged"
        elif percentage_destroyed < 0.75:
            return "heavily_damaged"
        else:
            return "destroyed"
    
    def render(self, surface: pygame.Surface) -> None:
        """Render all active barrier blocks."""
        for row in self.blocks:
            for block in row:
                block.render(surface)
    
    def get_bounding_rect(self) -> pygame.Rect:
        """
        Get the bounding rectangle of the entire barrier.
        
        Returns:
            pygame.Rect: Rectangle representing the barrier bounds
        """
        return pygame.Rect(self.barrier_x, self.barrier_y, BARRIER_WIDTH, BARRIER_HEIGHT)
    
    def reset(self, x: float, y: float) -> None:
        """
        Reset the barrier to a new position.
        
        Args:
            x: New x position
            y: New y position
        """
        self.barrier_x = x
        self.barrier_y = y
        self._create_blocks()
    
    def heal_all_blocks(self, amount: int = 1) -> None:
        """
        Heal all blocks in the barrier.
        
        Args:
            amount: Amount of health to restore to each block
        """
        for row in self.blocks:
            for block in row:
                if block.active:
                    block.heal(amount)
        
        # Update active block count
        self.active_blocks = sum(1 for row in self.blocks for block in row if block.active)


class BarrierManager:
    """
    Manages multiple barriers positioned across the screen.
    
    Attributes:
        barriers (list): List of Barrier objects
        screen_width (int): Width of the game screen
    """
    
    def __init__(self, screen_width: int):
        """Initialize the barrier manager."""
        self.screen_width = screen_width
        self.barriers = []
        self._create_barriers()
    
    def _create_barriers(self) -> None:
        """Create barriers positioned across the screen."""
        self.barriers = []
        
        # Calculate spacing between barriers
        total_barrier_width = BARRIER_COUNT * BARRIER_WIDTH
        available_space = self.screen_width - total_barrier_width
        spacing = available_space // (BARRIER_COUNT + 1)
        
        # Position barriers equally spaced
        for i in range(BARRIER_COUNT):
            barrier_x = spacing + (i * (BARRIER_WIDTH + spacing))
            barrier_y = BARRIER_START_Y
            
            barrier = Barrier(barrier_x, barrier_y)
            self.barriers.append(barrier)
    
    def update(self, dt: float) -> None:
        """Update all barriers."""
        for barrier in self.barriers:
            barrier.update(dt)
    
    def check_bullet_collisions(self, bullet_rect: pygame.Rect) -> tuple:
        """
        Check bullet collision with any barrier.
        
        Args:
            bullet_rect: Rectangle representing the bullet
            
        Returns:
            tuple: (collision_detected, hit_barrier, hit_block)
        """
        for barrier in self.barriers:
            collision_detected, hit_block, bullet_destroyed = barrier.check_bullet_collision(bullet_rect)
            if collision_detected:
                return True, barrier, hit_block
        
        return False, None, None
    
    def render(self, surface: pygame.Surface) -> None:
        """Render all barriers."""
        for barrier in self.barriers:
            barrier.render(surface)
    
    def get_active_barriers(self) -> list:
        """
        Get all barriers that are not completely destroyed.
        
        Returns:
            list: List of active Barrier objects
        """
        return [barrier for barrier in self.barriers if not barrier.is_completely_destroyed()]
    
    def get_barrier_count(self) -> int:
        """Get the number of barriers."""
        return len(self.barriers)
    
    def get_total_active_blocks(self) -> int:
        """
        Get the total number of active blocks across all barriers.
        
        Returns:
            int: Total active blocks
        """
        return sum(barrier.active_blocks for barrier in self.barriers)
    
    def get_total_blocks(self) -> int:
        """
        Get the total number of blocks across all barriers.
        
        Returns:
            int: Total blocks
        """
        return sum(barrier.total_blocks for barrier in self.barriers)
    
    def is_all_destroyed(self) -> bool:
        """Check if all barriers are completely destroyed."""
        return all(barrier.is_completely_destroyed() for barrier in self.barriers)
    
    def reset(self) -> None:
        """Reset all barriers to their initial state."""
        self._create_barriers()
    
    def get_barrier_at_position(self, x: float, y: float) -> Barrier:
        """
        Get the barrier at a specific position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Barrier: The barrier at the position or None
        """
        for barrier in self.barriers:
            if barrier.get_bounding_rect().collidepoint(x, y):
                return barrier
        return None
    
    def heal_all_barriers(self, amount: int = 1) -> None:
        """
        Heal all blocks in all barriers.
        
        Args:
            amount: Amount of health to restore to each block
        """
        for barrier in self.barriers:
            barrier.heal_all_blocks(amount)