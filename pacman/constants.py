"""
Pacman Game Constants

This module contains all game configuration constants.
"""

# Game window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pacman"
TARGET_FPS = 60

# Game colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)

# Game settings
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Player settings
PACMAN_SPEED = 150
PACMAN_SIZE = CELL_SIZE
PACMAN_START_LIVES = 3

# Ghost settings
GHOST_SPEED = 120
GHOST_SIZE = CELL_SIZE
GHOST_COUNT = 3

# Game state constants
STATE_MENU = "menu"
STATE_PLAY = "play"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"

# Input constants
INPUT_UP = "up"
INPUT_DOWN = "down"
INPUT_LEFT = "left"
INPUT_RIGHT = "right"
INPUT_ENTER = "enter"
INPUT_ESCAPE = "escape"