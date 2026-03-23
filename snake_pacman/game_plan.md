# Snake-Man: Final Plan

## Grid & Display
- Window: 600x600px, 20x20 grid, 30px per tile
- FPS: 60 render, game logic tick every 100ms (10 moves/sec)
- Background: black, grid lines optional

## Snake (snake.py)
- `segments`: list of (x, y) tuples, index 0 = head
- Start: length 3, center of grid, moving right
- Movement: append new head, remove tail (unless growing)
- Direction: stored as (dx, dy), cannot reverse (if moving right, left input ignored until next move)
- Death: head collides with own body OR segments == 0 after ghost hit
- Grow: append head without removing tail

## Pellets (pellet.py)
- Spawn: random empty tile, one at a time
- Value: +1 segment, +10 points
- Respawn immediately after eaten

## Powerup (pellet.py)
- Spawn: every 30 seconds on random empty tile
- Duration: 10 seconds active, disappears if not picked up after 15 seconds
- Effect: enables shooting, spacebar fires projectile
- Visual: white star, blinks (alternate visible/hidden every 200ms)

## Ghosts (ghost.py)
- Count: 4, spawn at corners
- Movement: every tick, pick direction toward player with 70% probability, random with 30%
- Cannot reverse direction
- Collision with snake body: no effect
- Collision with snake head: player loses last segment, ghost teleports to spawn
- Killed by projectile: ghost removed, respawns at corner after 5 seconds
- Speed increase: every 100 points, ghost tick rate decreases by 10ms (min 50ms)

## Projectiles
- Fired from snake head in current direction
- Speed: 2 tiles per tick
- Destroyed on: hit ghost, hit wall, or travel 10 tiles
- Max 3 projectiles on screen at once

## Win/Lose
- Win: score >= 500
- Lose: segments == 0

## HUD (renderer.py)
- Top bar: "Score: X | Length: X | Power: ACTIVE/COOLDOWN"
- Font: pygame default, white, size 24

## Entry Point (main.py)
- Pygame init, game loop, event handling
- Calls game.update() and renderer.draw()
- Restart: R key on game over

## Simplified File Structure
```
snake_pacman/
├── main.py        # Pygame loop, events
├── game.py        # All game logic (snake, ghosts, pellets, collisions)
└── renderer.py    # All drawing
```
- 3 files only. Keep it simple.
