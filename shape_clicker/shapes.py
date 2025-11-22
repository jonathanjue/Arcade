"""Shape drawing and click detection for Shape Clicker"""

import pygame
import math
from constants import *


class ClickableShape:
    """Base class for clickable shapes"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.highlighted = False
        self.color = WHITE
        self.highlight_color = WHITE
    
    def draw(self, screen):
        """Draw the shape on screen"""
        pass
    
    def is_clicked(self, mouse_pos):
        """Check if the shape was clicked"""
        return self.rect.collidepoint(mouse_pos)
    
    def update_highlight(self, mouse_pos):
        """Update highlight state based on mouse position"""
        self.highlighted = self.is_clicked(mouse_pos)
        return self.highlighted


class CircleShape(ClickableShape):
    """Clickable circle shape"""
    
    def __init__(self, x, y, radius=CIRCLE_RADIUS):
        super().__init__(x, y)
        self.radius = radius
        self.color = CIRCLE_COLOR
        self.highlight_color = CIRCLE_HIGHLIGHT_COLOR
        
        # Create collision rectangle
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
    
    def draw(self, screen):
        """Draw the circle on screen"""
        color = self.highlight_color if self.highlighted else self.color
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)
        
        # Draw border
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius, 3)
    
    def is_clicked(self, mouse_pos):
        """Check if circle was clicked using distance calculation"""
        mouse_x, mouse_y = mouse_pos
        distance = math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)
        return distance <= self.radius


class SquareShape(ClickableShape):
    """Clickable square shape"""
    
    def __init__(self, x, y, size=SQUARE_SIZE):
        super().__init__(x, y)
        self.size = size
        self.color = SQUARE_COLOR
        self.highlight_color = SQUARE_HIGHLIGHT_COLOR
        
        # Create collision rectangle
        half_size = size // 2
        self.rect = pygame.Rect(x - half_size, y - half_size, size, size)
    
    def draw(self, screen):
        """Draw the square on screen"""
        color = self.highlight_color if self.highlighted else self.color
        
        # Calculate square position
        half_size = self.size // 2
        rect = pygame.Rect(self.x - half_size, self.y - half_size, self.size, self.size)
        
        pygame.draw.rect(screen, color, rect)
        
        # Draw border
        pygame.draw.rect(screen, WHITE, rect, 3)
    
    def is_clicked(self, mouse_pos):
        """Check if square was clicked using rectangle collision"""
        return self.rect.collidepoint(mouse_pos)


class TriangleShape(ClickableShape):
    """Clickable triangle shape (equilateral)"""
    
    def __init__(self, x, y, side_length=TRIANGLE_SIZE):
        super().__init__(x, y)
        self.side_length = side_length
        self.color = TRIANGLE_COLOR
        self.highlight_color = TRIANGLE_HIGHLIGHT_COLOR
        
        # Calculate triangle points for equilateral triangle
        # Centered at (x, y) with side_length
        import math
        height = side_length * math.sqrt(3) / 2
        
        # Triangle vertices
        self.point1 = (x, y - height / 2)
        self.point2 = (x - side_length / 2, y + height / 2)
        self.point3 = (x + side_length / 2, y + height / 2)
        
        # Create collision rectangle (bounding box)
        min_x = min(self.point1[0], self.point2[0], self.point3[0])
        max_x = max(self.point1[0], self.point2[0], self.point3[0])
        min_y = min(self.point1[1], self.point2[1], self.point3[1])
        max_y = max(self.point1[1], self.point2[1], self.point3[1])
        
        self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    
    def draw(self, screen):
        """Draw the triangle on screen"""
        color = self.highlight_color if self.highlighted else self.color
        
        pygame.draw.polygon(screen, color, [self.point1, self.point2, self.point3])
        
        # Draw border
        pygame.draw.polygon(screen, WHITE, [self.point1, self.point2, self.point3], 3)
    
    def is_clicked(self, mouse_pos):
        """Check if triangle was clicked using point-in-triangle test"""
        mouse_x, mouse_y = mouse_pos
        
        # Bounding box check first for performance
        if not self.rect.collidepoint(mouse_pos):
            return False
            
        # Point-in-triangle test using barycentric coordinates
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        def point_in_triangle(pt, v1, v2, v3):
            d1 = sign(pt, v1, v2)
            d2 = sign(pt, v2, v3)
            d3 = sign(pt, v3, v1)
            
            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            
            return not (has_neg and has_pos)
        
        return point_in_triangle((mouse_x, mouse_y), self.point1, self.point2, self.point3)


class Button:
    """Clickable button for UI"""
    
    def __init__(self, x, y, width, height, text, cost=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.cost = cost
        self.rect = pygame.Rect(x, y, width, height)
        self.enabled = True
        self.clicked = False
    
    def draw(self, screen, font):
        """Draw the button on screen"""
        # Color based on state
        if not self.enabled:
            color = GRAY
        elif self.clicked:
            color = YELLOW
        else:
            color = LIGHT_GRAY
        
        # Draw button background
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw border
        border_color = WHITE if self.enabled else DARK_GRAY
        pygame.draw.rect(screen, border_color, self.rect, 2)
        
        # Draw text
        text_surface = font.render(self.text, True, BLACK if self.enabled else DARK_GRAY)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
        # Draw cost if applicable
        if self.cost > 0:
            cost_font = pygame.font.Font(None, FONT_SMALL)
            cost_text = f"Cost: {self.cost}"
            cost_surface = cost_font.render(cost_text, True, BLACK if self.enabled else DARK_GRAY)
            cost_rect = cost_surface.get_rect(center=(self.rect.centerx, self.rect.bottom - 15))
            screen.blit(cost_surface, cost_rect)
    
    def is_clicked(self, mouse_pos):
        """Check if button was clicked"""
        return self.enabled and self.rect.collidepoint(mouse_pos)
    
    def update_state(self, mouse_pos):
        """Update button state based on mouse position"""
        if self.is_clicked(mouse_pos):
            self.clicked = True
        else:
            self.clicked = False