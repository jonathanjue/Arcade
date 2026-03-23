#!/usr/bin/env python3
"""
Jujutsu Kaisen: Curse Clash
A 2D fighting game with curse techniques and particle-based visual effects.
Controls:
  Player 1:
    A/D - Move left/right
    W - Jump
    S - Block
    J - Light attack
    K - Heavy attack
    L - Special technique (costs cursed energy)
    Space - Ultimate technique (costs full meter)

  Player 2:
    Arrow keys - Move/Jump/Block
    Numpad 1 - Light attack
    Numpad 2 - Heavy attack
    Numpad 3 - Special technique
    Numpad 0 - Ultimate technique

  ESC - Quit
"""

from engine import GameEngine

if __name__ == "__main__":
    game = GameEngine()
    game.run()
