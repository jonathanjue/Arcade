#!/usr/bin/env python3
"""
Space Invaders - Main Game Entry Point
Complete implementation following the development plan specifications.
"""

import pygame
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.game.game_manager import GameManager
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    """Main game entry point."""
    # Initialize pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    
    # Set up the clock for 60 FPS
    clock = pygame.time.Clock()
    
    # Create the game manager
    game_manager = GameManager(screen, clock)
    
    # Main game loop
    running = True
    while running:
        # Calculate delta time
        dt = clock.tick(FPS) / 1000.0
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_manager.handle_events(event)
        
        # Update game state
        game_manager.update(dt)
        
        # Render frame
        game_manager.render()
        
        # Update display
        pygame.display.flip()
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()