import pygame
import sys
import traceback

def main():
    pygame.init()
    try:
        from engine import GameEngine
        engine = GameEngine()
        engine.run()
    except Exception:
        traceback.print_exc()
        print("\nPress ENTER to exit...")
        input()
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()
