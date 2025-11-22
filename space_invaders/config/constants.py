"""
Game Configuration Constants
All configuration values for the Space Invaders game.
"""

import pygame

# Screen Configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_CENTER_X = SCREEN_WIDTH // 2
SCREEN_CENTER_Y = SCREEN_HEIGHT // 2

# Frame Rate
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)
ORANGE = (255, 165, 0)

# Player Colors
PLAYER_COLOR = GREEN
PLAYER_ACCENT_COLOR = WHITE

# Alien Colors (by row - top to bottom)
ALIEN_COLORS = [
    MAGENTA,    # Top row
    CYAN,       # Middle row  
    YELLOW      # Bottom row
]

# Bullet Colors
PLAYER_BULLET_COLOR = WHITE
ENEMY_BULLET_COLOR = RED

# Barrier Colors
BARRIER_COLOR = GRAY
BARRIER_HIGHLIGHT = LIGHT_GRAY
BARRIER_DAMAGE_COLORS = [
    LIGHT_GRAY,  # 75% health
    GRAY,        # 50% health
    DARK_GRAY,   # 25% health
    BLACK        # 0% health (invisible)
]

# UI Colors
UI_COLOR = CYAN
SCORE_COLOR = WHITE
LIVES_COLOR = GREEN
GAME_OVER_COLOR = RED
VICTORY_COLOR = YELLOW

# Font Configuration
TITLE_FONT_SIZE = 72
LARGE_FONT_SIZE = 48
MEDIUM_FONT_SIZE = 36
SMALL_FONT_SIZE = 24
UI_FONT_SIZE = 20

# Player Configuration
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 24
PLAYER_SPEED = 300  # pixels per second
PLAYER_ACCELERATION = 800
PLAYER_FRICTION = 600
PLAYER_LIVES = 3
PLAYER_SHOOT_DELAY = 0.3  # seconds between shots

# Bullet Configuration
BULLET_WIDTH = 4
BULLET_HEIGHT = 10
PLAYER_BULLET_SPEED = 400
ENEMY_BULLET_SPEED = 200
BULLET_COOLDOWN = 0.1

# Alien Configuration
ALIEN_SIZES = {
    'small': (24, 16),      # Top row
    'medium': (32, 24),     # Middle row
    'large': (40, 32)       # Bottom row
}

ALIEN_SPEEDS = {
    'small': 50,
    'medium': 40,
    'large': 30
}

ALIEN_SCORES = {
    'small': 30,     # Top row
    'medium': 20,    # Middle row  
    'large': 10      # Bottom row
}

ALIEN_SHOOT_PROBABILITY = 0.5
ALIEN_SHOOT_INTERVAL = 1.0  # Base shooting interval

# Formation Configuration
FORMATION_ROWS = 5
FORMATION_COLS = 11
FORMATION_HORIZONTAL_SPACING = 50
FORMATION_VERTICAL_SPACING = 40
FORMATION_START_Y = 100
FORMATION_SPEED_MULTIPLIER = 1.0
FORMATION_DROP_DISTANCE = 20

# Barrier Configuration
BARRIER_WIDTH = 64
BARRIER_HEIGHT = 40
BARRIER_BLOCK_SIZE = 8
BARRIER_ROWS = 5
BARRIER_COLS = 8
BARRIER_COUNT = 4
BARRIER_START_Y = SCREEN_HEIGHT - 150
BARRIER_DAMAGE_INTERVAL = 0.1

# Particle Configuration
EXPLOSION_PARTICLE_COUNT = 10
EXPLOSION_PARTICLE_LIFETIME = 1.0
EXPLOSION_PARTICLE_SPEED = 100
IMPACT_PARTICLE_COUNT = 5
IMPACT_PARTICLE_LIFETIME = 0.5
IMPACT_PARTICLE_SPEED = 50

# Game States
GAME_STATE_START = 'start'
GAME_STATE_PLAY = 'play'
GAME_STATE_PAUSE = 'pause'
GAME_STATE_GAME_OVER = 'game_over'
GAME_STATE_VICTORY = 'victory'

# Animation Configuration
ALIEN_ANIMATION_SPEED = 4  # FPS
PLAYER_ANIMATION_SPEED = 6  # FPS
PARTICLE_ANIMATION_SPEED = 8  # FPS

# Sound Configuration
SOUND_VOLUME = 0.5
MUSIC_VOLUME = 0.3

# Input Configuration
KEY_START = pygame.K_f
KEY_SHOOT = pygame.K_b
KEY_PAUSE = pygame.K_ESCAPE
KEY_LEFT = pygame.K_LEFT
KEY_RIGHT = pygame.K_RIGHT
KEY_UP = pygame.K_UP
KEY_DOWN = pygame.K_DOWN

# Debug Configuration
DEBUG_MODE = False
SHOW_FPS = True
SHOW_BOUNDING_BOXES = False