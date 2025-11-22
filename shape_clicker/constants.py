"""Game constants for Shape Clicker"""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)
BLUE = (0, 100, 200)
LIGHT_BLUE = (100, 150, 220)
RED = (200, 50, 50)
GREEN = (50, 150, 50)
YELLOW = (255, 215, 0)

# Font settings
FONT_SMALL = 24
FONT_MEDIUM = 32
FONT_LARGE = 48

# Circle stage constants
CIRCLE_RADIUS = 80
CIRCLE_COLOR = BLUE
CIRCLE_HIGHLIGHT_COLOR = LIGHT_BLUE

# Square stage constants
SQUARE_SIZE = 160
SQUARE_COLOR = RED
SQUARE_HIGHLIGHT_COLOR = (255, 100, 100)

# Triangle stage constants
TRIANGLE_SIZE = 120
TRIANGLE_COLOR = GREEN
TRIANGLE_HIGHLIGHT_COLOR = (100, 255, 100)

# Point requirements
CIRCLE_MAX_POINTS = 10000
SQUARE_MAX_POINTS = 15000  # Updated to 15,000 as per requirements
TRIANGLE_MAX_POINTS = 20000  # Victory condition

# Upgrade constants by stage
# Circle stage
CIRCLE_CLICK_POWER_BASE_COST = 10
CIRCLE_AUTO_CLICKER_BASE_COST = 25
# Square stage  
SQUARE_CLICK_POWER_BASE_COST = 100
SQUARE_AUTO_CLICKER_BASE_COST = 250
# Triangle stage
TRIANGLE_CLICK_POWER_BASE_COST = 1000
TRIANGLE_AUTO_CLICKER_BASE_COST = 2500

# General upgrade multipliers
CLICK_POWER_COST_MULTIPLIER = 1.5
AUTO_CLICKER_COST_MULTIPLIER = 1.3

# Progression rewards
SQUARE_CLICK_REWARD = 5  # Points per click in square stage
TRIANGLE_CLICK_REWARD = 25  # Points per click in triangle stage

# UI layout
UI_PADDING = 20
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
BUTTON_SPACING = 10

# Achievement constants
ACHIEVEMENT_FADE_DURATION = 5.0  # Seconds to display achievements
ACHIEVEMENT_MULTIPLIER = 1.25  # Multiplier when advancing stages (if auto clickers owned)
ACHIEVEMENT_GOLD = (255, 215, 0)  # Gold color for achievements

# Achievement names
ACHIEVEMENT_PURE_CLICKER = "Pure Clicker"
ACHIEVEMENT_AUTO_MASTER = "Auto Master"
ACHIEVEMENT_ROBOT = "ROBOT"

# Achievement descriptions
ACHIEVEMENT_PURE_CLICKER_DESC = "Beat the game using only Click Power!"
ACHIEVEMENT_AUTO_MASTER_DESC = "Beat the game using only Auto Clickers!"
ACHIEVEMENT_ROBOT_DESC = "Beat the game using only Auto Clickers, no clicking!"

# Game starting points
STARTING_CIRCLE_POINTS = 100

# Timewarp multiplier
TIMEWARP_MULTIPLIER = 100

# Music system
MUSIC_FILES = {
    'loonboon': 'musicforgame1.mp3',
    'doometernal': 'musicforgame2.mp3',
    'tetris': 'musicforgame3.mp3',
    'coin': 'musicforgame4.mp3',
    'boss': 'boss.mp3',
    'gamestart': 'gamestart.mp3',
    'ending': 'ending.mp3'
}

MUSIC_NAMES = {
    'loonboon': 'Loonboon Music',
    'doometernal': 'Doom Eternal Music', 
    'tetris': 'Tetris Music',
    'coin': 'Coin Music',
    'boss': 'Boss Music',
    'gamestart': 'Game Start',
    'ending': 'Ending'
}

# Music button layout
MUSIC_BUTTON_WIDTH = 200
MUSIC_BUTTON_HEIGHT = 40
MUSIC_BUTTON_Y_START = SCREEN_HEIGHT - 60

# Powerup helpers
POWERUP_DURATION = 10.0  # seconds
POWERUP_MULTIPLIER = 10.0
POWERUP_COST_FACTOR = 5  # Powerup costs 5x normal upgrade cost

# Expert mode
EXPERT_CLICK_POWER_START = 0.75
EXPERT_MODE_UNLOCKED = False  # Will be set when both achievements are earned

# Compound stage (triangle + square + circle)
COMPOUND_MAX_POINTS = 50000
COMPOUND_COLOR = (255, 215, 0)  # Golden

# Shape colors
SHAPE_COLORS = {
    'red': (200, 50, 50),
    'green': (50, 150, 50),
    'blue': (0, 100, 200),
    'purple': (150, 50, 150),
    'default': None  # Will use stage default color
}