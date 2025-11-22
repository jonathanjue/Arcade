"""
Doom game placeholder for the Arcade Collection.
Displays a "coming soon" message with retro styling and returns to menu on ESC.
"""

import pygame
import math
from game_states import BaseGameState
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, Colors, Fonts,
    NEON_COLORS
)


class DoomGame(BaseGameState):
    """
    Placeholder game handler for Doom.
    Shows a coming soon message with retro arcade styling.
    """
    
    def __init__(self):
        """Initialize the Doom game placeholder."""
        super().__init__()
        self.animation_time = 0.0
        self.particles = []
        
        # Load fonts
        self._load_fonts()
        
        # Initialize particles for visual effect
        self._initialize_particles()
        
        print("DoomGame initialized")
    
    def _load_fonts(self):
        """Load fonts for the game."""
        try:
            self.title_font = pygame.font.Font(None, Fonts.GAME_TITLE_SIZE)
            self.message_font = pygame.font.Font(None, Fonts.MENU_SIZE)
            self.instruction_font = pygame.font.Font(None, Fonts.INSTRUCTION_SIZE)
        except:
            self.title_font = pygame.font.Font(None, Fonts.GAME_TITLE_SIZE)
            self.message_font = pygame.font.Font(None, Fonts.MENU_SIZE)
            self.instruction_font = pygame.font.Font(None, Fonts.INSTRUCTION_SIZE)
    
    def _initialize_particles(self):
        """Initialize floating particles for visual effect."""
        import random
        for _ in range(20):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'vx': random.uniform(-20, 20),
                'vy': random.uniform(-20, 20),
                'color': NEON_COLORS[random.randint(0, len(NEON_COLORS) - 1)],
                'size': random.randint(2, 6)
            })
    
    def handle_event(self, event):
        """
        Handle game events.
        
        Args:
            event: Pygame event to handle
            
        Returns:
            bool: True if event was handled
        """
        # All events are handled by the state manager (ESC for return to menu)
        return False
    
    def update(self, dt):
        """
        Update the game state and animations.
        
        Args:
            dt: Delta time (time since last frame)
        """
        super().update(dt)
        self.animation_time += dt
        
        # Update particles
        for particle in self.particles:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            
            # Wrap around screen edges
            if particle['x'] < 0:
                particle['x'] = SCREEN_WIDTH
            elif particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
            
            if particle['y'] < 0:
                particle['y'] = SCREEN_HEIGHT
            elif particle['y'] > SCREEN_HEIGHT:
                particle['y'] = 0
    
    def render(self, screen):
        """
        Render the Doom game placeholder.
        
        Args:
            screen: Pygame surface to render to
        """
        # Clear screen with dark background
        screen.fill(Colors.DARK_RED)
        
        # Render particles
        self._render_particles(screen)
        
        # Render title
        self._render_title(screen)
        
        # Render coming soon message
        self._render_message(screen)
        
        # Render instructions
        self._render_instructions(screen)
        
        # Render decorative elements
        self._render_decorations(screen)
    
    def _render_particles(self, screen):
        """Render floating particles."""
        for particle in self.particles:
            color = particle['color']
            alpha = int(100 + 100 * math.sin(self.animation_time + particle['x'] * 0.01))
            color_with_alpha = (
                min(255, color[0]),
                min(255, color[1]),
                min(255, color[2])
            )
            
            pygame.draw.circle(screen, color_with_alpha, 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
    
    def _render_title(self, screen):
        """Render the game title with intense styling."""
        title_text = "DOOM"
        title_color = Colors.RED
        
        # Render multiple glow layers
        for offset in range(1, 6):
            glow_alpha = int(255 - (offset * 40))
            glow_surface = self.title_font.render(title_text, True, title_color)
            glow_rect = glow_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
            
            # Offset glow in all directions
            for dx in range(-offset, offset + 1):
                for dy in range(-offset, offset + 1):
                    if dx != 0 or dy != 0:
                        glow_rect.offset(dx * 2, dy * 2)
                        screen.blit(glow_surface, glow_rect)
                        glow_rect.offset(-dx * 2, -dy * 2)  # Reset position
        
        # Render main title
        title_surface = self.title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surface, title_rect)
    
    def _render_message(self, screen):
        """Render the coming soon message."""
        message = "GAME COMING SOON!"
        message_color = Colors.YELLOW
        
        # Pulsing effect
        pulse_scale = 1.0 + 0.1 * math.sin(self.animation_time * 3)
        message_surface = self.message_font.render(message, True, message_color)
        
        # Scale the surface
        scaled_width = int(message_surface.get_width() * pulse_scale)
        scaled_height = int(message_surface.get_height() * pulse_scale)
        scaled_surface = pygame.transform.scale(message_surface, (scaled_width, scaled_height))
        
        message_rect = scaled_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(scaled_surface, message_rect)
        
        # Additional message
        sub_message = "Prepare for demonic battles!"
        sub_surface = self.instruction_font.render(sub_message, True, Colors.WHITE)
        sub_rect = sub_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(sub_surface, sub_rect)
    
    def _render_instructions(self, screen):
        """Render control instructions."""
        instruction_text = "Press ESC to return to menu"
        instruction_color = Colors.CYAN
        
        instruction_surface = self.instruction_font.render(instruction_text, True, instruction_color)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        
        # Add blinking effect
        blink_alpha = int(150 + 105 * math.sin(self.animation_time * 4))
        if blink_alpha > 200:  # Only show when bright
            screen.blit(instruction_surface, instruction_rect)
    
    def _render_decorations(self, screen):
        """Render decorative elements."""
        # Render some geometric shapes
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Rotating squares
        for i in range(4):
            angle = self.animation_time + i * math.pi / 2
            size = 20 + 10 * math.sin(angle)
            
            x = center_x + 100 * math.cos(angle)
            y = center_y + 100 * math.sin(angle)
            
            color = NEON_COLORS[i % len(NEON_COLORS)]
            rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
            
            pygame.draw.rect(screen, color, rect, 2)
        
        # Corner decorations
        corner_size = 40
        for corner_x, corner_y in [(50, 50), (SCREEN_WIDTH - 90, 50), 
                                   (50, SCREEN_HEIGHT - 90), 
                                   (SCREEN_WIDTH - 90, SCREEN_HEIGHT - 90)]:
            pygame.draw.rect(screen, Colors.RED, 
                           (corner_x, corner_y, corner_size, corner_size), 3)