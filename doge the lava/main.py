import pygame
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge The Blocks")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 200, 255)
BLOCK_COLOR = (200, 0, 0)
SPIKE_COLOR = (255, 80, 0)
DASH_TRAIL_COLOR = (0, 120, 200)
GRAY = (80, 80, 80)
WALL_COLOR = (40, 40, 40)

# Wall and spike setup
WALL_THICKNESS = 20
SPIKE_W = 60  # collision zone width for spikes
SPIKE_H = HEIGHT

# Player
player_size = 40
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 7
facing = 0  # -1 left, 1 right, 0 none

# Dash
DASH_DISTANCE = 160
DASH_SPEED = 30
dashing = False
dash_target_x = 0
dash_direction = 0
dash_cooldown = 0
DASH_COOLDOWN_MAX = 30  # frames (~0.5s at 60fps)
dash_trails = []  # list of (x, y, alpha)

# Blocks
block_size = 50
block_speed = 5
blocks = []

# Spikes (collapsed to walls later)
spikes_active = False
spike_left_rect = pygame.Rect(0, 0, SPIKE_W, HEIGHT)
spike_right_rect = pygame.Rect(WIDTH - SPIKE_W, 0, SPIKE_W, HEIGHT)

font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)
score = 0
game_over = False
rotating = False
rotation_angle = 0


def reset_game():
    global blocks, score, game_over, player_x, spikes_active, dashing, dash_cooldown, facing, dash_trails, block_speed, rotating
    blocks = []
    score = 0
    game_over = False
    spikes_active = False
    dashing = False
    dash_cooldown = 0
    facing = 0
    dash_trails = []
    block_speed = 5
    player_x = WIDTH // 2 - player_size // 2
    rotating = False
    rotation_angle = 0
    spawn_blocks(6)

def left_bound():
    base = WALL_THICKNESS
    if spikes_active:
        base += SPIKE_W
    return base

def right_bound():
    base = WIDTH - WALL_THICKNESS - player_size
    if spikes_active:
        base -= SPIKE_W
    return base

def spawn_blocks(count):
    for _ in range(count):
        x = random.randint(left_bound(), right_bound())
        y = random.randint(-HEIGHT, -block_size)
        blocks.append([x, y])


def draw_spike_zones(surface):
    if not spikes_active:
        return
    pygame.draw.rect(surface, SPIKE_COLOR, spike_left_rect)
    pygame.draw.rect(surface, SPIKE_COLOR, spike_right_rect)

# Init
reset_game()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
            if event.key == pygame.K_SPACE and not game_over and not dashing and dash_cooldown == 0:
                if facing != 0:
                    dashing = True
                    dash_direction = facing
                    dash_target_x = player_x + DASH_DISTANCE * dash_direction
                    dash_target_x = max(left_bound(), min(right_bound(), dash_target_x))

    keys = pygame.key.get_pressed()
    if not game_over:
        # Movement
        if not dashing:
            moved = False
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_x -= player_speed
                facing = -1
                moved = True
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_x += player_speed
                facing = 1
                moved = True
            if not moved:
                pass
        else:
            # Dash trail for feedback
            dash_trails.append([player_x + player_size // 2, player_y + player_size // 2, 200])
            diff = dash_target_x - player_x
            if abs(diff) < DASH_SPEED:
                player_x = dash_target_x
                dashing = False
                dash_cooldown = DASH_COOLDOWN_MAX
            else:
                player_x += DASH_SPEED * dash_direction

        player_x = max(left_bound(), min(right_bound(), player_x))
        if dash_cooldown > 0:
            dash_cooldown -= 1

        # Difficulty scaling: blocks accelerate, spikes appear later
        if score >= 50 and not spikes_active:
            spikes_active = True
            # Extend spike collision area to full height on activation
            spike_left_rect = pygame.Rect(WALL_THICKNESS, 0, SPIKE_W, HEIGHT)
            spike_right_rect = pygame.Rect(WIDTH - WALL_THICKNESS - SPIKE_W, 0, SPIKE_W, HEIGHT)
            # keep bounds consistent
        block_speed = 5 + score * 0.04
        if score >= 128 and not rotating:
            rotating = True
            rotation_angle = 0
        # Rotation is active from 128 to 160
        if rotating and score >= 128 and score < 160:
            rotation_angle += 2
        elif rotating and score >= 160:
            rotating = False
            rotation_angle = 0

        # Move blocks
        for b in blocks:
            b[1] += block_speed
            if b[1] > HEIGHT:
                lb = left_bound() + 5
                rb = right_bound() - block_size - 5
                b[0] = random.randint(int(lb), int(rb))
                b[1] = random.randint(-300, -block_size)
                score += 1

        # Collision with blocks
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for b in blocks:
            block_rect = pygame.Rect(b[0], b[1], block_size, block_size)
            if player_rect.colliderect(block_rect):
                game_over = True
                break

        # Collision with spikes
        if spikes_active and not game_over:
            if player_rect.colliderect(spike_left_rect) or player_rect.colliderect(spike_right_rect):
                game_over = True

        # Update dash trails
        new_trails = []
        for t in dash_trails:
            t[2] -= 12
            if t[2] > 0:
                new_trails.append(t)
        dash_trails = new_trails

    # DRAWING
    # Offscreen surface for rotation when needed
    game_surface = pygame.Surface((WIDTH, HEIGHT))
    game_surface.fill(BLACK)

    # Walls
    pygame.draw.rect(game_surface, WALL_COLOR, (0, 0, WALL_THICKNESS, HEIGHT))
    pygame.draw.rect(game_surface, WALL_COLOR, (WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, HEIGHT))

    # Spikes zones on walls
    draw_spike_zones(game_surface)

    # Blocks
    for b in blocks:
        pygame.draw.rect(game_surface, BLOCK_COLOR, (b[0], b[1], block_size, block_size))
        pygame.draw.rect(game_surface, WHITE, (b[0], b[1], block_size, block_size), 1)

    # Dash trails
    for t in dash_trails:
        alpha = max(0, t[2])
        s = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
        s.fill((DASH_TRAIL_COLOR[0], DASH_TRAIL_COLOR[1], DASH_TRAIL_COLOR[2], alpha))
        game_surface.blit(s, (t[0] - player_size // 2, t[1] - player_size // 2))

    # Player
    color = PLAYER_COLOR if not dashing else (100, 255, 255)
    pygame.draw.rect(game_surface, color, (player_x, player_y, player_size, player_size))
    pygame.draw.rect(game_surface, WHITE, (player_x, player_y, player_size, player_size), 2)

    # HUD overlays on a separate layer (not rotated with game_surface unless rotating)
    score_text = font.render(f"Score: {score}", True, WHITE)
    game_surface.blit(score_text, (10, 10))
    if dash_cooldown > 0:
        cd_pct = dash_cooldown / DASH_COOLDOWN_MAX
        bar_w = 80
        pygame.draw.rect(game_surface, GRAY, (WIDTH - bar_w - 20, 12, bar_w, 14))
        pygame.draw.rect(game_surface, DASH_TRAIL_COLOR, (WIDTH - bar_w - 20, 12, int(bar_w * (1 - cd_pct)), 14))
        cd_label = small_font.render("DASH", True, WHITE)
        game_surface.blit(cd_label, (WIDTH - bar_w - 60, 10))
    else:
        cd_label = small_font.render("DASH READY", True, (0, 255, 120))
        game_surface.blit(cd_label, (WIDTH - 130, 10))
    if rotating and score >= 128 and score < 160:
        rot_label = small_font.render("ROTATING WALLS", True, (200, 200, 0))
        game_surface.blit(rot_label, (WIDTH // 2 - rot_label.get_width() // 2, 10))

    # Render to screen with rotation if active
    if rotating and score >= 128 and score < 160:
        # rotate around center, keep movement responsive by not halting input
        rotation_angle = min(360, rotation_angle)
        rotated = pygame.transform.rotate(game_surface, rotation_angle)
        rect = rotated.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.fill(BLACK)
        screen.blit(rotated, rect.topleft)
        # Note: during rotation we don't draw the separate HUD again; HUD is baked into game_surface
    else:
        screen.blit(game_surface, (0, 0))

    # Overlays for game state
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        go_text = font.render(f"Game Over!  Score: {score}", True, WHITE)
        screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 20))
        restart_text = small_font.render("Press R to restart", True, (180, 180, 180))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()
    clock.tick(60)
