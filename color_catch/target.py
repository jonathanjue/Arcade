import pygame
import random
from constants import TARGET_WIDTH, TARGET_HEIGHT, TARGET_INITIAL_SPEED, RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK, SCREEN_WIDTH, SCREEN_HEIGHT, SPEED_INCREASE_PERCENTAGE, MAX_SPEED

class Target:
    def __init__(self, x=None, y=None, speed_multiplier=1.0):
        # Initialize with random position if not provided
        self.x = x if x is not None else random.randint(0, SCREEN_WIDTH - TARGET_WIDTH)
        self.y = y if y is not None else random.randint(0, SCREEN_HEIGHT - TARGET_HEIGHT)
        self.width = TARGET_WIDTH
        self.height = TARGET_HEIGHT
        
        # Base speed and multiplier for difficulty adjustment
        self.base_speed = TARGET_INITIAL_SPEED
        self.speed_multiplier = speed_multiplier
        self.speed = TARGET_INITIAL_SPEED * speed_multiplier

        # Random color for the target
        self.color = self._get_random_color()

        # Target rectangle for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Movement properties
        self.direction_x = random.choice([-1, 1])  # Random horizontal direction
        self.direction_y = random.choice([-1, 1])  # Random vertical direction
        self.direction_change_counter = 0
        self.direction_change_interval = random.randint(30, 90)  # Change direction every 30-90 frames

        # Store screen boundaries
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        # Slowdown multiplier (1.0 = normal speed, lower = slower)
        self._slowdown_multiplier = 1.0

    @property
    def slowdown_multiplier(self):
        """Get the current slowdown multiplier"""
        return self._slowdown_multiplier

    def set_slowdown(self, multiplier):
        """Set the slowdown multiplier for the target"""
        self._slowdown_multiplier = multiplier

    def _get_random_color(self):
        """Get a random color for the target"""
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
        return random.choice(colors)

    def update(self):
        """Update target position with random movement and animations"""
        # Store previous position for smooth movement
        prev_x, prev_y = self.x, self.y

        # Move target in current direction with slowdown multiplier applied
        self.x += self.speed * self.slowdown_multiplier * self.direction_x
        self.y += self.speed * self.slowdown_multiplier * self.direction_y

        # Update rectangle position
        self.rect.x = self.x
        self.rect.y = self.y

        # Change direction randomly at intervals
        self.direction_change_counter += 1
        if self.direction_change_counter >= self.direction_change_interval:
            self.direction_change_counter = 0
            self.direction_change_interval = random.randint(30, 90)  # New random interval

            # Randomly change direction (50% chance for each axis)
            if random.random() < 0.5:
                self.direction_x *= -1
            if random.random() < 0.5:
                self.direction_y *= -1

        # Keep target within screen boundaries
        if self.x <= 0:
            self.x = 0
            self.direction_x = 1  # Bounce off left edge
        elif self.x >= self.screen_width - self.width:
            self.x = self.screen_width - self.width
            self.direction_x = -1  # Bounce off right edge

        if self.y <= 0:
            self.y = 0
            self.direction_y = 1  # Bounce off top edge
        elif self.y >= self.screen_height - self.height:
            self.y = self.screen_height - self.height
            self.direction_y = -1  # Bounce off bottom edge

        # Update animation state
        self._update_animation_state(prev_x, prev_y)

    def _update_animation_state(self, prev_x, prev_y):
        """Update target animation state based on movement and speed"""
        # Calculate movement delta
        delta_x = self.x - prev_x
        delta_y = self.y - prev_y

        # Initialize animation properties if they don't exist
        if not hasattr(self, 'pulse_scale'):
            self.pulse_scale = 1.0
            self.pulse_direction = 1
            self.pulse_counter = 0

        # Apply pulsing animation for high speed targets
        if self.speed > 10:  # High speed pulsing
            self._apply_pulse_animation()
        elif self.speed > 5:  # Medium speed subtle pulse
            self._apply_subtle_pulse()
        else:  # Normal speed - reset to default
            self.pulse_scale = 1.0

    def _apply_pulse_animation(self):
        """Apply pulsing animation for high speed targets"""
        # Pulse animation parameters
        pulse_speed = 0.1
        pulse_amount = 0.3

        # Update pulse scale
        self.pulse_scale += pulse_speed * self.pulse_direction

        # Reverse direction at bounds
        if self.pulse_scale >= 1.0 + pulse_amount:
            self.pulse_direction = -1
        elif self.pulse_scale <= 1.0 - pulse_amount:
            self.pulse_direction = 1

    def _apply_subtle_pulse(self):
        """Apply subtle pulsing for medium speed targets"""
        # Subtle pulse animation
        pulse_speed = 0.05
        pulse_amount = 0.15

        # Update pulse scale
        self.pulse_scale += pulse_speed * self.pulse_direction

        # Reverse direction at bounds
        if self.pulse_scale >= 1.0 + pulse_amount:
            self.pulse_direction = -1
        elif self.pulse_scale <= 1.0 - pulse_amount:
            self.pulse_direction = 1

    def draw(self, surface):
        """Draw the target on the given surface with animations"""
        # Get the base rectangle
        base_rect = self.rect.copy()

        # Apply pulsing animation if active
        if hasattr(self, 'pulse_scale') and self.pulse_scale != 1.0:
            # Calculate scaled dimensions
            scaled_width = int(self.width * self.pulse_scale)
            scaled_height = int(self.height * self.pulse_scale)

            # Calculate center position
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2

            # Create scaled rectangle centered at the same position
            scaled_rect = pygame.Rect(
                center_x - scaled_width // 2,
                center_y - scaled_height // 2,
                scaled_width,
                scaled_height
            )

            # Draw the pulsed target
            pygame.draw.rect(surface, self.color, scaled_rect)
        else:
            # Draw normal target
            pygame.draw.rect(surface, self.color, base_rect)

        # Always keep the collision rect at the base size for consistent collision detection
        self.rect.width = self.width
        self.rect.height = self.height

    def respawn(self):
        """Respawn the target at a new random position with new color and increased speed"""
        # Move to new random position
        self.x = random.randint(0, self.screen_width - self.width)
        self.y = random.randint(0, self.screen_height - self.height)

        # Update rectangle position
        self.rect.x = self.x
        self.rect.y = self.y

        # Change to new random color
        self.color = self._get_random_color()

        # Apply speed increase with percentage-based difficulty progression
        self._increase_speed()

        # Reset movement direction
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.direction_change_counter = 0
        self.direction_change_interval = random.randint(30, 90)

    def _increase_speed(self):
        """Increase target speed with percentage-based progression and maximum cap"""
        # Calculate new base speed with percentage increase
        new_base_speed = self.base_speed * (1 + SPEED_INCREASE_PERCENTAGE)
        
        # Apply maximum speed cap to base speed
        self.base_speed = min(new_base_speed, MAX_SPEED)
        
        # Apply multiplier to actual speed
        self.speed = self.base_speed * self.speed_multiplier
        self.speed = min(self.speed, MAX_SPEED)

        # Ensure speed doesn't get too high to cause physics issues
        if self.speed > MAX_SPEED:
            self.speed = MAX_SPEED

        # Change color based on speed for visual feedback
        self._update_color_based_on_speed()
    
    def set_speed_multiplier(self, multiplier):
        """Set the speed multiplier for difficulty adjustment"""
        self.speed_multiplier = multiplier
        self.speed = self.base_speed * multiplier
        self.speed = min(self.speed, MAX_SPEED)

    def _update_color_based_on_speed(self):
        """Update target color based on current speed for visual feedback"""
        if self.speed < 5:
            # Slow speed - use basic colors
            colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
        elif self.speed < 10:
            # Medium speed - add orange
            colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]
        else:
            # High speed - add pink for visual intensity
            colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK]

        self.color = random.choice(colors)

    def get_speed(self):
        """Get current target speed"""
        return self.speed

    def get_position(self):
        """Get target's current position"""
        return (self.x, self.y)

    def get_rect(self):
        """Get target's collision rectangle"""
        return self.rect

    def is_off_screen(self, screen_height):
        """Check if target is off screen"""
        return self.y > screen_height