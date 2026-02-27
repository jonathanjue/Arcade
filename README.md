# Infection Spread Game

A simple 2D top‑down infection strategy game built with **Pygame**.

## Overview
- Nodes are colored circles connected by lines.
- Player controls a red "virus" circle.
- Neutral nodes are gray, defensive nodes are blue.
- Stay on a neutral node until its resistance timer expires to infect it (turns red).
- Defensive (blue) nodes slow the infection timer.
- Goal: infect all neutral nodes before the level timer runs out.

## Controls
- Arrow keys or **WASD** to move along the connecting lines.

## Files
- `main.py` – game loop, drawing, input handling.
- `requirements.txt` – required Python packages.

Run the game with:
```bash
python main.py
```
