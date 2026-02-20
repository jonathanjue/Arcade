"""
Gravity Flip Arena - A 2D arena survival game
PHASE 2: Player + Gravity System

Controls:
- Arrow Keys: Move left/right
- SPACE or Left Click: Flip gravity
- ESC: Quit game
"""

import pygame
import sys

# =============================================================================
# CONSTANTS
# =============================================================================

# Screen Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player Settings
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_SPEED = 300  # pixels per second
PLAYER_ENERGY_MAX = 100
PLAYER_ENERGY_REGEN = 15  # per second
GRAVITY_FLIP_COST = 25

# Physics Settings
GRAVITY_FORCE = 800  # pixels per second squared
TERMINAL_VELOCITY = 500

# Enemy Settings (for future phases)
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 30
ENEMY_BASE_SPEED = 150
ENEMY_STUN_DURATION = 0.5  # seconds

# Spawn Settings (for future phases)
BASE_SPAWN_INTERVAL = 3.0  # seconds
MIN_SPAWN_INTERVAL = 0.5
SPAWN_DECREASE_RATE = 0.1  # decrease per spawn

# Spike Settings
SPIKE_HEIGHT = 20
SPIKE_COUNT = 20  # per row

# Screen Shake Settings (for future phases)
SHAKE_INTENSITY = 10
SHAKE_DECAY = 0.9


# =============================================================================
# PLAYER CLASS
# =============================================================================

class Player:
    """
    Player character with movement, gravity physics, and rendering.
    
    Attributes:
        rect: pygame.Rect for position and dimensions
        velocity_y: float for vertical velocity
        speed: horizontal movement speed in pixels/second
        color: RGB color tuple (NEON_CYAN)
        is_alive: bool for alive state
    """
    
    def __init__(self, x, y, width, height):
        """
        Initialize player at position.
        
        Args:
            x: Initial x position
            y: Initial y position
            width: Player width
            height: Player height
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity_y = 0.0
        self.speed = PLAYER_SPEED
        self.color = NEON_CYAN
        self.is_alive = True
    
    def update(self, dt, keys, gravity):
        """
        Update player position, handle input, and apply physics.
        
        Args:
            dt: Delta time in seconds
            keys: pygame key state from pygame.key.get_pressed()
            gravity: Current gravity direction (1 or -1)
        """
        if not self.is_alive:
            return
        
        # Handle horizontal movement
        self.handle_input(dt, keys)
        
        # Apply gravity physics
        self.apply_gravity(dt, gravity)
        
        # Check floor/ceiling collision
        self.check_floor_ceiling_collision()
    
    def handle_input(self, dt, keys):
        """
        Process left/right movement input.
        
        Args:
            dt: Delta time in seconds
            keys: pygame key state from pygame.key.get_pressed()
        """
        # Move left
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * dt
        
        # Move right
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * dt
        
        # Keep player within horizontal screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    
    def apply_gravity(self, dt, gravity):
        """
        Apply gravity force to vertical velocity.
        
        Args:
            dt: Delta time in seconds
            gravity: Current gravity direction (1 or -1)
        """
        # Apply gravity acceleration
        self.velocity_y += GRAVITY_FORCE * gravity * dt
        
        # Cap at terminal velocity
        self.velocity_y = max(-TERMINAL_VELOCITY, min(TERMINAL_VELOCITY, self.velocity_y))
        
        # Update vertical position
        self.rect.y += self.velocity_y * dt
    
    def draw(self, surface):
        """
        Render player rectangle.
        
        Args:
            surface: pygame surface to draw on
        """
        pygame.draw.rect(surface, self.color, self.rect)
    
    def check_floor_ceiling_collision(self):
        """
        Keep player within screen bounds, accounting for spike height zones.
        Stops vertical velocity when hitting floor or ceiling.
        """
        # Floor collision (account for spike zone)
        if self.rect.bottom >= SCREEN_HEIGHT - SPIKE_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - SPIKE_HEIGHT
            self.velocity_y = 0
        
        # Ceiling collision (account for spike zone)
        if self.rect.top <= SPIKE_HEIGHT:
            self.rect.top = SPIKE_HEIGHT
            self.velocity_y = 0


# =============================================================================
# GAME CLASS
# =============================================================================

class Game:
    """
    Main game controller managing state, entities, rendering, and game loop.
    
    Attributes:
        screen: Main display surface
        clock: Game clock for FPS control
        running: Main loop running flag
        state: Current game state ("menu", "playing", "game_over")
        player: Player instance
        gravity: Current gravity direction (1 = down, -1 = up)
    """
    
    def __init__(self):
        """Initialize Pygame and game state."""
        # Initialize Pygame
        pygame.init()
        
        # Create display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Gravity Flip Arena")
        
        # Set up clock for FPS control
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.state = "menu"
        
        # Initialize font for text rendering
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        
        # Gravity system
        self.gravity = 1  # 1 = down, -1 = up
        
        # Create player in center of screen
        player_x = (SCREEN_WIDTH - PLAYER_WIDTH) // 2
        player_y = (SCREEN_HEIGHT - PLAYER_HEIGHT) // 2
        self.player = Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    def run(self):
        """
        Main game loop entry point.
        Handles the game loop with delta time for smooth movement.
        """
        while self.running:
            # Calculate delta time (convert milliseconds to seconds)
            dt = self.clock.tick(FPS) / 1000.0
            
            # Handle events
            self.handle_events()
            
            # State-specific logic
            if self.state == "menu":
                self.render_menu()
            elif self.state == "playing":
                self.update(dt)
                self.render()
            elif self.state == "game_over":
                self.render_game_over()
            
            # Update display
            pygame.display.flip()
        
        # Clean up
        pygame.quit()
    
    def handle_events(self):
        """Process pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                # Global quit with ESC
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # State-specific input handling
                if self.state == "menu":
                    if event.key == pygame.K_SPACE:
                        self.state = "playing"
                
                elif self.state == "playing":
                    if event.key == pygame.K_SPACE:
                        self.flip_gravity()
                
                elif self.state == "game_over":
                    if event.key == pygame.K_r:
                        self.restart()
                        self.state = "playing"
            
            # Mouse button handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left click flips gravity in playing state
                if event.button == 1:  # Left mouse button
                    if self.state == "playing":
                        self.flip_gravity()
    
    def update(self, dt):
        """
        Update all game logic.
        
        Args:
            dt: Delta time in seconds
        """
        # Get current key state
        keys = pygame.key.get_pressed()
        
        # Update player
        self.player.update(dt, keys, self.gravity)
    
    def render(self):
        """Render all game elements."""
        # Clear screen with black background
        self.screen.fill(BLACK)
        
        # Draw spike zones
        self.draw_spikes()
        
        # Draw player
        self.player.draw(self.screen)
    
    def draw_spikes(self):
        """Render floor and ceiling spikes as triangles."""
        spike_width = SCREEN_WIDTH // SPIKE_COUNT
        
        # Draw floor spikes
        for i in range(SPIKE_COUNT):
            x = i * spike_width
            # Triangle pointing down (into the play area)
            points = [
                (x, SCREEN_HEIGHT - SPIKE_HEIGHT),  # Top left
                (x + spike_width, SCREEN_HEIGHT - SPIKE_HEIGHT),  # Top right
                (x + spike_width // 2, SCREEN_HEIGHT)  # Bottom center (tip)
            ]
            pygame.draw.polygon(self.screen, RED, points)
        
        # Draw ceiling spikes
        for i in range(SPIKE_COUNT):
            x = i * spike_width
            # Triangle pointing up (into the play area)
            points = [
                (x, SPIKE_HEIGHT),  # Bottom left
                (x + spike_width, SPIKE_HEIGHT),  # Bottom right
                (x + spike_width // 2, 0)  # Top center (tip)
            ]
            pygame.draw.polygon(self.screen, RED, points)
    
    def render_menu(self):
        """Render the main menu screen."""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw title
        title_text = self.title_font.render("GRAVITY FLIP ARENA", True, NEON_CYAN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)
        
        # Draw instructions
        instruction_text = self.font.render("Press SPACE to Start", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(instruction_text, instruction_rect)
        
        # Draw controls info
        controls_text = self.font.render("SPACE/Left Click: Flip Gravity | Arrow Keys: Move", True, WHITE)
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        self.screen.blit(controls_text, controls_rect)
        
        # Draw quit instruction
        quit_text = self.font.render("ESC: Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
        self.screen.blit(quit_text, quit_rect)
    
    def render_game_over(self):
        """Render the game over screen."""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw game over text
        game_over_text = self.title_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Draw restart instruction
        restart_text = self.font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, restart_rect)
        
        # Draw quit instruction
        quit_text = self.font.render("ESC: Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        self.screen.blit(quit_text, quit_rect)
    
    def restart(self):
        """Reset game to initial state."""
        # Reset gravity
        self.gravity = 1
        
        # Reset player to center of screen
        player_x = (SCREEN_WIDTH - PLAYER_WIDTH) // 2
        player_y = (SCREEN_HEIGHT - PLAYER_HEIGHT) // 2
        self.player = Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    def flip_gravity(self):
        """Reverse gravity direction."""
        self.gravity *= -1


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main entry point for the game."""
    game = Game()
    game.run()
    sys.exit()


if __name__ == "__main__":
    main()
