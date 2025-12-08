# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (RGB format)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Game settings
FPS = 60

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5

# Target settings
TARGET_WIDTH = 30
TARGET_HEIGHT = 30
TARGET_INITIAL_SPEED = 2

# Difficulty progression settings
SPEED_INCREASE_PERCENTAGE = 0.10  # 10% speed increase per collision
MAX_SPEED = 25.0  # Maximum speed cap (increased from 15.0)
SPEED_INDICATOR_COLOR = (200, 200, 200)  # Light gray for speed indicator
TIME_INDICATOR_COLOR = (150, 200, 255)  # Light blue for time indicator

# Visual effects settings
PARTICLE_COUNT = 20  # Number of particles to spawn on collision
PARTICLE_LIFETIME = 60  # Frames for particle to live
PARTICLE_SPEED = 3.0  # Base speed for particles
PARTICLE_SIZE = 5  # Size of particles
SCREEN_SHAKE_DURATION = 15  # Frames for screen shake effect
SCREEN_SHAKE_INTENSITY = 5  # Maximum pixels to shake
PULSE_ANIMATION_SPEED = 0.05  # Speed of pulsing animation
PULSE_ANIMATION_AMOUNT = 0.2  # Amount of size change in pulse
BACKGROUND_STAR_COUNT = 100  # Number of background stars
PARALLAX_LAYERS = 3  # Number of parallax layers
PARALLAX_SPEEDS = [0.5, 1.0, 1.5]  # Speed multipliers for each layer

# Game state constants
START = "START"
PLAYING = "PLAYING"
GAME_OVER = "GAME_OVER"
VICTORY = "VICTORY"
PAUSED = "PAUSED"