"""
Play State
Main gameplay state handling all game logic.
"""

import pygame
import random
import math
from src.game.game_state import GameState
from config.constants import *
from src.entities.player import Player
from src.entities.alien import Alien
from src.entities.bullet import Bullet
from src.entities.barrier import Barrier
from src.managers.input_manager import InputManager
from src.managers.score_manager import ScoreManager
from src.managers.formation_manager import FormationManager
from src.managers.collision_manager import CollisionManager

class PlayState(GameState):
    """Main gameplay state with all game systems."""
    
    def __init__(self):
        """Initialize the play state."""
        super().__init__()
        self.name = "play"
        
        # Game systems
        self.input_manager = InputManager()
        self.score_manager = ScoreManager()
        self.formation_manager = FormationManager()
        self.collision_manager = CollisionManager()
        
        # Game entities
        self.player = None
        self.aliens = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.barriers = []
        
        # Game state
        self.current_level = 1
        self.game_time = 0.0
        self.pause_requested = False
        
        # UI
        self.font_small = pygame.font.Font(None, SMALL_FONT_SIZE)
        self.font_medium = pygame.font.Font(None, MEDIUM_FONT_SIZE)
        
        # Initialize game objects
        self._init_game_objects()
    
    def _init_game_objects(self) -> None:
        """Initialize all game objects for a new game."""
        # Create player
        self.player = Player(
            SCREEN_CENTER_X - PLAYER_WIDTH // 2,
            SCREEN_HEIGHT - 80
        )
        
        # Create aliens
        self.aliens = self._create_alien_formation()
        
        # Create barriers
        self.barriers = self._create_barriers()
        
        # Clear bullets
        self.player_bullets = []
        self.enemy_bullets = []
    
    def _create_alien_formation(self) -> list:
        """Create the alien formation for the current level."""
        aliens = []
        
        # Formation positioning
        total_width = (FORMATION_COLS - 1) * FORMATION_HORIZONTAL_SPACING
        start_x = SCREEN_CENTER_X - total_width // 2
        start_y = FORMATION_START_Y
        
        # Create rows of aliens
        for row in range(FORMATION_ROWS):
            for col in range(FORMATION_COLS):
                # Determine alien type based on row
                if row == 0:
                    alien_type = 'small'
                    color = ALIEN_COLORS[0]
                elif row in [1, 2]:
                    alien_type = 'medium'
                    color = ALIEN_COLORS[1]
                else:
                    alien_type = 'large'
                    color = ALIEN_COLORS[2]
                
                # Calculate position
                x = start_x + col * FORMATION_HORIZONTAL_SPACING
                y = start_y + row * FORMATION_VERTICAL_SPACING
                
                # Create alien
                alien = Alien(x, y, alien_type, color)
                aliens.append(alien)
        
        return aliens
    
    def _create_barriers(self) -> list:
        """Create destructible barriers."""
        barriers = []
        spacing = SCREEN_WIDTH // (BARRIER_COUNT + 1)
        
        for i in range(BARRIER_COUNT):
            x = spacing * (i + 1) - BARRIER_WIDTH // 2
            y = BARRIER_START_Y
            barrier = Barrier(x, y)
            barriers.append(barrier)
        
        return barriers
    
    def handle_events(self, event: pygame.event.Event):
        """
        Handle play state events.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            New state name to transition to, or None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_PAUSE:  # ESC to pause
                return 'pause'
        
        return None
    
    def update(self, dt: float) -> None:
        """
        Update the game state.
        
        Args:
            dt: Delta time in seconds
        """
        if dt <= 0:
            return
        
        # Update game time
        self.game_time += dt
        
        # Update input
        self.input_manager.update()
        
        # Update player
        if self.player and self.player.active:
            self.player.update(dt, self.input_manager, SCREEN_WIDTH, SCREEN_HEIGHT)
            
            # Handle shooting
            if self.input_manager.is_key_just_pressed(KEY_SHOOT):
                bullet = self.player.shoot()
                if bullet:
                    self.player_bullets.append(bullet)
        
        # Update alien formation
        if self.aliens:
            self.formation_manager.update_formation(dt, self.aliens, SCREEN_WIDTH)
            
            # Handle alien shooting
            for alien in self.aliens:
                if alien.can_shoot():
                    bullet = alien.shoot()
                    if bullet:
                        self.enemy_bullets.append(bullet)
        
        # Update bullets
        self._update_bullets(dt)
        
        # Handle collisions
        self._handle_collisions()
        
        # Update barriers
        for barrier in self.barriers:
            if barrier.active:
                barrier.update(dt)
        
        # Check game conditions
        self._check_game_conditions()
    
    def _update_bullets(self, dt: float) -> None:
        """Update all bullets."""
        # Update player bullets
        for bullet in self.player_bullets[:]:
            bullet.update(dt)
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.player_bullets.remove(bullet)
        
        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet.update(dt)
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.enemy_bullets.remove(bullet)
    
    def _handle_collisions(self) -> None:
        """Handle all collision detection."""
        # Player bullets vs aliens
        for bullet in self.player_bullets[:]:
            for alien in self.aliens[:]:
                if alien.active and bullet.get_rect().colliderect(alien.get_rect()):
                    # Remove bullet and alien
                    self.player_bullets.remove(bullet)
                    self.aliens.remove(alien)
                    
                    # Award points
                    score_value = ALIEN_SCORES.get(alien.alien_type, 10)
                    self.score_manager.add_points(score_value)
                    
                    break
        
        # Player bullets vs barriers
        for bullet in self.player_bullets[:]:
            for barrier in self.barriers:
                if barrier.active and barrier.check_collision(bullet):
                    self.player_bullets.remove(bullet)
                    break
        
        # Enemy bullets vs player
        if self.player and self.player.active:
            for bullet in self.enemy_bullets[:]:
                if bullet.get_rect().colliderect(self.player.get_rect()):
                    self.enemy_bullets.remove(bullet)
                    self.player.take_damage()
                    if self.player.lives <= 0:
                        self.player.active = False
        
        # Enemy bullets vs barriers
        for bullet in self.enemy_bullets[:]:
            for barrier in self.barriers:
                if barrier.active and barrier.check_collision(bullet):
                    self.enemy_bullets.remove(bullet)
                    break
        
        # Aliens vs player (if aliens reach bottom)
        for alien in self.aliens:
            if self.player and self.player.active:
                if alien.get_rect().colliderect(self.player.get_rect()):
                    self.player.take_damage()
                    if self.player.lives <= 0:
                        self.player.active = False
    
    def _check_game_conditions(self) -> None:
        """Check win/lose conditions."""
        # Check if all aliens are destroyed (victory)
        if not self.aliens:
            return  # Victory state would be handled by external code
        
        # Check if aliens reached the bottom (game over)
        for alien in self.aliens:
            if alien.y >= self.player.y - self.player.height:
                return  # Game over state would be handled by external code
        
        # Check if player is dead
        if self.player and not self.player.active:
            return  # Game over state would be handled by external code
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the game.
        
        Args:
            surface: The pygame surface to render on
        """
        # Clear screen
        surface.fill(BLACK)
        
        # Render game objects
        self._render_game_objects(surface)
        
        # Render UI
        self._render_ui(surface)
    
    def _render_game_objects(self, surface: pygame.Surface) -> None:
        """Render all game objects."""
        # Render player
        if self.player and self.player.active:
            self.player.render(surface)
        
        # Render aliens
        for alien in self.aliens:
            if alien.active:
                alien.render(surface)
        
        # Render bullets
        for bullet in self.player_bullets:
            bullet.render(surface)
        
        for bullet in self.enemy_bullets:
            bullet.render(surface)
        
        # Render barriers
        for barrier in self.barriers:
            if barrier.active:
                barrier.render(surface)
    
    def _render_ui(self, surface: pygame.Surface) -> None:
        """Render the user interface."""
        # Render score
        score_text = self.font_medium.render(f"Score: {self.score_manager.get_score()}", True, SCORE_COLOR)
        surface.blit(score_text, (10, 10))
        
        # Render lives
        if self.player:
            lives_text = self.font_medium.render(f"Lives: {self.player.lives}", True, LIVES_COLOR)
            lives_rect = lives_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
            surface.blit(lives_text, lives_rect)
        
        # Render level
        level_text = self.font_small.render(f"Level: {self.current_level}", True, UI_COLOR)
        level_rect = level_text.get_rect(center=(SCREEN_CENTER_X, 10))
        surface.blit(level_text, level_rect)
        
        # Render controls hint
        if self.game_time < 5.0:  # Show controls for first 5 seconds
            controls = [
                "Arrow Keys: Move",
                "B: Shoot",
                "ESC: Pause"
            ]
            y_pos = SCREEN_HEIGHT - 100
            for control in controls:
                control_text = self.font_small.render(control, True, WHITE)
                surface.blit(control_text, (10, y_pos))
                y_pos += 20
    
    def on_enter(self, game_manager) -> None:
        """Called when entering the play state."""
        # Reset game state
        self.current_level = 1
        self.game_time = 0.0
        self._init_game_objects()
    
    def on_exit(self) -> None:
        """Called when exiting the play state."""
        pass