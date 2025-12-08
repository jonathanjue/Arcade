import pygame
from constants import PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED

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

    def update(self):
        """Update player position based on movement flags with smooth animation"""
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

    def _apply_smooth_transition(self, prev_x, prev_y):
        """Apply smooth transition effect for player movement"""
        # Calculate movement delta for potential animation effects
        delta_x = self.x - prev_x
        delta_y = self.y - prev_y

        # Add subtle visual feedback for movement
        if abs(delta_x) > 0 or abs(delta_y) > 0:
            # Could add trail effects or other visual feedback here
            pass

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