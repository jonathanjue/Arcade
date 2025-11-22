"""Base Module
Contains fundamental base classes for the Space Invaders game.
"""

from .game_object import GameObject
from .sprite_object import SpriteObject

__all__ = [
    'GameObject',
    'SpriteObject'
]