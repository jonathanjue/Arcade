"""
Contra game placeholder for the Arcade Collection.
Displays a "coming soon" message with jungle/military styling and returns to menu on ESC.
"""

import pygame
import math
import random
from game_states import BaseGameState
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, Colors, Fonts,
    NEON_COLORS
)


class ContraGame(BaseGameState):
    """
    Placeholder game handler for Contra.
    Shows a coming soon message with military/jungle styling.
    """
    
    def __init__(self):
        """Initialize the Contra game placeholder."""
        super().__init__()
        self.animation_time = 0.0
        self.soldiers = []
        self.bullets = []
        
        # Load fonts
        self._load_fonts()
        
        # Initialize soldiers for visual effect
        self._initialize_soldiers()
        
        print("ContraGame initialized")
    
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
    
    def _initialize_soldiers(self):
        """Initialize soldier sprites for visual effect."""
        for _ in range(6):
            self.soldiers.append({
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(100, SCREEN_HEIGHT - 100),
                'vx': random.choice([-50, 50]),
                'color': Colors.GREEN if random.random() > 0.5 else Colors.DARK_GREEN
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
        
        # Update soldiers
        for soldier in self.soldiers:
            soldier['x'] += soldier['vx'] * dt
            
            # Bounce off screen edges
            if soldier['x'] < 20 or soldier['x'] > SCREEN_WIDTH - 20:
                soldier['vx'] *= -1
        
        # Generate occasional bullet effects
        if random.random() < 0.05:  # 5% chance per frame
            self._generate_bullet_effect()
    
    def _generate_bullet_effect(self):
        """Generate a bullet effect."""
        start_x = random.randint(0, SCREEN_WIDTH)
        start_y = random.randint(0, SCREEN_HEIGHT)
        end_x = random.randint(0, SCREEN_WIDTH)
        end_y = random.randint(0, SCREEN_HEIGHT)
        
        self.bullets.append({
            'start_x': start_x,
            'start_y': start_y,
            'end_x': end_x,
            'end_y': end_y,
            'progress': 0.0,
            'duration': 0.5
        })
    
    def render(self, screen):
        """
        Render the Contra game placeholder.
        
        Args:
            screen: Pygame surface to render to
        """
        # Clear screen with jungle/military background
        screen.fill(Colors.DARK_GREEN)
        
        # Render background elements
        self._render_background(screen)
        
        # Render title
        self._render_title(screen)
        
        # Render soldiers
        self._render_soldiers(screen)
        
        # Render bullets
        self._render_bullets(screen)
        
        # Render coming soon message
        self._render_message(screen)
        
        # Render instructions
        self._render_instructions(screen)
    
    def _render_background(self, screen):
        """Render jungle/military background."""
        # Draw horizontal lines to simulate jungle vegetation
        for y in range(0, SCREEN_HEIGHT, 30):
            alpha = int(50 + 50 * math.sin(self.animation_time + y * 0.01))
            line_color = (0, max(0, 50 + alpha), 0)
            pygame.draw.line(screen, line_color, (0, y), (SCREEN_WIDTH, y), 2)
        
        # Draw some military-style grid
        grid_spacing = 60
        for x in range(0, SCREEN_WIDTH, grid_spacing):
            pygame.draw.line(screen, (20, 60, 20), (x, 0), (x, SCREEN_HEIGHT), 1)
        
        for y in range(0, SCREEN_HEIGHT, grid_spacing):
            pygame.draw.line(screen, (20, 60, 20), (0, y), (SCREEN_WIDTH, y), 1)
    
    def _render_soldiers(self, screen):
        """Render soldier sprites."""
        for soldier in self.soldiers:
            x, y = int(soldier['x']), int(soldier['y'])
            
            # Soldier body (simple rectangle)
            soldier_rect = pygame.Rect(x - 8, y - 12, 16, 24)
            pygame.draw.rect(screen, soldier['color'], soldier_rect)
            
            # Soldier helmet
            helmet_rect = pygame.Rect(x - 6, y - 16, 12, 6)
            pygame.draw.rect(screen, Colors.DARK_GREEN, helmet_rect)
            
            # Soldier gun
            gun_x = x + (8 if soldier['vx'] > 0 else -8)
            gun_rect = pygame.Rect(gun_x, y - 4, 12, 2)
            pygame.draw.rect(screen, Colors.BLACK, gun_rect)
    
    def _render_bullets(self, screen):
        """Render bullet effects."""
        bullets_to_remove = []
        
        for i, bullet in enumerate(self.bullets):
            bullet['progress'] += 1.0 / (bullet['duration'] * 60)  # Assuming 60 FPS
            
            if bullet['progress'] >= 1.0:
                bullets_to_remove.append(i)
                continue
            
            # Calculate current bullet position
            current_x = bullet['start_x'] + (bullet['end_x'] - bullet['start_x']) * bullet['progress']
            current_y = bullet['start_y'] + (bullet['end_y'] - bullet['start_y']) * bullet['progress']
            
            # Draw bullet trail
            trail_length = 20
            trail_x = current_x - (current_x - bullet['start_x']) * 0.1
            trail_y = current_y - (current_y - bullet['start_y']) * 0.1
            
            # Draw trail
            pygame.draw.line(screen, Colors.YELLOW, 
                           (trail_x, trail_y), (current_x, current_y), 3)
            
            # Draw bullet head
            pygame.draw.circle(screen, Colors.RED, (int(current_x), int(current_y)), 4)
        
        # Remove completed bullets
        for i in reversed(bullets_to_remove):
            self.bullets.pop(i)
    
    def _render_title(self, screen):
        """Render the game title with military styling."""
        title_text = "CONTRA"
        title_color = Colors.GREEN
        
        # Render military-style title with border
        for offset in range(1, 4):
            border_surface = self.title_font.render(title_text, True, Colors.BLACK)
            border_rect = border_surface.get_rect(center=(SCREEN_WIDTH // 2 + offset, 120 + offset))
            screen.blit(border_surface, border_rect)
        
        # Render main title
        title_surface = self.title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(title_surface, title_rect)
        
        # Render subtitle
        subtitle_text = "MISSION READY"
        subtitle_surface = self.instruction_font.render(subtitle_text, True, Colors.YELLOW)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 160))
        screen.blit(subtitle_surface, subtitle_rect)
    
    def _render_message(self, screen):
        """Render the coming soon message."""
        message = "GAME COMING SOON!"
        message_color = Colors.YELLOW
        
        # Military-style border
        message_surface = self.message_font.render(message, True, Colors.BLACK)
        border_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        
        # Draw border effect
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx != 0 or dy != 0:
                    border_rect.move_ip(dx, dy)
                    screen.blit(message_surface, border_rect)
                    border_rect.move_ip(-dx, -dy)
        
        # Render main message
        main_surface = self.message_font.render(message, True, message_color)
        main_rect = main_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(main_surface, main_rect)
        
        # Additional message
        sub_message = "Prepare for action!"
        sub_surface = self.instruction_font.render(sub_message, True, Colors.WHITE)
        sub_rect = sub_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(sub_surface, sub_rect)
    
    def _render_instructions(self, screen):
        """Render control instructions."""
        instruction_text = "Press ESC to return to menu"
        instruction_color = Colors.CYAN
        
        instruction_surface = self.instruction_font.render(instruction_text, True, instruction_color)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        
        # Add military-style border
        border_surface = self.instruction_font.render(instruction_text, True, Colors.BLACK)
        border_rect = border_surface.get_rect(center=(SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT - 79))
        screen.blit(border_surface, border_rect)
        
        screen.blit(instruction_surface, instruction_rect)
    
    def render_menu_option(self, screen, x, y, selected=False):
        """Render menu option for the main menu."""
        text = "Contra"
        color = Colors.GREEN if not selected else Colors.YELLOW
        
        # Military-style rendering
        text_surface = pygame.font.Font(None, Fonts.MENU_SIZE).render(text, True, color)
        screen.blit(text_surface, (x, y))