import pygame
import time
import math
import random

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, SPEED_INDICATOR_COLOR, TIME_INDICATOR_COLOR, GREEN, YELLOW, RED, PARTICLE_COUNT, SCREEN_SHAKE_DURATION, SCREEN_SHAKE_INTENSITY, START, PLAYING, GAME_OVER, VICTORY, PAUSED
from player import Player
from target import Target
from particle import ParticleSystem

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()

        # Initialize game objects
        self.player = None
        self.target = None
        self.targets = []  # Keep for future multiple targets

        # Game state management
        self.game_state = START  # Initial state
        self.score = 0
        self.game_over = False
        self.victory = False
        self.paused = False  # Pause state
        self.start_time = time.time()
        self.win_score = 50  # Win condition: reach 50 points
        self.max_speed_reached = False  # Game over condition

        # Command system variables
        self.command_input = ""  # Current command being typed
        self.command_active = False  # Whether command input is active
        self.speed_cheat_active = False  # Track SPEED command state
        self.normal_player_speed = None  # Store normal speed for cheat deactivation

        # Visual effects
        self.particle_system = ParticleSystem()
        self.screen_shake = 0
        self.shake_intensity = 0

        # Font initialization for score display
        self.font = pygame.font.SysFont('Arial', 36)

        # Initialize game objects
        self._initialize_game_objects()

    def _initialize_game_objects(self):
        """Initialize player and initial targets"""
        # Create player at bottom center of screen
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

        # Create initial target
        self.target = Target()

    def _create_target(self):
        """Create a new target at random position"""
        # This will be implemented in full game logic
        pass

    def update(self):
        """Update game state"""
        if self.game_state == START:
            return  # No updates needed for start screen

        if self.game_state == GAME_OVER or self.game_state == VICTORY:
            return

        # When paused, only update visual effects but not game logic
        if not self.paused:
            # Update player
            if self.player:
                self.player.update()

            # Update target
            if self.target:
                self.target.update()

            # Update targets list (for future multiple targets)
            for target in self.targets:
                target.update()

            # Check collisions (placeholder)
            self._check_collisions()

            # Check win condition
            self._check_win_condition()

            # Check game over condition (target speed reaches maximum)
            self._check_game_over_condition()

        # Always update visual effects (particles, screen shake) even when paused
        # Update particle system
        self.particle_system.update()

        # Update screen shake effect
        if self.screen_shake > 0:
            self.screen_shake -= 1
            if self.screen_shake <= 0:
                self.shake_intensity = 0

    def _check_collisions(self):
        """Check for collisions between player and targets"""
        try:
            if self.player and self.target and hasattr(self.player, 'rect') and hasattr(self.target, 'rect'):
                # Check collision between player and target using pygame.Rect.colliderect()
                if self.player.rect.colliderect(self.target.rect):
                    self._handle_collision()
        except Exception as e:
            print(f"Error in collision detection: {e}")
            # Continue game if there's an error

    def _handle_collision(self):
        """Handle collision response between player and target"""
        # Respawn target to new random position
        self.target.respawn()

        # Increase player's score
        self._increase_score()

        # Speed increase is now handled in target.respawn() method

        # Add visual effects: particle explosion and screen shake
        self._add_collision_effects()

    def _add_collision_effects(self):
        """Add visual effects for collision"""
        # Spawn particles at collision position
        collision_x = self.player.rect.centerx
        collision_y = self.player.rect.centery
        self.particle_system.spawn_particles(collision_x, collision_y, self.target.color, PARTICLE_COUNT)

        # Add screen shake effect
        self.screen_shake = SCREEN_SHAKE_DURATION
        self.shake_intensity = SCREEN_SHAKE_INTENSITY

    def _increase_score(self):
        """Increase the player's score"""
        self.score += 1

    def _check_win_condition(self):
        """Check if player has reached the win condition"""
        if self.score >= self.win_score:
            self.victory = True
            self.game_state = VICTORY
            # Record the end time for calculating total time taken
            self.end_time = time.time()

    def _check_game_over_condition(self):
        """Check if game over condition is met - currently disabled as per user request"""
        # Game over condition removed - players cannot fail in this game
        pass

    def render(self):
        """Render game objects"""
        if self.game_state == START:
            self.render_start_screen()
            return
        elif self.game_state == VICTORY:
            self.render_victory_screen()
            return
        elif self.game_state == GAME_OVER:
            self.render_game_over_screen()
            return
        elif self.paused:
            self.render_pause_screen()
            return

        # Apply screen shake effect
        shake_offset_x, shake_offset_y = self._get_shake_offset()

        # Clear screen
        self.screen.fill(BLACK)

        # Draw background elements
        self._draw_background()

        # Draw player with shake offset
        if self.player:
            self.player.draw(self.screen)

        # Draw target with shake offset
        if self.target:
            self.target.draw(self.screen)

        # Draw targets list (for future multiple targets)
        for target in self.targets:
            target.draw(self.screen)

        # Draw particles (not affected by shake for better visual effect)
        self.particle_system.draw(self.screen)

        # Draw score (placeholder)
        self._draw_score()

    def _get_shake_offset(self):
        """Get screen shake offset based on current shake intensity"""
        if self.screen_shake > 0:
            # Calculate shake offset based on remaining shake duration
            shake_factor = self.screen_shake / SCREEN_SHAKE_DURATION
            max_offset = self.shake_intensity * shake_factor
            return random.uniform(-max_offset, max_offset), random.uniform(-max_offset, max_offset)
        return 0, 0

    def _draw_background(self):
        """Draw decorative background elements with parallax scrolling"""
        # Draw parallax layers
        self._draw_parallax_background()

        # Draw stars on top of parallax
        self._draw_stars()

        # Draw grid
        self._draw_grid()

    def _draw_parallax_background(self):
        """Draw parallax scrolling background layers"""
        # Initialize parallax layers if they don't exist
        if not hasattr(self, 'parallax_layers'):
            self._initialize_parallax_layers()

        # Update parallax layer positions
        self._update_parallax_layers()

        # Draw each parallax layer
        for i, layer in enumerate(self.parallax_layers):
            self._draw_parallax_layer(layer, i)

    def _initialize_parallax_layers(self):
        """Initialize parallax background layers"""
        from constants import PARALLAX_LAYERS, PARALLAX_SPEEDS

        self.parallax_layers = []
        self.parallax_positions = []

        # Create multiple layers with different star densities and sizes
        for i in range(PARALLAX_LAYERS):
            layer_stars = []
            # Create stars for this layer
            for _ in range(100):  # Stars per layer
                x = random.randint(0, SCREEN_WIDTH * 2)  # Wider area for scrolling
                y = random.randint(0, SCREEN_HEIGHT)
                size = random.uniform(1, 3)  # Star size
                brightness = random.randint(50, 200)
                color = (brightness, brightness, brightness)
                layer_stars.append((x, y, size, color))

            self.parallax_layers.append(layer_stars)
            self.parallax_positions.append(0)  # Starting position

    def _update_parallax_layers(self):
        """Update parallax layer positions for scrolling effect"""
        from constants import PARALLAX_SPEEDS

        # Move each layer at different speeds
        for i in range(len(self.parallax_positions)):
            self.parallax_positions[i] += PARALLAX_SPEEDS[i % len(PARALLAX_SPEEDS)]

            # Reset position when it goes beyond screen width
            if self.parallax_positions[i] > SCREEN_WIDTH:
                self.parallax_positions[i] = 0

    def _draw_parallax_layer(self, layer_stars, layer_index):
        """Draw a single parallax layer"""
        from constants import PARALLAX_SPEEDS

        # Get current position for this layer
        position = self.parallax_positions[layer_index]

        # Draw stars in this layer with wrap-around for continuous scrolling
        for star in layer_stars:
            x, y, size, color = star

            # Calculate wrapped position
            wrapped_x = (x - position) % (SCREEN_WIDTH * 2)

            # Only draw stars that are on screen
            if 0 <= wrapped_x <= SCREEN_WIDTH:
                # Draw star with some transparency for depth effect
                star_surface = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
                pygame.draw.circle(star_surface, (*color[:3], 150), (int(size), int(size)), int(size))
                self.screen.blit(star_surface, (int(wrapped_x), int(y)))

    def _draw_stars(self):
        """Draw decorative stars in the background"""
        # Create a star pattern
        for i in range(0, SCREEN_WIDTH, 50):
            for j in range(0, SCREEN_HEIGHT, 50):
                # Random brightness for twinkling effect
                brightness = random.randint(100, 200)
                color = (brightness, brightness, brightness)

                # Draw small stars
                pygame.draw.circle(self.screen, color, (i, j), 2)

                # Occasionally draw larger stars
                if random.random() < 0.1:
                    pygame.draw.circle(self.screen, color, (i + 10, j + 10), 3)

    def _draw_grid(self):
        """Draw a subtle grid pattern in the background"""
        # Draw faint grid lines
        grid_color = (30, 30, 50)  # Dark blue grid

        # Horizontal lines
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(self.screen, grid_color, (0, y), (SCREEN_WIDTH, y), 1)

        # Vertical lines
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)

    def _draw_score(self):
        """Draw the current score with label in top-left corner"""
        # Create score text with label
        score_text = f"Score: {self.score}"

        # Render score text with white color for visibility on black background
        score_surface = self.font.render(score_text, True, WHITE)

        # Position score in top-left corner with some padding
        score_rect = score_surface.get_rect()
        score_rect.topleft = (20, 20)

        # Draw score on screen
        self.screen.blit(score_surface, score_rect)

        # Draw speed indicator
        self._draw_speed_indicator()

        # Draw time indicator in top-right corner
        self._draw_time_indicator()

    def _draw_speed_indicator(self):
        """Draw speed indicator to show current target speed"""
        if self.target:
            speed = self.target.get_speed()
            speed_text = f"Speed: {speed:.1f}"

            # Render speed text
            speed_surface = self.font.render(speed_text, True, SPEED_INDICATOR_COLOR)

            # Position speed indicator below score
            speed_rect = speed_surface.get_rect()
            speed_rect.topleft = (20, 60)

            # Draw speed indicator on screen
            self.screen.blit(speed_surface, speed_rect)

            # Visual feedback: change color based on speed level
            if speed > 10:
                # High speed - red warning color
                pygame.draw.rect(self.screen, (255, 50, 50), speed_rect.inflate(10, 5), 2)
            elif speed > 5:
                # Medium speed - yellow warning color
                pygame.draw.rect(self.screen, (255, 255, 50), speed_rect.inflate(10, 5), 2)

    def _draw_time_indicator(self):
        """Draw time indicator to show elapsed game time"""
        # Calculate elapsed time
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        # Format time as minutes:seconds
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_text = f"Time: {minutes:02d}:{seconds:02d}"

        # Render time text
        time_surface = self.font.render(time_text, True, TIME_INDICATOR_COLOR)

        # Position time indicator in top-right corner
        time_rect = time_surface.get_rect()
        time_rect.topright = (SCREEN_WIDTH - 20, 20)

        # Draw time indicator on screen
        self.screen.blit(time_surface, time_rect)

    def render_pause_screen(self):
        """Render the pause screen with enhanced visual feedback"""
        # Draw background with dimming effect
        self._draw_pause_background()

        # Create pause message with animation
        pause_font = pygame.font.SysFont('Arial', 72, bold=True)
        pause_text = pause_font.render("PAUSED", True, YELLOW)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Create resume instruction with visual feedback
        resume_font = pygame.font.SysFont('Arial', 36)
        resume_text = resume_font.render("Press ESC to Resume", True, WHITE)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))

        # Add visual feedback elements
        self._draw_pause_visual_feedback()

        # Draw command prompt if command input is active
        if self.command_active:
            # Draw command prompt
            command_prompt = pygame.font.SysFont('Arial', 24).render("Command: " + self.command_input, True, WHITE)
            command_rect = command_prompt.get_rect(topleft=(20, 20))
            self.screen.blit(command_prompt, command_rect)

            # Draw command instructions
            instructions = [
                "Type commands and press ENTER:",
                "SPEED - Toggle player speed cheat",
                "ESC - Resume game"
            ]

            for i, instruction in enumerate(instructions):
                instruction_text = pygame.font.SysFont('Arial', 20).render(instruction, True, (200, 200, 200))
                instruction_rect = instruction_text.get_rect(topleft=(20, 60 + i * 25))
                self.screen.blit(instruction_text, instruction_rect)

        # Draw all elements
        self.screen.blit(pause_text, pause_rect)
        self.screen.blit(resume_text, resume_rect)

    def _draw_pause_background(self):
        """Draw pause screen background with dimming effect"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))

        # Draw paused game state in background (dimmed)
        self._draw_dimmed_game_state()

    def _draw_dimmed_game_state(self):
        """Draw the current game state dimmed in the background"""
        # Save current screen state
        temp_surface = self.screen.copy()

        # Draw dimmed game elements
        if self.player:
            dimmed_color = (*WHITE[:3], 80)  # Add transparency
            player_surface = pygame.Surface((self.player.width, self.player.height), pygame.SRCALPHA)
            player_surface.fill(dimmed_color)
            self.screen.blit(player_surface, (self.player.x, self.player.y))

        if self.target:
            dimmed_color = (*self.target.color[:3], 80)  # Add transparency
            target_surface = pygame.Surface((self.target.width, self.target.height), pygame.SRCALPHA)
            target_surface.fill(dimmed_color)
            self.screen.blit(target_surface, (self.target.x, self.target.y))

        # Restore screen
        self.screen.blit(temp_surface, (0, 0))

    def _draw_pause_visual_feedback(self):
        """Draw visual feedback elements for pause screen"""
        # Draw pulsing border around pause text
        self._draw_pulsing_border(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 200, 100)

        # Draw animated particles around the screen edges
        self._draw_edge_particles()

    def _draw_pulsing_border(self, center_x, center_y, width, height):
        """Draw a pulsing border around a rectangular area"""
        # Initialize pulse animation if not exists
        if not hasattr(self, 'pause_pulse_scale'):
            self.pause_pulse_scale = 1.0
            self.pause_pulse_direction = 1

        # Update pulse animation
        self.pause_pulse_scale += 0.05 * self.pause_pulse_direction
        if self.pause_pulse_scale >= 1.2 or self.pause_pulse_scale <= 0.8:
            self.pause_pulse_direction *= -1

        # Calculate border rectangle
        border_rect = pygame.Rect(
            center_x - width // 2 - 20,
            center_y - height // 2 - 20,
            width + 40,
            height + 40
        )

        # Draw pulsing border
        pulse_width = int(3 * self.pause_pulse_scale)
        pygame.draw.rect(self.screen, YELLOW, border_rect, pulse_width)

    def _draw_edge_particles(self):
        """Draw animated particles around screen edges"""
        # Draw particles along top and bottom edges
        for i in range(0, SCREEN_WIDTH, 30):
            # Top edge particles
            if random.random() < 0.3:
                color = (random.randint(100, 200), random.randint(100, 200), 255)
                pygame.draw.circle(self.screen, color, (i, 20), 3)

            # Bottom edge particles
            if random.random() < 0.3:
                color = (random.randint(100, 200), random.randint(100, 200), 255)
                pygame.draw.circle(self.screen, color, (i, SCREEN_HEIGHT - 20), 3)

        # Draw particles along left and right edges
        for j in range(0, SCREEN_HEIGHT, 30):
            # Left edge particles
            if random.random() < 0.3:
                color = (random.randint(100, 200), random.randint(100, 200), 255)
                pygame.draw.circle(self.screen, color, (20, j), 3)

            # Right edge particles
            if random.random() < 0.3:
                color = (random.randint(100, 200), random.randint(100, 200), 255)
                pygame.draw.circle(self.screen, color, (SCREEN_WIDTH - 20, j), 3)

    def render_victory_screen(self):
        """Render the victory screen with enhanced visual feedback"""
        # Draw victory background with effects
        self._draw_victory_background()

        # Calculate time taken
        time_taken = self.end_time - self.start_time
        minutes = int(time_taken // 60)
        seconds = int(time_taken % 60)

        # Create victory message with animation
        victory_font = pygame.font.SysFont('Arial', 72, bold=True)
        victory_text = victory_font.render("You Win!", True, GREEN)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

        # Create score text
        score_font = pygame.font.SysFont('Arial', 48)
        score_text = score_font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Create time text
        time_text = score_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))

        # Create restart instruction
        restart_font = pygame.font.SysFont('Arial', 36)
        restart_text = restart_font.render("Press R to Restart", True, YELLOW)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))

        # Add victory visual effects
        self._draw_victory_effects()

        # Draw all elements
        self.screen.blit(victory_text, victory_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(time_text, time_rect)
        self.screen.blit(restart_text, restart_rect)

    def render_start_screen(self):
        """Render the start screen with game title and instructions"""
        # Draw start screen background
        self._draw_start_background()

        # Create title with attractive styling
        title_font = pygame.font.SysFont('Arial', 72, bold=True)
        title_text = title_font.render("Color Catch", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

        # Create instructions
        instructions_font = pygame.font.SysFont('Arial', 24)
        instructions_lines = [
            "Catch the colored targets to score points!",
            "Use LEFT and RIGHT arrow keys to move",
            "Avoid letting targets reach maximum speed!",
            "Reach 50 points to win!"
        ]

        # Create "Press SPACE to Start" prompt with pulsing animation
        start_font = pygame.font.SysFont('Arial', 36)
        start_text = start_font.render("Press SPACE to Start", True, GREEN)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

        # Draw all elements
        self.screen.blit(title_text, title_rect)

        # Draw instructions
        for i, line in enumerate(instructions_lines):
            instruction_text = instructions_font.render(line, True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + i * 30))
            self.screen.blit(instruction_text, instruction_rect)

        # Draw start prompt with pulsing animation
        self._draw_pulsing_start_prompt(start_text, start_rect)

    def _draw_start_background(self):
        """Draw start screen background with decorative elements"""
        # Create gradient background
        self._draw_start_gradient()

        # Draw decorative stars
        self._draw_start_stars()

    def _draw_start_gradient(self):
        """Draw a gradient background for start screen"""
        # Create gradient surface
        gradient = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Draw vertical gradient from dark blue to black
        for y in range(SCREEN_HEIGHT):
            # Calculate color based on position
            intensity = 255 * (1 - y / SCREEN_HEIGHT)
            color = (0, 0, int(intensity * 0.3))
            pygame.draw.line(gradient, color, (0, y), (SCREEN_WIDTH, y))

        self.screen.blit(gradient, (0, 0))

    def _draw_start_stars(self):
        """Draw decorative stars for start screen"""
        # Draw twinkling stars
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(100, 200)
            color = (brightness, brightness, brightness)
            size = random.randint(1, 3)

            pygame.draw.circle(self.screen, color, (x, y), size)

    def _draw_pulsing_start_prompt(self, text_surface, text_rect):
        """Draw pulsing animation for start prompt"""
        # Initialize pulse animation if not exists
        if not hasattr(self, 'start_pulse_scale'):
            self.start_pulse_scale = 1.0
            self.start_pulse_direction = 1

        # Update pulse animation
        self.start_pulse_scale += 0.03 * self.start_pulse_direction
        if self.start_pulse_scale >= 1.2 or self.start_pulse_scale <= 0.8:
            self.start_pulse_direction *= -1

        # Create scaled version of the text
        scaled_width = int(text_surface.get_width() * self.start_pulse_scale)
        scaled_height = int(text_surface.get_height() * self.start_pulse_scale)
        scaled_surface = pygame.transform.scale(text_surface, (scaled_width, scaled_height))

        # Position scaled text
        scaled_rect = scaled_surface.get_rect(center=text_rect.center)

        # Draw the pulsing text
        self.screen.blit(scaled_surface, scaled_rect)

    def render_game_over_screen(self):
        """Render the game over screen with final score and restart option"""
        # Draw game over background
        self._draw_game_over_background()

        # Calculate time played
        time_played = self.end_time - self.start_time
        minutes = int(time_played // 60)
        seconds = int(time_played % 60)

        # Create game over message
        game_over_font = pygame.font.SysFont('Arial', 72, bold=True)
        game_over_text = game_over_font.render("Game Over", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

        # Create final score text
        score_font = pygame.font.SysFont('Arial', 48)
        score_text = score_font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Create time played text
        time_text = score_font.render(f"Time Played: {minutes:02d}:{seconds:02d}", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))

        # Create high score text (placeholder - would need high score tracking)
        high_score_text = score_font.render(f"High Score: {self.score}", True, YELLOW)  # Use actual score
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))

        # Create restart instruction
        restart_font = pygame.font.SysFont('Arial', 36)
        restart_text = restart_font.render("Press R to Restart", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180))

        # Draw all elements
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(time_text, time_rect)
        self.screen.blit(high_score_text, high_score_rect)
        self.screen.blit(restart_text, restart_rect)

    def _draw_game_over_background(self):
        """Draw game over screen background with special effects"""
        # Create dark red gradient background
        self._draw_game_over_gradient()

        # Draw falling particles effect
        self._draw_falling_particles()

    def _draw_game_over_gradient(self):
        """Draw a dark red gradient background for game over screen"""
        # Create gradient surface
        gradient = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Draw vertical gradient from dark red to black
        for y in range(SCREEN_HEIGHT):
            # Calculate color based on position
            intensity = 150 * (1 - y / SCREEN_HEIGHT)
            color = (int(intensity * 0.8), 0, 0)
            pygame.draw.line(gradient, color, (0, y), (SCREEN_WIDTH, y))

        self.screen.blit(gradient, (0, 0))

    def _draw_falling_particles(self):
        """Draw falling particles effect for game over screen"""
        # Draw falling particles
        for _ in range(30):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            color = (random.randint(100, 200), random.randint(50, 100), random.randint(50, 100))
            size = random.randint(2, 4)

            pygame.draw.circle(self.screen, color, (x, y), size)

    def _draw_victory_background(self):
        """Draw victory screen background with special effects"""
        # Create gradient background
        self._draw_victory_gradient()

        # Draw confetti particles
        self._draw_confetti_particles()

    def _draw_victory_gradient(self):
        """Draw a gradient background for victory screen"""
        # Create gradient surface
        gradient = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Draw vertical gradient from dark blue to black
        for y in range(SCREEN_HEIGHT):
            # Calculate color based on position
            intensity = 255 * (1 - y / SCREEN_HEIGHT)
            color = (0, 0, int(intensity * 0.3))
            pygame.draw.line(gradient, color, (0, y), (SCREEN_WIDTH, y))

        self.screen.blit(gradient, (0, 0))

    def _draw_confetti_particles(self):
        """Draw confetti-like particles for victory celebration"""
        # Draw colorful confetti particles
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(3, 8)
            color = (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255)
            )

            # Draw confetti pieces with different shapes
            if random.random() < 0.3:
                # Square confetti
                pygame.draw.rect(self.screen, color, (x, y, size, size))
            elif random.random() < 0.6:
                # Circle confetti
                pygame.draw.circle(self.screen, color, (x, y), size // 2)
            else:
                # Star confetti
                self._draw_star(self.screen, color, (x, y), size)

    def _draw_star(self, surface, color, center, size):
        """Draw a star shape for confetti"""
        points = []
        for i in range(5):
            angle = 2 * math.pi * i / 5 - math.pi / 2
            outer_radius = size
            inner_radius = size // 2
            outer_point = (
                center[0] + outer_radius * math.cos(angle),
                center[1] + outer_radius * math.sin(angle)
            )
            inner_point = (
                center[0] + inner_radius * math.cos(angle + math.pi / 5),
                center[1] + inner_radius * math.sin(angle + math.pi / 5)
            )
            points.extend([outer_point, inner_point])

        pygame.draw.polygon(surface, color, points)

    def _draw_victory_effects(self):
        """Draw additional victory visual effects"""
        # Draw pulsing glow around victory text
        self._draw_victory_glow(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        # Draw fireworks particles
        self._draw_fireworks()

    def _draw_victory_glow(self, center_x, center_y):
        """Draw pulsing glow effect around victory text"""
        # Initialize glow animation if not exists
        if not hasattr(self, 'victory_glow_scale'):
            self.victory_glow_scale = 1.0
            self.victory_glow_direction = 1

        # Update glow animation
        self.victory_glow_scale += 0.03 * self.victory_glow_direction
        if self.victory_glow_scale >= 1.3 or self.victory_glow_scale <= 0.7:
            self.victory_glow_direction *= -1

        # Draw glow effect
        glow_size = 200 * self.victory_glow_scale
        glow_surface = pygame.Surface((int(glow_size), int(glow_size)), pygame.SRCALPHA)

        # Create radial gradient for glow
        for i in range(int(glow_size // 2)):
            alpha = max(0, 255 * (1 - i / (glow_size // 2)))
            color = (100, 255, 100, alpha)
            pygame.draw.circle(glow_surface, color, (int(glow_size // 2), int(glow_size // 2)), int(glow_size // 2) - i, 1)

        # Blit glow centered
        glow_rect = glow_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(glow_surface, glow_rect)

    def _draw_fireworks(self):
        """Draw fireworks particles for victory celebration"""
        # Draw fireworks explosions
        for _ in range(3):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 200)

            # Draw firework explosion
            explosion_size = random.randint(30, 60)
            colors = [
                (255, 0, 0), (0, 255, 0), (0, 0, 255),
                (255, 255, 0), (255, 0, 255), (0, 255, 255)
            ]

            # Draw explosion particles
            for i in range(20):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0, explosion_size)
                particle_x = x + distance * math.cos(angle)
                particle_y = y + distance * math.sin(angle)
                color = random.choice(colors)
                size = random.randint(2, 5)

                pygame.draw.circle(self.screen, color, (int(particle_x), int(particle_y)), size)

    def handle_events(self, events):
        """Handle game events"""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == START and event.key == pygame.K_SPACE:
                    # Start game from start screen
                    self._start_game()
                elif self.game_state == VICTORY and event.key == pygame.K_r:
                    self._restart_game()
                elif self.game_state == GAME_OVER and event.key == pygame.K_r:
                    self._restart_game()
                elif event.key == pygame.K_ESCAPE and self.game_state == PLAYING:
                    # Toggle pause with ESC key (only during gameplay)
                    self.paused = not self.paused
                    if self.paused:
                        self.command_active = True  # Activate command input when paused
                        print("Game paused. Type commands and press ENTER.")
                    else:
                        self.command_active = False
                        self.command_input = ""  # Clear command input when unpausing
                        print("Game resumed.")
                elif event.key == pygame.K_RETURN and self.paused and self.command_active:
                    # Handle command submission when paused
                    self._handle_command_submission()
                elif self.paused and self.command_active and event.key != pygame.K_RETURN:
                    # Handle command input when paused
                    self._handle_command_input(event)

        # Handle player input (only when playing and not paused)
        if self.player and self.game_state == PLAYING and not self.paused:
            self.player.handle_input(events)

    def _start_game(self):
        """Start the game from the start screen"""
        self.game_state = PLAYING
        self.start_time = time.time()
        print("Game started!")

    def _restart_game(self):
        """Restart the game by resetting all game state"""
        # Reset game state
        self.score = 0
        self.victory = False
        self.game_over = False
        self.max_speed_reached = False
        self.game_state = PLAYING
        self.start_time = time.time()

        # Reinitialize game objects
        self._initialize_game_objects()


    def _handle_key_down(self, event):
        """Handle key down events"""
        if self.player:
            if event.key == pygame.K_LEFT:
                self.player.move_left = True
            elif event.key == pygame.K_RIGHT:
                self.player.move_right = True

    def _handle_key_up(self, event):
        """Handle key up events"""
        if self.player:
            if event.key == pygame.K_LEFT:
                self.player.move_left = False
            elif event.key == pygame.K_RIGHT:
                self.player.move_right = False

    def _handle_command_input(self, event):
        """Handle command input when paused"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Remove last character from command input
                self.command_input = self.command_input[:-1]
            elif event.key == pygame.K_ESCAPE:
                # Clear command input if ESC is pressed while typing
                self.command_input = ""
            elif event.unicode and event.unicode.isprintable():
                # Add printable character to command input
                self.command_input += event.unicode

    def _handle_command_submission(self):
        """Handle command submission when ENTER is pressed"""
        if not self.command_input:
            return

        command = self.command_input.strip().upper()
        print(f"Command received: {command}")

        if command == "SPEED":
            self._handle_speed_command()
        else:
            print(f"Unknown command: {command}")

        # Clear command input after submission
        self.command_input = ""

    def _handle_speed_command(self):
        """Handle the SPEED command"""
        if not self.speed_cheat_active:
            # First use: activate cheat mode
            if self.player and not self.speed_cheat_active:
                self.normal_player_speed = self.player.speed  # Store normal speed
                self.player.speed = 27  # Set to cheat speed
                self.speed_cheat_active = True
                print("SPEED command activated! Player speed set to 27.")
        else:
            # Second use: deactivate cheat mode
            if self.player and self.normal_player_speed is not None:
                self.player.speed = self.normal_player_speed  # Restore normal speed
                self.speed_cheat_active = False
                print("SPEED command deactivated! Player speed restored to normal.")

    def handle_volume_control(self, events):
        """Handle volume control and mute functionality"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Cheat code: CTRL+C to set target speed to 25
                    if self.target:
                        self.target.speed = 25.0
                        print("Cheat activated: Target speed set to 25!")