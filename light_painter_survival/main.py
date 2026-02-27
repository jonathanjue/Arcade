# main.py – Light Painter Survival (Pygame)
"""
A top‑down survival game where you (blue circle) draw temporary light barriers
to block red‑circle enemies. Barriers fade after a few seconds.

Controls:
  • WASD – move player
  • Hold LEFT MOUSE BUTTON (or SPACE) – draw a barrier from the player toward the mouse

The game includes a menu, barrier limits, cooldowns, and a simple pause system.
"""

import pygame
import random
import math

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (30, 30, 30)          # dark gray
PLAYER_COLOR = (0, 120, 255)      # blue
ENEMY_COLOR = (255, 50, 50)       # red
BARRIER_COLOR = (255, 255, 150)   # pale yellow (glowing)

PLAYER_RADIUS = 15
ENEMY_RADIUS = 12
PLAYER_SPEED = 4
ENEMY_SPEED = 2

BARRIER_WIDTH = 5
BARRIER_LIFETIME = 4000   # ms (fully visible)
BARRIER_FADE_TIME = 2000  # ms (fade out)

SPAWN_INTERVAL = 2000      # ms – enemy spawn rate
DIFFICULTY_RAMP = 0.001    # speed increase per ms survived

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

# ------------------------------------------------------------
# Game objects
# ------------------------------------------------------------
class Player:
    def __init__(self, pos):
        self.pos = list(pos)
        self.radius = PLAYER_RADIUS

    def handle_input(self, keys):
        dx = dy = 0
        if keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_s]: dy += 1
        if keys[pygame.K_a]: dx -= 1
        if keys[pygame.K_d]: dx += 1
        if dx or dy:
            length = math.hypot(dx, dy)
            dx, dy = dx / length, dy / length
            self.pos[0] += dx * PLAYER_SPEED
            self.pos[1] += dy * PLAYER_SPEED
            # clamp to screen
            self.pos[0] = max(self.radius, min(SCREEN_WIDTH - self.radius, self.pos[0]))
            self.pos[1] = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.pos[1]))

    def draw(self, surf):
        pygame.draw.circle(surf, PLAYER_COLOR, (int(self.pos[0]), int(self.pos[1])), self.radius)

class Enemy:
    def __init__(self, pos, speed):
        self.pos = list(pos)
        self.radius = ENEMY_RADIUS
        self.speed = speed

    def update(self, player_pos, barriers):
        # vector toward player
        dx = player_pos[0] - self.pos[0]
        dy = player_pos[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        dx /= dist
        dy /= dist
        # check barrier blockage
        blocked = any(line_intersects_circle(b.start, b.end, self.pos, self.radius) for b in barriers)
        if not blocked:
            self.pos[0] += dx * self.speed
            self.pos[1] += dy * self.speed
        # keep inside bounds
        self.pos[0] = max(self.radius, min(SCREEN_WIDTH - self.radius, self.pos[0]))
        self.pos[1] = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.pos[1]))

    def draw(self, surf):
        pygame.draw.circle(surf, ENEMY_COLOR, (int(self.pos[0]), int(self.pos[1])), self.radius)

class Barrier:
    def __init__(self, start, end, created_at):
        self.start = start
        self.end = end
        self.created_at = created_at

    def age(self, now):
        return now - self.created_at

    def is_dead(self, now):
        return self.age(now) > BARRIER_LIFETIME + BARRIER_FADE_TIME

    def draw(self, surf, now):
        age = self.age(now)
        if age < BARRIER_LIFETIME:
            alpha = 255
        elif age < BARRIER_LIFETIME + BARRIER_FADE_TIME:
            alpha = int(255 * (1 - (age - BARRIER_LIFETIME) / BARRIER_FADE_TIME))
        else:
            return
        line_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(line_surf, BARRIER_COLOR + (alpha,), self.start, self.end, BARRIER_WIDTH)
        surf.blit(line_surf, (0, 0))

# ------------------------------------------------------------
# Geometry helper – line vs circle intersection
# ------------------------------------------------------------
def line_intersects_circle(p1, p2, center, radius):
    (x1, y1), (x2, y2) = p1, p2
    cx, cy = center
    dx, dy = x2 - x1, y2 - y1
    if dx == dy == 0:
        return distance(p1, center) <= radius
    t = ((cx - x1) * dx + (cy - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))
    closest = (x1 + t * dx, y1 + t * dy)
    return distance(closest, center) <= radius

# ------------------------------------------------------------
# Game states
# ------------------------------------------------------------
MENU, PLAYING, PAUSED, GAMEOVER = range(4)

# ------------------------------------------------------------
# Main loop
# ------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Light Painter Survival")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 48)

    state = MENU
    player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    enemies = []
    barriers = []
    last_spawn = 0
    start_time = 0
    last_barrier_time = 0
    barrier_cooldown = 300  # ms between barrier creations
    max_barriers = 3

    drawing = False
    draw_start = None
    running = True

    while running:
        dt = clock.tick(60)
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            if state == MENU:
                if event.type == pygame.KEYDOWN:
                    state = PLAYING
                    player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    enemies = []
                    barriers = []
                    last_spawn = now
                    start_time = now
                    last_barrier_time = now - barrier_cooldown
                    continue
            elif state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = PAUSED
                    elif event.key == pygame.K_SPACE:
                        drawing = True
                        draw_start = player.pos.copy()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE and drawing:
                        drawing = False
                        mouse_pos = pygame.mouse.get_pos()
                        if len(barriers) < max_barriers and now - last_barrier_time >= barrier_cooldown:
                            barriers.append(Barrier(tuple(draw_start), mouse_pos, now))
                            last_barrier_time = now
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        drawing = True
                        draw_start = player.pos.copy()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and drawing:
                        drawing = False
                        mouse_pos = pygame.mouse.get_pos()
                        if len(barriers) < max_barriers and now - last_barrier_time >= barrier_cooldown:
                            barriers.append(Barrier(tuple(draw_start), mouse_pos, now))
                            last_barrier_time = now
            elif state == PAUSED:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = PLAYING
            elif state == GAMEOVER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    state = MENU
        # -----------------------------------------------------
        # Game logic
        # -----------------------------------------------------
        if state == PLAYING:
            keys = pygame.key.get_pressed()
            player.handle_input(keys)
            # spawn enemies
            if now - last_spawn > SPAWN_INTERVAL:
                last_spawn = now
                side = random.choice(["top", "bottom", "left", "right"])
                if side == "top":
                    pos = (random.randint(0, SCREEN_WIDTH), -ENEMY_RADIUS)
                elif side == "bottom":
                    pos = (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + ENEMY_RADIUS)
                elif side == "left":
                    pos = (-ENEMY_RADIUS, random.randint(0, SCREEN_HEIGHT))
                else:
                    pos = (SCREEN_WIDTH + ENEMY_RADIUS, random.randint(0, SCREEN_HEIGHT))
                elapsed = now - start_time
                speed = ENEMY_SPEED + elapsed * DIFFICULTY_RAMP
                enemies.append(Enemy(pos, speed))
            for e in enemies:
                e.update(player.pos, barriers)
            barriers = [b for b in barriers if not b.is_dead(now)]
            # collision – player vs enemy
            for e in enemies:
                if distance(player.pos, e.pos) < player.radius + e.radius:
                    state = GAMEOVER
                    final_score = (now - start_time) // 1000
                    break
        # -----------------------------------------------------
        # Rendering
        # -----------------------------------------------------
        screen.fill(BG_COLOR)
        if state == MENU:
            title = big_font.render("Light Painter Survival", True, (200, 200, 200))
            instr1 = font.render("WASD to move, hold mouse or SPACE to draw barriers", True, (180, 180, 180))
            instr2 = font.render("Press any key to start", True, (180, 180, 180))
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//3))
            screen.blit(instr1, (SCREEN_WIDTH//2 - instr1.get_width()//2, SCREEN_HEIGHT//3 + 60))
            screen.blit(instr2, (SCREEN_WIDTH//2 - instr2.get_width()//2, SCREEN_HEIGHT//3 + 100))
        elif state == PLAYING:
            for b in barriers:
                b.draw(screen, now)
            player.draw(screen)
            for e in enemies:
                e.draw(screen)
            # HUD
            survived = (now - start_time) // 1000
            hud = font.render(f"Survived: {survived}s  Barriers: {len(barriers)}/{max_barriers}", True, (200, 200, 200))
            screen.blit(hud, (10, 10))
        elif state == PAUSED:
            pause = big_font.render("Paused", True, (255, 255, 0))
            screen.blit(pause, (SCREEN_WIDTH//2 - pause.get_width()//2, SCREEN_HEIGHT//2 - 30))
        elif state == GAMEOVER:
            over = big_font.render("Game Over", True, (255, 80, 80))
            score = font.render(f"Survived: {final_score}s", True, (200, 200, 200))
            restart = font.render("Press R to return to menu", True, (180, 180, 180))
            screen.blit(over, (SCREEN_WIDTH//2 - over.get_width()//2, SCREEN_HEIGHT//3))
            screen.blit(score, (SCREEN_WIDTH//2 - score.get_width()//2, SCREEN_HEIGHT//3 + 50))
            screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, SCREEN_HEIGHT//3 + 90))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
