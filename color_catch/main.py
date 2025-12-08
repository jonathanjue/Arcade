import pygame
import sys
import argparse
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game

def parse_arguments():
    """Parse command line arguments for display mode selection"""
    parser = argparse.ArgumentParser(description="Color Catch Game")
    parser.add_argument('--fullscreen', action='store_true', help='Run game in fullscreen mode')
    parser.add_argument('--windowed', action='store_true', help='Run game in windowed mode (default)')
    return parser.parse_args()

def setup_display(fullscreen=False):
    """Set up the display with appropriate flags based on mode"""
    display_flags = pygame.HWSURFACE | pygame.DOUBLEBUF

    if fullscreen:
        # Add fullscreen flag for better recording compatibility
        display_flags |= pygame.FULLSCREEN
        print("Running in fullscreen mode")
    else:
        # Windowed mode with resizable option for better recording
        display_flags |= pygame.RESIZABLE
        print("Running in windowed mode")

    # Set up the display with proper flags
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), display_flags)
    pygame.display.set_caption("Color Catch")

    # Set window properties for better recording compatibility
    pygame.display.set_icon(pygame.Surface((32, 32)))  # Set a basic icon
    pygame.display.set_allow_screensaver(False)  # Prevent screensaver from interfering

    return screen

def main():
    # Initialize Pygame
    pygame.init()

    # Parse command line arguments
    args = parse_arguments()

    # Set up display based on arguments
    screen = setup_display(fullscreen=args.fullscreen)

    # Create game clock
    clock = pygame.time.Clock()

    # Create game instance
    game = Game(screen)

    # Main game loop
    running = True
    while running:
        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize events for better recording compatibility
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)
                pygame.display.set_caption("Color Catch")
                print(f"Window resized to: {event.w}x{event.h}")

        # Handle game events
        game.handle_events(events)

        # Update game state
        game.update()

        # Render game
        game.render()

        # Update display
        pygame.display.flip()

        # Control frame rate
        clock.tick(FPS)

    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()