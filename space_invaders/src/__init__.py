"""Space Invaders Game Package
Core game package containing all major modules and components.
"""

from . import base
from . import entities  
from . import game
from . import managers

__all__ = [
    'base',
    'entities', 
    'game',
    'managers'
]