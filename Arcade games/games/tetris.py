"""
Tetris game placeholder for the Arcade Collection.
Displays a "coming soon" message with puzzle/block styling and returns to menu on ESC.
"""

import pygame
import math
import random
from game_states import BaseGameState
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, Colors, Fonts,
    NEON_COLORS
)


class TetrisGame(BaseGameState):
    """
    Placeholder game handler for Tetris.
    Shows a coming soon message with puzzle/block styling.
    """
    
    def __init__(self):
        """Initialize the Tetris game placeholder."""
        super().__init__()
        self.animation_time = 0.0
        self.falling_blocks = []
        self.completed_lines = []
        
        # Tetris piece colors
        self.piece_colors = [
            Colors.CYAN,    # I piece
            Colors.BLUE,    # J piece
            Colors.ORANGE,  # L piece
            Colors.YELLOW,  # O piece
            Colors.GREEN,   # S piece
            Colors.PURPLE,  # T piece
            Colors.RED      # Z piece
        ]
        
        # Load fonts
        self._load_fonts()
        
        # Initialize falling blocks
        self._initialize_blocks()
        
        print("TetrisGame initialized")
    
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
    
    def _initialize_blocks(self):
        """Initialize falling blocks for visual effect."""
        for _ in range(8):
            self._spawn_block()
    
    def _spawn_block(self):
        """Spawn a new falling block."""
        block_type = random.randint(0, 6)  # 0-6 for different tetris pieces
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(-100, 0)
        
        # Different falling speeds for variety
        speed = random.uniform(30, 80)
        
        self.falling_blocks.append({
            'x': x,
            'y': y,
            'speed': speed,
            'type': block_type,
            'color': self.piece_colors[block_type]
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
        
        # Update falling blocks
        blocks_to_remove = []
        
        for i, block in enumerate(self.falling_blocks):
            block['y'] += block['speed'] * dt
            
            # Remove blocks that fall off screen and respawn them
            if block['y'] > SCREEN_HEIGHT:
                blocks_to_remove.append(i)
        
        # Remove old blocks and spawn new ones
        for i in reversed(blocks_to_remove):
            self.falling_blocks.pop(i)
            self._spawn_block()
        
        # Occasionally add more blocks
        if len(self.falling_blocks) < 10 and random.random() < 0.02:
            self._spawn_block()
    
    def render(self, screen):
        """
        Render the Tetris game placeholder.
        
        Args:
            screen: Pygame surface to render to
        """
        # Clear screen with dark background
        screen.fill(Colors.BLACK)
        
        # Render grid background
        self._render_grid(screen)
        
        # Render title
        self._render_title(screen)
        
        # Render falling blocks
        self._render_blocks(screen)
        
        # Render completed lines effect
        self._render_lines_effect(screen)
        
        # Render coming soon message
        self._render_message(screen)
        
        # Render instructions
        self._render_instructions(screen)
    
    def _render_grid(self, screen):
        """Render Tetris-style grid background."""
        grid_size = 30
        
        # Draw grid lines
        for x in range(0, SCREEN_WIDTH, grid_size):
            pygame.draw.line(screen, Colors.DARK_GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
        
        for y in range(0, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(screen, Colors.DARK_GRAY, (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw game area border
        game_area = pygame.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
        pygame.draw.rect(screen, Colors.BLUE, game_area, 3)
        
        # Add some subtle scrolling effect
        scroll_offset = int(self.animation_time * 20) % grid_size
        for x in range(scroll_offset, SCREEN_WIDTH, grid_size):
            alpha = int(100 + 100 * math.sin(self.animation_time + x * 0.01))
            color = (50, 50, 50, max(0, min(255, alpha)))
            pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, SCREEN_HEIGHT), 1)
    
    def _render_blocks(self, screen):
        """Render falling Tetris blocks."""
        for block in self.falling_blocks:
            x, y = int(block['x']), int(block['y'])
            color = block['color']
            block_type = block['type']
            
            # Draw block based on type
            if block_type == 0:  # I piece
                pygame.draw.rect(screen, color, (x - 15, y, 30, 20))
                pygame.draw.rect(screen, Colors.WHITE, (x - 15, y, 30, 20), 2)
            elif block_type == 1:  # J piece
                pygame.draw.rect(screen, color, (x - 10, y - 10, 20, 30))
                pygame.draw.rect(screen, Colors.WHITE, (x - 10, y - 10, 20, 30), 2)
            elif block_type == 2:  # L piece
                pygame.draw.rect(screen, color, (x - 10, y - 10, 20, 30))
                pygame.draw.rect(screen, Colors.WHITE, (x - 10, y - 10, 20, 30), 2)
            elif block_type == 3:  # O piece
                pygame.draw.rect(screen, color, (x - 10, y - 10, 20, 20))
                pygame.draw.rect(screen, Colors.WHITE, (x - 10, y - 10, 20, 20), 2)
            elif block_type == 4:  # S piece
                pygame.draw.rect(screen, color, (x - 15, y, 30, 15))
                pygame.draw.rect(screen, color, (x, y - 15, 15, 15))
                pygame.draw.rect(screen, Colors.WHITE, (x - 15, y, 30, 15), 2)
                pygame.draw.rect(screen, Colors.WHITE, (x, y - 15, 15, 15), 2)
            elif block_type == 5:  # T piece
                pygame.draw.rect(screen, color, (x - 15, y - 10, 30, 15))
                pygame.draw.rect(screen, color, (x - 5, y - 25, 10, 15))
                pygame.draw.rect(screen, Colors.WHITE, (x - 15, y - 10, 30, 15), 2)
                pygame.draw.rect(screen, Colors.WHITE, (x - 5, y - 25, 10, 15), 2)
            elif block_type == 6:  # Z piece
                pygame.draw.rect(screen, color, (x, y - 15, 15, 15))
                pygame.draw.rect(screen, color, (x - 15, y, 30, 15))
                pygame.draw.rect(screen, Colors.WHITE, (x, y - 15, 15, 15), 2)
                pygame.draw.rect(screen, Colors.WHITE, (x - 15, y, 30, 15), 2)
    
    def _render_lines_effect(self, screen):
        """Render completed lines effect."""
        # Create some animated completed line effects
        for i in range(3):
            y = 200 + i * 80 + 40 * math.sin(self.animation_time * 2 + i)
            alpha = int(150 + 105 * math.sin(self.animation_time * 4 + i))
            
            if alpha > 200:
                color = (255, 255, 0)  # Yellow line
                pygame.draw.rect(screen, color, (120, y, SCREEN_WIDTH - 240, 4))
    
    def _render_title(self, screen):
        """Render the game title with Tetris styling."""
        title_text = "TETRIS"
        title_color = Colors.CYAN
        
        # Render with block-style borders
        for offset in range(1, 4):
            # Border rectangles around title
            border_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - 100 + offset,
                80 + offset,
                200 - 2 * offset,
                40 - 2 * offset
            )
            pygame.draw.rect(screen, Colors.BLUE, border_rect, 2)
        
        # Render main title
        title_surface = self.title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # Render subtitle with falling effect
        subtitle_text = "BLOCK PUZZLE READY"
        subtitle_color = Colors.YELLOW
        
        subtitle_surface = self.instruction_font.render(subtitle_text, True, subtitle_color)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 140))
        screen.blit(subtitle_surface, subtitle_rect)
    
    def _render_message(self, screen):
        """Render the coming soon message."""
        message = "GAME COMING SOON!"
        message_color = Colors.YELLOW
        
        # Create block-style message background
        block_size = 20
        msg_width = len(message) * 12  # Rough estimate
        msg_height = 30
        
        msg_x = (SCREEN_WIDTH - msg_width) // 2
        msg_y = SCREEN_HEIGHT // 2 - 15
        
        # Draw blocky background
        for x in range(0, msg_width, block_size):
            for y in range(0, msg_height, block_size):
                if (x + y) % (block_size * 2) == 0:
                    pygame.draw.rect(screen, Colors.DARK_GRAY, 
                                   (msg_x + x, msg_y + y, block_size, block_size))
        
        pygame.draw.rect(screen, Colors.CYAN, 
                        (msg_x, msg_y, msg_width, msg_height), 3)
        
        # Render main message
        main_surface = self.message_font.render(message, True, message_color)
        main_rect = main_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(main_surface, main_rect)
        
        # Additional message
        sub_message = "Get ready to stack!"
        sub_surface = self.instruction_font.render(sub_message, True, Colors.WHITE)
        sub_rect = sub_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(sub_surface, sub_rect)
    
    def _render_instructions(self, screen):
        """Render control instructions."""
        instruction_text = "Press ESC to return to menu"
        instruction_color = Colors.CYAN
        
        instruction_surface = self.instruction_font.render(instruction_text, True, instruction_color)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        
        # Add Tetris-style background
        block_size = 8
        for x in range(-20, instruction_surface.get_width() + 20, block_size):
            for y in range(-5, 10, block_size):
                if random.random() < 0.3:
                    color = random.choice(self.piece_colors)
                    pygame.draw.rect(screen, color, 
                                   (instruction_rect.x + x, instruction_rect.y + y, 
                                    block_size, block_size))
        
        screen.blit(instruction_surface, instruction_rect)
    
    def render_next_piece_preview(self, screen, x, y):
        """Render preview of next piece (for future Tetris implementation)."""
        # Placeholder for next piece preview
        preview_rect = pygame.Rect(x, y, 60, 60)
        pygame.draw.rect(screen, Colors.DARK_GRAY, preview_rect, 2)
        
        preview_text = "NEXT"
        preview_surface = self.instruction_font.render(preview_text, True, Colors.WHITE)
        preview_text_rect = preview_surface.get_rect(center=(x + 30, y + 30))
        screen.blit(preview_surface, preview_text_rect)