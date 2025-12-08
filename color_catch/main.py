import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Color Catch")

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