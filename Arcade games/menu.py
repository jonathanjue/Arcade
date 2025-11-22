"""
Main menu system for the Arcade Collection.
Provides a retro arcade-style menu with navigation and visual feedback.
"""

import pygame
import math
from game_states import BaseGameState
from constants import (
    GameState, SCREEN_WIDTH, SCREEN_HEIGHT, Colors, Fonts,
    MENU_CENTER_X, MENU_START_Y, MENU_ITEM_SPACING,
    MENU_SELECTED_COLOR, MENU_NORMAL_COLOR, MENU_QUIT_COLOR, MENU_TITLE_COLOR,
    MENU_ANIMATION_SPEED, MENU_BORDER_THICKNESS, NEON_COLORS, MENU_BG_COLOR
)


class MainMenu(BaseGameState):
    """
    Main menu system with retro arcade aesthetics.
    Handles menu navigation, selection, and visual effects.
    """
    
    def __init__(self):
        """Initialize the main menu."""
        super().__init__()
        self.menu_options = [
            {"text": "Doom", "color": MENU_NORMAL_COLOR},
            {"text": "Contra", "color": MENU_NORMAL_COLOR},
            {"text": "Tetris", "color": MENU_NORMAL_COLOR},
            {"text": "Quit", "color": MENU_QUIT_COLOR}
        ]
        self.selected_index = 0
        self.animation_time = 0.0
        self.glow_effects = []
        
        # Load fonts
        self._load_fonts()
        
        # Initialize glow effects for menu items
        self._initialize_glow_effects()
        
        print("MainMenu initialized")
    
    def _load_fonts(self):
        """Load fonts with fallback to system fonts."""
        try:
            # Try to load retro-style fonts, fallback to default
            self.title_font = pygame.font.Font(None, Fonts.TITLE_SIZE)
            self.menu_font = pygame.font.Font(None, Fonts.MENU_SIZE)
            self.instruction_font = pygame.font.Font(None, Fonts.INSTRUCTION_SIZE)
        except:
            # Fallback to default font
            self.title_font = pygame.font.Font(None, Fonts.TITLE_SIZE)
            self.menu_font = pygame.font.Font(None, Fonts.MENU_SIZE)
            self.instruction_font = pygame.font.Font(None, Fonts.INSTRUCTION_SIZE)
        
        print("Fonts loaded successfully")
    
    def _initialize_glow_effects(self):
        """Initialize glow effects for menu items."""
        for i in range(len(self.menu_options)):
            self.glow_effects.append({
                "intensity": 0.0,
                "max_intensity": 2.0,
                "speed": 3.0,
                "phase": i * 0.5  # Offset phases for variety
            })
    
    def handle_event(self, event):
        """
        Handle menu navigation events.
        
        Args:
            event: Pygame event to handle
            
        Returns:
            bool: True if event was handled
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._navigate_up()
                return True
            elif event.key == pygame.K_DOWN:
                self._navigate_down()
                return True
            elif event.key == pygame.K_RETURN:
                # Selection is handled by the state manager
                return True
        
        return False
    
    def _navigate_up(self):
        """Navigate to the previous menu option."""
        self.selected_index = (self.selected_index - 1) % len(self.menu_options)
        print(f"Selected menu option: {self.menu_options[self.selected_index]['text']}")
    
    def _navigate_down(self):
        """Navigate to the next menu option."""
        self.selected_index = (self.selected_index + 1) % len(self.menu_options)
        print(f"Selected menu option: {self.menu_options[self.selected_index]['text']}")
    
    def update(self, dt):
        """
        Update the menu state and animations.
        
        Args:
            dt: Delta time (time since last frame)
        """
        super().update(dt)
        self.animation_time += dt
        
        # Update glow effects
        for i, effect in enumerate(self.glow_effects):
            if i == self.selected_index:
                # Increase glow for selected item
                effect["intensity"] = min(
                    effect["max_intensity"],
                    effect["intensity"] + effect["speed"] * dt
                )
            else:
                # Decrease glow for unselected items
                effect["intensity"] = max(
                    0.0,
                    effect["intensity"] - effect["speed"] * dt
                )
    
    def render(self, screen):
        """
        Render the main menu with retro arcade aesthetics.
        
        Args:
            screen: Pygame surface to render to
        """
        # Clear screen with black background
        screen.fill(MENU_BG_COLOR)
        
        # Render animated background elements
        self._render_background(screen)
        
        # Render title
        self._render_title(screen)
        
        # Render menu options
        self._render_menu_options(screen)
        
        # Render instructions
        self._render_instructions(screen)
        
        # Render border effect
        self._render_border(screen)
    
    def _render_background(self, screen):
        """Render animated background elements."""
        # Create a simple animated grid effect
        grid_spacing = 40
        grid_color = (20, 20, 40)
        
        for x in range(0, SCREEN_WIDTH, grid_spacing):
            alpha = int(50 + 30 * math.sin(self.animation_time + x * 0.01))
            if alpha > 0:
                color_with_alpha = (*grid_color, max(0, min(255, alpha)))
                # Simple line rendering (Pygame doesn't support alpha per-line easily)
                pygame.draw.line(screen, grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)
        
        for y in range(0, SCREEN_HEIGHT, grid_spacing):
            alpha = int(50 + 30 * math.sin(self.animation_time + y * 0.01))
            if alpha > 0:
                color_with_alpha = (*grid_color, max(0, min(255, alpha)))
                pygame.draw.line(screen, grid_color, (0, y), (SCREEN_WIDTH, y), 1)
    
    def _render_title(self, screen):
        """Render the main title with glow effect."""
        title_text = "ARCADE COLLECTION"
        title_surface = self.title_font.render(title_text, True, MENU_TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        
        # Render glow effect
        for offset in range(1, 4):
            glow_surface = self.title_font.render(title_text, True, MENU_TITLE_COLOR)
            glow_rect = title_rect.copy()
            glow_rect.x += offset
            glow_rect.y += offset
            screen.blit(glow_surface, glow_rect)
        
        screen.blit(title_surface, title_rect)
    
    def _render_menu_options(self, screen):
        """Render the menu options with selection highlighting."""
        start_y = MENU_START_Y
        
        for i, option in enumerate(self.menu_options):
            y_pos = start_y + i * MENU_ITEM_SPACING
            color = option["color"]
            
            # Add selection highlighting
            if i == self.selected_index:
                color = MENU_SELECTED_COLOR
                
                # Render selection border
                border_rect = pygame.Rect(
                    MENU_CENTER_X - 150, y_pos - 20,
                    300, 50
                )
                pygame.draw.rect(screen, color, border_rect, 2)
                
                # Render pulsing effect
                pulse_intensity = 0.5 + 0.5 * math.sin(self.animation_time * 4)
                pulse_color = (
                    min(255, int(color[0] * pulse_intensity)),
                    min(255, int(color[1] * pulse_intensity)),
                    min(255, int(color[2] * pulse_intensity))
                )
                border_rect.inflate_ip(10, 6)
                pygame.draw.rect(screen, pulse_color, border_rect, 1)
            
            # Render menu text
            text_surface = self.menu_font.render(option["text"], True, color)
            text_rect = text_surface.get_rect(center=(MENU_CENTER_X, y_pos))
            screen.blit(text_surface, text_rect)
            
            # Render glow effect for selected item
            if i == self.selected_index:
                self._render_text_glow(screen, option["text"], text_rect, color)
    
    def _render_text_glow(self, screen, text, rect, base_color):
        """Render glow effect around text."""
        glow_layers = 3
        for layer in range(1, glow_layers + 1):
            glow_alpha = int(100 - (layer * 25))
            glow_color = (
                min(255, base_color[0] + 50),
                min(255, base_color[1] + 50),
                min(255, base_color[2] + 50)
            )
            
            for offset_x in range(-layer, layer + 1):
                for offset_y in range(-layer, layer + 1):
                    if offset_x != 0 or offset_y != 0:
                        glow_rect = rect.copy()
                        glow_rect.x += offset_x * 2
                        glow_rect.y += offset_y * 2
                        glow_surface = self.menu_font.render(text, True, glow_color)
                        screen.blit(glow_surface, glow_rect)
    
    def _render_instructions(self, screen):
        """Render control instructions."""
        instructions = [
            "Use ARROW KEYS to navigate",
            "Press ENTER to select",
            "ESC to return from games"
        ]
        
        y_start = SCREEN_HEIGHT - 100
        for i, instruction in enumerate(instructions):
            instruction_surface = self.instruction_font.render(instruction, True, Colors.GRAY)
            instruction_rect = instruction_surface.get_rect(
                center=(SCREEN_WIDTH // 2, y_start + i * 25)
            )
            screen.blit(instruction_surface, instruction_rect)
    
    def _render_border(self, screen):
        """Render animated border around the screen."""
        border_color = Colors.DARK_BLUE
        border_alpha = int(100 + 100 * math.sin(self.animation_time * 2))
        
        # Simple border effect
        pygame.draw.rect(screen, border_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), MENU_BORDER_THICKNESS)
        
        # Corner effects
        corner_size = 30
        for corner_x, corner_y in [(0, 0), (SCREEN_WIDTH - corner_size, 0), 
                                   (0, SCREEN_HEIGHT - corner_size), 
                                   (SCREEN_WIDTH - corner_size, SCREEN_HEIGHT - corner_size)]:
            pygame.draw.rect(screen, border_color, 
                           (corner_x, corner_y, corner_size, corner_size), 2)
    
    def get_selected_option(self):
        """
        Get the currently selected menu option.
        
        Returns:
            str: The text of the selected option
        """
        return self.menu_options[self.selected_index]["text"]