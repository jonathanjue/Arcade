# main.py – Shadow Swap Puzzle Game
"""
A minimal top‑down puzzle game built with pygame.

Features implemented from the spec:
* Player (blue square) moves with WASD, smooth movement.
* Shadow (dark gray) follows the player's past positions with a fixed delay.
* Press SPACE to swap player and shadow positions (1 s cooldown).
* Walls (light gray), switches (green circles) and doors (red rectangles).
* Switches open doors when either player or shadow stands on them.
* Simple level layout defined in code.
"""

import pygame
import sys
from collections import deque

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
PLAYER_SIZE = 40
SHADOW_SIZE = 40
WALL_COLOR = (200, 200, 200)
PLAYER_COLOR = (0, 0, 255)
SHADOW_COLOR = (50, 50, 50)
SWITCH_COLOR = (0, 200, 0)
DOOR_COLOR = (200, 0, 0)
EXIT_COLOR = (128, 0, 128)

# History settings – 2 seconds delay at 60 FPS → 120 frames
DELAY_FRAMES = 120
HISTORY_MAXLEN = DELAY_FRAMES + 10  # a little extra safety

SWAP_COOLDOWN = 1000  # milliseconds

# ---------------------------------------------------------------------------
# Helper classes
# ---------------------------------------------------------------------------
class Wall(pygame.Rect):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

class Switch:
    def __init__(self, x, y, radius=15):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.activated = False
        self.linked_doors = []  # doors this switch controls

    def check(self, player_rect, shadow_rect):
        # Activate if either rect collides with the circle
        if self.pos.distance_to(player_rect.center) <= self.radius or \
           self.pos.distance_to(shadow_rect.center) <= self.radius:
            self.activated = True
            for door in self.linked_doors:
                door.open = True
        else:
            self.activated = False
            for door in self.linked_doors:
                door.open = False

    def draw(self, surf):
        color = (0, 255, 0) if self.activated else SWITCH_COLOR
        pygame.draw.circle(surf, color, self.pos, self.radius)

class Door(pygame.Rect):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.open = False

    def draw(self, surf):
        if not self.open:
            pygame.draw.rect(surf, DOOR_COLOR, self)

class Player:
    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.vel = pygame.Vector2(0, 0)
        self.speed = 4.0

    def handle_input(self, keys):
        self.vel.x = self.vel.y = 0
        if keys[pygame.K_a]:
            self.vel.x = -self.speed
        if keys[pygame.K_d]:
            self.vel.x = self.speed
        if keys[pygame.K_w]:
            self.vel.y = -self.speed
        if keys[pygame.K_s]:
            self.vel.y = self.speed

    def move(self, walls):
        # Move on X axis
        self.rect.x += self.vel.x
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.vel.x > 0:
                    self.rect.right = wall.left
                elif self.vel.x < 0:
                    self.rect.left = wall.right
        # Move on Y axis
        self.rect.y += self.vel.y
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.vel.y > 0:
                    self.rect.bottom = wall.top
                elif self.vel.y < 0:
                    self.rect.top = wall.bottom

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

class Shadow:
    def __init__(self, size, color, delay_frames, history):
        self.rect = pygame.Rect(0, 0, size, size)
        self.color = color
        self.delay = delay_frames
        self.history = history  # reference to the shared deque
        self.last_pos = pygame.Vector2(0, 0)

    def update(self, walls):
        # If we have enough history, follow the delayed position
        if len(self.history) > self.delay:
            pos = self.history[-self.delay]
            self.rect.topleft = (int(pos.x), int(pos.y))
        # Simple wall collision – shadow stops at walls (optional behaviour)
        for wall in walls:
            if self.rect.colliderect(wall):
                # revert to previous safe position
                self.rect.topleft = (int(self.last_pos.x), int(self.last_pos.y))
                break
        self.last_pos = pygame.Vector2(self.rect.topleft)

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

# ---------------------------------------------------------------------------
# Level definition – multiple levels support
# ---------------------------------------------------------------------------

def create_levels():
    """Return a list of level dictionaries.
    Each dict contains: walls, switches, doors, exit_rect, moving_walls, pressure_plates.
    """
    levels = []

    # ---------- Level 1 – basic delay teaching ----------
    walls1 = [
        Wall(0, 0, SCREEN_WIDTH, 20),  # top border
        Wall(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),  # bottom
        Wall(0, 0, 20, SCREEN_HEIGHT),  # left
        Wall(SCREEN_WIDTH - 20, 0, 20, SCREEN_HEIGHT),  # right
        Wall(200, 150, 400, 20),  # horizontal wall
        Wall(200, 150, 20, 300),  # vertical wall
    ]
    door1 = Door(600, 400, 60, 20)
    switch1 = Switch(250, 200)
    switch1.linked_doors.append(door1)
    exit1 = pygame.Rect(700, 500, 60, 60)
    levels.append({
        "walls": walls1,
        "switches": [switch1],
        "doors": [door1],
        "moving_walls": [],
        "pressure_plates": [],
        "exit": exit1,
    })

    # ---------- Level 2 – two switches, two doors ----------
    walls2 = walls1.copy()
    door2a = Door(500, 300, 60, 20)
    door2b = Door(650, 200, 60, 20)
    switch2a = Switch(150, 400)
    switch2b = Switch(550, 100)
    switch2a.linked_doors.append(door2a)
    switch2b.linked_doors.append(door2b)
    exit2 = pygame.Rect(750, 50, 60, 60)
    levels.append({
        "walls": walls2,
        "switches": [switch2a, switch2b],
        "doors": [door2a, door2b],
        "moving_walls": [],
        "pressure_plates": [],
        "exit": exit2,
    })

    # ---------- Level 3 – moving wall and pressure plate ----------
    walls3 = walls1.copy()
    # Moving wall will slide horizontally between x=300 and x=500
    moving_wall = Wall(300, 350, 200, 20)
    # Pressure plate (requires continuous stand)
    plate = Switch(400, 250, radius=12)  # reuse Switch as plate
    plate.linked_doors.append(Door(600, 100, 60, 20))
    exit3 = pygame.Rect(750, 500, 60, 60)
    levels.append({
        "walls": walls3,
        "switches": [],
        "doors": [],
        "moving_walls": [moving_wall],
        "pressure_plates": [plate],
        "exit": exit3,
    })

    return levels

# Helper for moving walls (simple back‑and‑forth)
class MovingWall:
    def __init__(self, rect, axis="x", range_min=0, range_max=0, speed=2):
        self.rect = rect
        self.axis = axis
        self.min = range_min
        self.max = range_max
        self.speed = speed
        self.direction = 1

    def update(self):
        if self.axis == "x":
            self.rect.x += self.speed * self.direction
            if self.rect.x < self.min or self.rect.x > self.max:
                self.direction *= -1
                self.rect.x += self.speed * self.direction
        else:
            self.rect.y += self.speed * self.direction
            if self.rect.y < self.min or self.rect.y > self.max:
                self.direction *= -1
                self.rect.y += self.speed * self.direction

# ---------------------------------------------------------------------------
# Main game loop – now supports level progression
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Shadow Swap Puzzle")
    clock = pygame.time.Clock()

    levels = create_levels()
    current_level_index = 0

    def load_level(idx):
        lvl = levels[idx]
        return (
            lvl["walls"],
            lvl["switches"],
            lvl["doors"],
            [MovingWall(w, "x", w.x, w.x + 200, 2) for w in lvl.get("moving_walls", [])],
            lvl.get("pressure_plates", []),
            lvl["exit"],
        )

    walls, switches, doors, moving_walls, pressure_plates, exit_rect = load_level(current_level_index)

    player = Player(100, 100, PLAYER_SIZE, PLAYER_COLOR)
    history = deque(maxlen=HISTORY_MAXLEN)
    shadow = Shadow(SHADOW_SIZE, SHADOW_COLOR, DELAY_FRAMES, history)
    last_swap_time = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    now = pygame.time.get_ticks()
                    if now - last_swap_time >= SWAP_COOLDOWN:
                        player_pos = pygame.Vector2(player.rect.topleft)
                        shadow_pos = pygame.Vector2(shadow.rect.topleft)
                        player.rect.topleft = (int(shadow_pos.x), int(shadow_pos.y))
                        shadow.rect.topleft = (int(player_pos.x), int(player_pos.y))
                        last_swap_time = now

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.move(walls + [mw.rect for mw in moving_walls])

        # Record player position after movement
        history.append(pygame.Vector2(player.rect.topleft))
        shadow.update(walls + [mw.rect for mw in moving_walls])

        # Update moving walls
        for mw in moving_walls:
            mw.update()

        # Switch logic (activate doors)
        for sw in switches:
            sw.check(player.rect, shadow.rect)
        # Pressure plates act like switches but stay open only while held
        for pp in pressure_plates:
            pp.check(player.rect, shadow.rect)

        # Win condition – advance level or finish
        if player.rect.colliderect(exit_rect):
            if current_level_index + 1 < len(levels):
                current_level_index += 1
                walls, switches, doors, moving_walls, pressure_plates, exit_rect = load_level(current_level_index)
                # reset player & shadow positions
                player.rect.topleft = (100, 100)
                shadow.rect.topleft = (100, 100)
                history.clear()
                print(f"Level {current_level_index + 1} loaded!")
            else:
                print("You completed all levels! Congratulations.")
                running = False

        # Rendering
        screen.fill((30, 30, 30))
        for wall in walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
        for mw in moving_walls:
            pygame.draw.rect(screen, (150, 150, 150), mw.rect)
        for door in doors:
            door.draw(screen)
        for sw in switches:
            sw.draw(screen)
        for pp in pressure_plates:
            pp.draw(screen)
        pygame.draw.rect(screen, EXIT_COLOR, exit_rect)
        player.draw(screen)
        shadow.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# Main game loop
# ---------------------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Shadow Swap Puzzle")
    clock = pygame.time.Clock()

    # Initialise objects
    player = Player(100, 100, PLAYER_SIZE, PLAYER_COLOR)
    history = deque(maxlen=HISTORY_MAXLEN)
    shadow = Shadow(SHADOW_SIZE, SHADOW_COLOR, DELAY_FRAMES, history)
    walls, switches, doors, exit_rect = create_level()

    last_swap_time = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    now = pygame.time.get_ticks()
                    if now - last_swap_time >= SWAP_COOLDOWN:
                        # Perform swap
                        player_pos = pygame.Vector2(player.rect.topleft)
                        shadow_pos = pygame.Vector2(shadow.rect.topleft)
                        player.rect.topleft = (int(shadow_pos.x), int(shadow_pos.y))
                        shadow.rect.topleft = (int(player_pos.x), int(player_pos.y))
                        last_swap_time = now

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.move(walls)

        # Record player position after movement
        history.append(pygame.Vector2(player.rect.topleft))
        shadow.update(walls)

        # Switch logic (activate doors)
        for sw in switches:
            sw.check(player.rect, shadow.rect)

        # Win condition
        if player.rect.colliderect(exit_rect):
            print("You reached the exit! Congratulations.")
            running = False

        # Rendering
        screen.fill((30, 30, 30))
        for wall in walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
        for door in doors:
            door.draw(screen)
        for sw in switches:
            sw.draw(screen)
        pygame.draw.rect(screen, EXIT_COLOR, exit_rect)
        player.draw(screen)
        shadow.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
