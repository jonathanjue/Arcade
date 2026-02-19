import pygame
import time
from constants import PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
from constants import DASH_SPEED, DASH_COOLDOWN, DASH_DURATION, DASH_DISTANCE

class Player:
    def __init__(self, x, y, abilities_enabled=True):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        
        # Abilities enabled flag (for difficulty adjustment)
        self.abilities_enabled = abilities_enabled

        # Movement flags for all directions
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

        # Screen boundaries
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        # Player rectangle for collision detection
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Dash properties
        self.is_dashing = False
        self.dash_cooldown = 0  # Time remaining until dash is available
        self.dash_direction = (0, -1)  # Default dash direction (up)
        self.dash_start_time = 0
        self.dash_start_x = 0
        self.dash_start_y = 0
        self.dash_target_x = 0
        self.dash_target_y = 0
        self.last_dash_time = -DASH_COOLDOWN  # Allow immediate first dash

    def update(self):
        """Update player position based on movement flags with smooth animation"""
        # Update dash cooldown
        self._update_dash_cooldown()
        
        # Handle dashing movement
        if self.is_dashing:
            self._update_dash()
            return
        
        # Store previous position for smooth movement
        prev_x, prev_y = self.x, self.y

        # Apply movement with easing for smoother animation
        if self.move_left:
            self.x -= self.speed
        if self.move_right:
            self.x += self.speed
        if self.move_up:
            self.y -= self.speed
        if self.move_down:
            self.y += self.speed

        # Keep player within screen bounds
        self._constrain_to_screen()

        # Update rectangle position
        self.rect.x = self.x
        self.rect.y = self.y

        # Add smooth transition effect
        self._apply_smooth_transition(prev_x, prev_y)
        
        # Update dash direction based on current movement
        self._update_dash_direction()

    def _apply_smooth_transition(self, prev_x, prev_y):
        """Apply smooth transition effect for player movement"""
        # Calculate movement delta for potential animation effects
        delta_x = self.x - prev_x
        delta_y = self.y - prev_y

        # Add subtle visual feedback for movement
        if abs(delta_x) > 0 or abs(delta_y) > 0:
            # Could add trail effects or other visual feedback here
            pass

    def _update_dash_direction(self):
        """Update dash direction based on current movement input"""
        # Calculate direction based on movement flags
        dx = 0
        dy = 0
        
        if self.move_left:
            dx -= 1
        if self.move_right:
            dx += 1
        if self.move_up:
            dy -= 1
        if self.move_down:
            dy += 1
        
        # If moving, update dash direction
        if dx != 0 or dy != 0:
            # Normalize the direction vector
            length = (dx * dx + dy * dy) ** 0.5
            self.dash_direction = (dx / length, dy / length)
        else:
            # Default to up when not moving
            self.dash_direction = (0, -1)

    def _update_dash_cooldown(self):
        """Update dash cooldown timer"""
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1 / 60  # Assuming 60 FPS

    def can_dash(self):
        """Check if player can dash (cooldown expired and abilities enabled)"""
        if not self.abilities_enabled:
            return False
        current_time = time.time()
        return current_time - self.last_dash_time >= DASH_COOLDOWN

    def start_dash(self):
        """Initiate a dash in the current direction"""
        if not self.can_dash():
            return False
        
        self.is_dashing = True
        self.dash_start_time = time.time()
        self.dash_start_x = self.x
        self.dash_start_y = self.y
        self.last_dash_time = self.dash_start_time
        
        # Calculate target position based on dash direction and distance
        self.dash_target_x = self.x + self.dash_direction[0] * DASH_DISTANCE
        self.dash_target_y = self.y + self.dash_direction[1] * DASH_DISTANCE
        
        return True

    def _update_dash(self):
        """Update player position during dash"""
        elapsed = time.time() - self.dash_start_time
        
        if elapsed >= DASH_DURATION:
            # Dash complete - snap to target
            self.x = self.dash_target_x
            self.y = self.dash_target_y
            self.is_dashing = False
        else:
            # Interpolate position for smooth dash movement
            progress = elapsed / DASH_DURATION
            # Use ease-out for smoother deceleration
            ease_progress = 1 - (1 - progress) ** 2
            
            self.x = self.dash_start_x + (self.dash_target_x - self.dash_start_x) * ease_progress
            self.y = self.dash_start_y + (self.dash_target_y - self.dash_start_y) * ease_progress
        
        # Keep player within screen bounds
        self._constrain_to_screen()
        
        # Update rectangle position
        self.rect.x = self.x
        self.rect.y = self.y

    def _constrain_to_screen(self):
        """Keep player within screen boundaries"""
        # Prevent player from going off left edge
        if self.x < 0:
            self.x = 0

        # Prevent player from going off right edge
        if self.x + self.width > self.screen_width:
            self.x = self.screen_width - self.width

        # Prevent player from going off top edge
        if self.y < 0:
            self.y = 0

        # Prevent player from going off bottom edge
        if self.y + self.height > self.screen_height:
            self.y = self.screen_height - self.height

    def draw(self, screen):
        """Draw the player on screen"""
        pygame.draw.rect(screen, WHITE, self.rect)

    def handle_input(self, events):
        """Handle input events for player movement"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_left = True
                elif event.key == pygame.K_RIGHT:
                    self.move_right = True
                elif event.key == pygame.K_UP:
                    self.move_up = True
                elif event.key == pygame.K_DOWN:
                    self.move_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move_left = False
                elif event.key == pygame.K_RIGHT:
                    self.move_right = False
                elif event.key == pygame.K_UP:
                    self.move_up = False
                elif event.key == pygame.K_DOWN:
                    self.move_down = False