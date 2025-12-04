#!/usr/bin/env python3
"""
Pacman Game - Main Entry Point

This module serves as the entry point for the Pacman game.
It initializes the game and starts the main game loop.
"""

def main():
    """Main entry point for the Pacman game."""
    from src.game.game_manager import GameManager

    # Create and run the game manager
    game = GameManager()
    game.run()

if __name__ == "__main__":
    main()