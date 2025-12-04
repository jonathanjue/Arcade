"""
PlayState Class

Handles the main gameplay state.
"""

import pygame
from ..game_state import GameState
import sys
import os
import random
import time
from pygame.math import Vector2
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from constants import BLACK, YELLOW, WHITE, RED, BLUE
from src.base.sprite_object import SpriteObject
from src.entities.simple_enemy import SimpleEnemy
from src.entities.bullet import Bullet

class PlayState(GameState):
    """Main gameplay state for the game."""

    def __init__(self, game_manager):
        """
        Initialize the play state.

        Args:
            game_manager: Reference to the GameManager instance
        """
        super().__init__(game_manager)
        self.set_name("PlayState")
        self.font = pygame.font.SysFont('Arial', 24)

        # Create placeholder Pacman
        self.pacman = SpriteObject(position=(100, 100), size=(30, 30), color=YELLOW)

        # Create enemy
        self.enemy = SimpleEnemy(position=(400, 300))
        self.enemy.set_game_manager(self.game_manager)

        # Game state variables
        self.score = 0
        self.lives = 3
        self.paused = False
        self.game_over_triggered = False

        # Powerup system
        self.powerup_active = False
        self.powerup_start_time = 0
        self.powerup_duration = 5.0  # 5 seconds
        self.powerup_cooldown = 0.0
        self.powerup_cooldown_duration = 1.0  # 1 second cooldown

        # Bullet system
        self.bullets = []
        self.bullet_shoot_timer = 0
        self.bullet_shoot_interval = 0.5  # Shoot every 0.5 seconds

        # Store original colors and speeds
        self.original_pacman_color = YELLOW
        self.original_enemy_speed = self.enemy.speed

    def enter(self):
        """Called when entering the play state."""
        print("Entering PlayState")

    def exit(self):
        """Called when exiting the play state."""
        print("Exiting PlayState")

    def handle_event(self, event):
        """
        Handle pygame events.

        Args:
            event: Pygame event to handle
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_manager.toggle_pause()
            elif event.key == pygame.K_p:
                # Activate powerup
                self.activate_powerup()

    def update(self, dt):
        """
        Update the play state.

        Args:
            dt: Delta time in seconds since last update
        """
        # Skip updates if paused
        if self.game_manager.is_paused():
            return

        # Update powerup cooldown
        if self.powerup_cooldown > 0:
            self.powerup_cooldown -= dt

        # Update powerup timer
        if self.powerup_active:
            if time.time() - self.powerup_start_time >= self.powerup_duration:
                self.deactivate_powerup()

        # Update bullet shoot timer
        self.bullet_shoot_timer += dt

        # Enemy shoots bullets when powerup is active
        if self.powerup_active and self.bullet_shoot_timer >= self.bullet_shoot_interval:
            self.enemy_shoot_bullet()
            self.bullet_shoot_timer = 0

        # Update bullets
        self.update_bullets(dt)

        # Get input direction
        input_manager = self.get_game_manager().input_manager
        direction = input_manager.get_current_direction()

        # Update Pacman position based on direction
        if direction == "up":
            self.pacman.position = (self.pacman.position[0], self.pacman.position[1] - 200 * dt)
        elif direction == "down":
            self.pacman.position = (self.pacman.position[0], self.pacman.position[1] + 200 * dt)
        elif direction == "left":
            self.pacman.position = (self.pacman.position[0] - 200 * dt, self.pacman.position[1])
        elif direction == "right":
            self.pacman.position = (self.pacman.position[0] + 200 * dt, self.pacman.position[1])

        # Update enemy AI (match Pacman speed when powerup active)
        enemy_speed = self.original_enemy_speed
        if self.powerup_active:
            # Enemy moves at same speed as Pacman during powerup
            enemy_speed = 200  # Same as Pacman's movement speed

        # Temporarily adjust enemy speed
        original_speed = self.enemy.speed
        self.enemy.speed = enemy_speed
        self.enemy.update(dt, self.pacman.position)
        self.enemy.speed = original_speed  # Restore original speed

        # Check for collision between Pacman and enemy (only if not invincible)
        if not self.powerup_active:
            self.check_collision()

        # Keep Pacman on screen
        screen_width = self.get_game_manager().screen.get_width()
        screen_height = self.get_game_manager().screen.get_height()

        if self.pacman.position[0] < 0:
            self.pacman.position = (0, self.pacman.position[1])
        elif self.pacman.position[0] > screen_width - self.pacman.size[0]:
            self.pacman.position = (screen_width - self.pacman.size[0], self.pacman.position[1])

        if self.pacman.position[1] < 0:
            self.pacman.position = (self.pacman.position[0], 0)
        elif self.pacman.position[1] > screen_height - self.pacman.size[1]:
            self.pacman.position = (self.pacman.position[0], screen_height - self.pacman.size[1])

    def render(self, screen):
        """
        Render the play state.

        Args:
            screen: Pygame surface to render on
        """
        # Clear screen
        screen.fill(BLACK)

        # Render Pacman
        if self.powerup_active:
            # Draw Pacman in blue when powerup is active
            pacman_rect = pygame.Rect(self.pacman.position, self.pacman.size)
            pygame.draw.rect(screen, BLUE, pacman_rect)

            # Draw "INVINCIBLE" text
            invincible_text = self.font.render("INVINCIBLE", True, WHITE)
            invincible_rect = invincible_text.get_rect(center=pacman_rect.center)
            screen.blit(invincible_text, invincible_rect)
        else:
            self.pacman.render(screen)

        # Render enemy
        self.enemy.render(screen)

        # Render bullets
        for bullet in self.bullets:
            bullet.render(screen)

        # Render score and lives
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))

        # Render powerup status
        if self.powerup_active:
            powerup_time_left = max(0, self.powerup_duration - (time.time() - self.powerup_start_time))
            powerup_text = self.font.render(f"POWERUP: {powerup_time_left:.1f}s", True, YELLOW)
            powerup_rect = powerup_text.get_rect(center=(screen.get_width() // 2, 50))
            screen.blit(powerup_text, powerup_rect)
        elif self.powerup_cooldown > 0:
            cooldown_text = self.font.render(f"COOLDOWN: {self.powerup_cooldown:.1f}s", True, (150, 150, 150))
            cooldown_rect = cooldown_text.get_rect(center=(screen.get_width() // 2, 50))
            screen.blit(cooldown_text, cooldown_rect)

        # Render pause message if paused
        if self.game_manager.is_paused():
            pause_text = self.font.render("PAUSED - Press ESC to continue", True, YELLOW)
            pause_rect = pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(pause_text, pause_rect)

        # Render instructions
        instructions = self.font.render("Arrow keys to move, ESC to pause, P for powerup", True, WHITE)
        instructions_rect = instructions.get_rect(center=(screen.get_width() // 2, screen.get_height() - 30))
        screen.blit(instructions, instructions_rect)

    def add_score(self, points):
        """Add points to the score."""
        self.score += points

    def lose_life(self):
        """Lose a life."""
        self.lives -= 1
        if self.lives <= 0:
            from .game_over_state import GameOverState
            self.get_game_manager().change_state(GameOverState(self.get_game_manager(), self.score))

    def activate_powerup(self):
        """
        Activate the powerup if not on cooldown.
        """
        if self.powerup_cooldown <= 0 and not self.powerup_active:
            print("Powerup activated! Pacman is now invincible!")
            self.powerup_active = True
            self.powerup_start_time = time.time()
            self.powerup_cooldown = self.powerup_cooldown_duration

            # Change Pacman color to blue
            self.pacman.color = BLUE

            # Store original enemy speed
            self.original_enemy_speed = self.enemy.speed

    def deactivate_powerup(self):
        """
        Deactivate the powerup.
        """
        print("Powerup deactivated!")
        self.powerup_active = False

        # Restore Pacman color
        self.pacman.color = self.original_pacman_color

        # Clear all bullets when powerup ends
        self.bullets.clear()

    def enemy_shoot_bullet(self):
        """
        Make the enemy shoot a bullet towards Pacman.
        """
        if len(self.bullets) < 10:  # Limit number of bullets
            # Calculate direction from enemy to Pacman
            direction = Vector2(self.pacman.position) - Vector2(self.enemy.position)
            if direction.length() > 0:
                direction = direction.normalize()

            # Create bullet at enemy position
            bullet = Bullet(
                position=(self.enemy.position[0] + self.enemy.size[0]//2,
                          self.enemy.position[1] + self.enemy.size[1]//2),
                direction=direction
            )
            self.bullets.append(bullet)
            print(f"Enemy shot bullet! Total bullets: {len(self.bullets)}")

    def update_bullets(self, dt):
        """
        Update all active bullets.
        """
        active_bullets = []
        for bullet in self.bullets:
            bullet.update(dt)
            if bullet.active:
                active_bullets.append(bullet)
            else:
                # Check if bullet hit Pacman (only if not invincible)
                if not self.powerup_active:
                    self.check_bullet_collision(bullet)

        self.bullets = active_bullets

    def check_bullet_collision(self, bullet):
        """
        Check if bullet hit Pacman.
        """
        bullet_rect = pygame.Rect(bullet.position, bullet.size)
        pacman_rect = pygame.Rect(self.pacman.position, self.pacman.size)

        if bullet_rect.colliderect(pacman_rect):
            print("Bullet hit Pacman!")
            self.lose_life()

    def check_collision(self):
        """
        Check for collision between Pacman and enemy.
        If collision detected, trigger game over.
        """
        # Simple bounding box collision detection
        pacman_rect = pygame.Rect(self.pacman.position, self.pacman.size)
        enemy_rect = pygame.Rect(self.enemy.position, self.enemy.size)

        if pacman_rect.colliderect(enemy_rect) and not self.game_over_triggered:
            print("Collision detected! You die!")
            self.game_over_triggered = True
            from .game_over_state import GameOverState
            self.get_game_manager().change_state(GameOverState(self.get_game_manager(), self.score))

    def on_pause_changed(self, is_paused):
        """
        Handle pause state changes.
        """
        self.paused = is_paused
        print(f"PlayState pause state changed to: {is_paused}")