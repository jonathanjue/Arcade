# Snake-Man: Snake + Pac-Man Hybrid

## Game Concept
Grid-based snake game with Pac-Man elements. Collect pellets to grow, avoid ghosts, grab powerups to shoot ghosts.

## Phase 1: Core Mechanics
- Grid-based movement (20x20 tile grid)
- Snake moves continuously in current direction
- Arrow keys change direction (no reverse)
- Snake head + body segments tracked as coordinate list
- Game loop at 10 FPS (adjustable speed)

## Phase 2: Game Logic
- Pellets spawn randomly on grid
- Eating pellet: +1 segment, +10 points
- Ghosts: 4 ghosts, move semi-randomly toward player
- Ghost collision: lose last segment (death if 0 segments)
- Powerup: appears every 30 seconds, lasts 10 seconds
- Powerup active: spacebar shoots projectile from head
- Projectile kills ghost on hit, ghost respawns after 5 seconds
- Win: reach 500 points. Lose: 0 segments remaining.

## Phase 3: Display
- Pygame window, 600x600 pixels (30px per tile)
- Snake: green rectangles, head is brighter
- Pellets: yellow circles
- Ghosts: colored rectangles (red, pink, cyan, orange)
- Powerup: flashing white star
- Projectile: white dot
- HUD: score, segments, powerup timer

## Phase 4: Polish
- Sound effects (eat, shoot, death, powerup)
- Game over screen with restart option
- Difficulty: ghosts get faster every 100 points
- Title screen

## File Structure
```
snake_pacman/
├── main.py          # Entry point
├── snake.py         # Snake class
├── ghost.py         # Ghost class
├── pellet.py        # Pellet/Powerup logic
├── game.py          # Game state manager
├── renderer.py      # Pygame rendering
└── sounds/          # Sound effects (optional)
```
