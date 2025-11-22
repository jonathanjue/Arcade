"""
Entities Package
All game entities and objects.

This module exports all entity classes for easy importing throughout the game.
Players can import specific classes like: from src.entities import Player, Bullet, Alien, etc.
"""

from .player import Player
from .bullet import Bullet, BulletPool  
from .alien import Alien, AlienFormation
from .barrier import BarrierBlock, Barrier, BarrierManager
from .particle import Particle, ParticleSystem

__all__ = [
    'Player',
    'Bullet', 'BulletPool',
    'Alien', 'AlienFormation',
    'BarrierBlock', 'Barrier', 'BarrierManager',
    'Particle', 'ParticleSystem'
]