"""
Main entry point for the Arcade Collection Pygame application.
Initializes Pygame, sets up game states, and runs the main game loop.
"""

import pygame
import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GameState
from game_states import GameStateManager
from menu import MainMenu
from games.doom import DoomGame
from games.contra import ContraGame
from games.tetris import TetrisGame


def initialize_pygame():
    """
    Initialize Pygame and create the main display surface.
    
    Returns:
        tuple: (screen, clock) - Pygame surface and clock objects
    """
    print("Initializing Pygame...")
    
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Arcade Collection - Retro Gaming Experience")
    
    # Set up the clock for FPS control
    clock = pygame.time.Clock()
    
    # Hide mouse cursor for more arcade-like experience
    pygame.mouse.set_visible(False)
    
    print("Pygame initialized successfully")
    print(f"Screen size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"Target FPS: {FPS}")
    
    return screen, clock


def setup_game_states(screen, clock):
    """
    Set up all game states and the state manager.
    
    Args:
        screen: Pygame surface for rendering
        clock: Pygame clock for timing
        
    Returns:
        GameStateManager: Configured state manager with all handlers
    """
    print("Setting up game states...")
    
    # Create the state manager
    state_manager = GameStateManager(screen, clock)
    
    # Create all game state handlers
    menu_handler = MainMenu()
    doom_handler = DoomGame()
    contra_handler = ContraGame()
    tetris_handler = TetrisGame()
    
    # Set screen and clock for all handlers
    for handler in [menu_handler, doom_handler, contra_handler, tetris_handler]:
        handler.set_screen_and_clock(screen, clock)
    
    # Register handlers with the state manager
    state_manager.set_state_handlers(
        menu_handler=menu_handler,
        doom_handler=doom_handler,
        contra_handler=contra_handler,
        tetris_handler=tetris_handler
    )
    
    print("Game states configured successfully")
    return state_manager


def run_game_loop(state_manager):
    """
    Run the main game loop.
    
    Args:
        state_manager: GameStateManager instance
        
    Returns:
        int: Exit code (0 for success)
    """
    print("Starting main game loop...")
    
    running = True
    last_frame_time = pygame.time.get_ticks()
    
    try:
        while running:
            # Calculate delta time
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_frame_time) / 1000.0  # Convert to seconds
            last_frame_time = current_time
            
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print("Quit event received")
                    running = False
            
            # Forward events to state manager for handling
            if not state_manager.handle_events(events):
                running = False
            
            # Update state manager
            state_manager.update(dt)
            
            # Render current state
            state_manager.render()
            
            # Check if state manager wants to quit
            if state_manager.is_quitting():
                print("State manager requested quit")
                running = False
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            state_manager.clock.tick(FPS)
            
    except Exception as e:
        print(f"Error in game loop: {e}")
        return 1
    
    print("Game loop ended")
    return 0


def cleanup():
    """Clean up Pygame resources."""
    print("Cleaning up...")
    pygame.quit()
    print("Cleanup complete")


def main():
    """
    Main function - entry point of the application.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    print("=" * 50)
    print("ARCADE COLLECTION - Starting Up")
    print("=" * 50)
    
    try:
        # Initialize Pygame
        screen, clock = initialize_pygame()
        
        # Set up game states
        state_manager = setup_game_states(screen, clock)
        
        # Run the main game loop
        exit_code = run_game_loop(state_manager)
        
        # Clean up
        cleanup()
        
        print("=" * 50)
        print("ARCADE COLLECTION - Shutting Down")
        print("=" * 50)
        
        return exit_code
        
    except Exception as e:
        print(f"Fatal error: {e}")
        cleanup()
        return 1


if __name__ == "__main__":
    """
    Entry point when the script is run directly.
    """
    exit_code = main()
    sys.exit(exit_code)