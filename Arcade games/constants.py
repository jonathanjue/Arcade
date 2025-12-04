"""
Constants and shared settings for the Arcade Collection game.
Contains game states, colors, dimensions, and other configuration values.
"""

# Game States
class GameState:
    """Enumeration of possible game states."""
    MENU = "menu"
    DOOM_GAME = "doom_game"
    CONTRA_GAME = "contra_game"
    TETRIS_GAME = "tetris_game"
    QUIT = "quit"

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (RGB)
class Colors:
    """RGB color constants for the arcade aesthetic."""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    DARK_RED = (139, 0, 0)
    DARK_GREEN = (0, 100, 0)
    DARK_BLUE = (0, 0, 139)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)

# Menu colors
MENU_BG_COLOR = Colors.BLACK
MENU_TITLE_COLOR = Colors.YELLOW
MENU_SELECTED_COLOR = Colors.CYAN
MENU_NORMAL_COLOR = Colors.WHITE
MENU_QUIT_COLOR = Colors.RED

# Arcade aesthetic colors
NEON_COLORS = [
    Colors.CYAN,
    Colors.MAGENTA,
    Colors.YELLOW,
    Colors.GREEN,
    Colors.ORANGE,
    Colors.PURPLE
]

# Fonts and text settings
class Fonts:
    """Font settings for different text elements."""
    TITLE_SIZE = 48
    MENU_SIZE = 32
    INSTRUCTION_SIZE = 24
    GAME_TITLE_SIZE = 36
    
    # Try to use system fonts, fallback to default
    TITLE_FONT = None  # Will be loaded in initialization
    MENU_FONT = None   # Will be loaded in initialization
    INSTRUCTION_FONT = None  # Will be loaded in initialization

# Game settings
FPS = 60

# Animation settings
MENU_SELECTION_ANIMATION_SPEED = 0.1
TEXT_GLOW_INTENSITY = 2

# Menu settings
MENU_ANIMATION_SPEED = 5
MENU_BORDER_THICKNESS = 3

# Menu item positions
MENU_CENTER_X = SCREEN_WIDTH // 2
MENU_START_Y = SCREEN_HEIGHT // 2
MENU_ITEM_SPACING = 60

# Visual effects
class Effects:
    """Visual effect settings."""
    PULSE_SPEED = 0.05
    GLOW_BLUR_RADIUS = 5
    SCREEN_FLASH_DURATION = 0.1