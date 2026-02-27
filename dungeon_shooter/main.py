# Roguelike Dungeon Crawler Top‑Down Shooter (Pygame)
# ---------------------------------------------------
# This is a minimal prototype that demonstrates:
#   • Randomly generated dungeon layout (rooms + corridors)
#   • Player movement (WASD / Arrow keys)
#   • Shooting bullets in 8 directions (mouse aim)
#   • Simple enemy AI that chases the player
#   • Basic collision detection and health system
#
# It is intentionally lightweight – you can extend it with more rooms,
# items, monsters, graphics, sound, etc.
# ---------------------------------------------------

import pygame
import sys
import random
import math

# ---------- Configuration ----------
WIDTH, HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 40
MAP_WIDTH, MAP_HEIGHT = 20, 15  # in tiles (fits the window)
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 2
PLAYER_MAX_HP = 5
ENEMY_SPAWN_RATE = 120  # frames between spawns
# Upgradeable parameters
BEAM_LENGTH = 250
BEAM_ANGLE_DEG = 45  # cone width
BULLET_COOLDOWN_FRAMES = 10  # frames between shots (default 10)
MULTISHOT_COUNT = 1
# Money system
money = 0
# Shop costs
COST_FLASHLIGHT = 10
COST_FASTER_SHOOT = 15
COST_MULTISHOT = 20
# Shop state
shop_open = False
# -----------------------------------

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roguelike Dungeon Shooter")
clock = pygame.time.Clock()

# ---------- Helper Functions ----------
def world_to_screen(pos):
    """Convert world (tile) coordinates to pixel screen coordinates."""
    return pos[0] * TILE_SIZE, pos[1] * TILE_SIZE

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def cast_ray(start_x, start_y, angle, max_len, dungeon):
    """Step along a ray until hitting a wall or reaching max_len.
    Returns the endpoint (x, y)."""
    step = 5  # pixels per iteration
    x, y = start_x, start_y
    for _ in range(int(max_len / step)):
        x += step * math.cos(angle)
        y += step * math.sin(angle)
        # check bounds
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            break
        # check tile
        tile_x = int(x / TILE_SIZE)
        tile_y = int(y / TILE_SIZE)
        if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
            if dungeon[tile_x][tile_y] == 1:  # wall
                # step back a bit so we don't go inside wall
                x -= step * math.cos(angle)
                y -= step * math.sin(angle)
                break
    return x, y

# ---------- Dungeon Generation ----------
# Simple BSP‑style room placement

def generate_dungeon():
    grid = [[1 for _ in range(MAP_HEIGHT)] for _ in range(MAP_WIDTH)]  # 1 = wall, 0 = floor
    rooms = []
    max_rooms = 8
    min_size, max_size = 3, 6
    for _ in range(max_rooms):
        w = random.randint(min_size, max_size)
        h = random.randint(min_size, max_size)
        x = random.randint(1, MAP_WIDTH - w - 1)
        y = random.randint(1, MAP_HEIGHT - h - 1)
        new_room = pygame.Rect(x, y, w, h)
        # check overlap
        if any(new_room.colliderect(other) for other in rooms):
            continue
        # carve out floor
        for i in range(x, x + w):
            for j in range(y, y + h):
                grid[i][j] = 0
        # connect to previous room with a corridor
        if rooms:
            prev = rooms[-1]
            # center points
            cx1, cy1 = new_room.center
            cx2, cy2 = prev.center
            if random.choice([True, False]):
                # horizontal then vertical
                for i in range(min(cx1, cx2), max(cx1, cx2) + 1):
                    grid[i][cy1] = 0
                for j in range(min(cy1, cy2), max(cy1, cy2) + 1):
                    grid[cx2][j] = 0
            else:
                # vertical then horizontal
                for j in range(min(cy1, cy2), max(cy1, cy2) + 1):
                    grid[cx1][j] = 0
                for i in range(min(cx1, cx2), max(cx1, cx2) + 1):
                    grid[i][cy2] = 0
        rooms.append(new_room)
    return grid, rooms

# ---------- Entity Classes ----------
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, TILE_SIZE // 2, TILE_SIZE // 2)
        self.hp = PLAYER_MAX_HP

    def move(self, dx, dy, dungeon):
        new_x = self.x + dx
        new_y = self.y + dy
        # collision with walls (check tile under new position)
        tile_x = int(new_x / TILE_SIZE)
        tile_y = int(new_y / TILE_SIZE)
        if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
            if dungeon[tile_x][tile_y] == 0:
                self.x = new_x
                self.y = new_y
                self.rect.topleft = (self.x, self.y)

    def draw(self, surf):
        pygame.draw.rect(surf, (0, 200, 0), self.rect)

class Bullet:
    def __init__(self, x, y, dir_vec):
        self.x = x
        self.y = y
        self.dir = dir_vec
        self.rect = pygame.Rect(x, y, 6, 6)

    def update(self, dungeon):
        self.x += self.dir[0] * BULLET_SPEED
        self.y += self.dir[1] * BULLET_SPEED
        self.rect.topleft = (self.x, self.y)
        # stop if hits wall or out of bounds
        tile_x = int(self.x / TILE_SIZE)
        tile_y = int(self.y / TILE_SIZE)
        if not (0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT):
            return False
        if dungeon[tile_x][tile_y] == 1:
            return False
        return True

    def draw(self, surf):
        pygame.draw.rect(surf, (255, 255, 0), self.rect)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, TILE_SIZE // 2, TILE_SIZE // 2)
        self.hp = 1

    def update(self, player, dungeon):
        # simple chase
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            self.x += dx * ENEMY_SPEED
            self.y += dy * ENEMY_SPEED
            # wall collision – revert if moving into wall
            tile_x = int(self.x / TILE_SIZE)
            tile_y = int(self.y / TILE_SIZE)
            if not (0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT) or dungeon[tile_x][tile_y] == 1:
                self.x -= dx * ENEMY_SPEED
                self.y -= dy * ENEMY_SPEED
        self.rect.topleft = (self.x, self.y)

    def draw(self, surf):
        pygame.draw.rect(surf, (200, 0, 0), self.rect)

# ---------- Main Game Loop ----------
def title_screen():
    """Display a simple title screen to choose difficulty."""
    font_big = pygame.font.SysFont(None, 64)
    font_small = pygame.font.SysFont(None, 32)
    title_surf = font_big.render("Dungeon Shooter", True, (255, 255, 255))
    hard_surf = font_small.render("Hard", True, (200, 0, 0))
    normal_surf = font_small.render("Normal", True, (0, 200, 0))
    hard_rect = hard_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    normal_rect = normal_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if hard_rect.collidepoint(mx, my):
                    return "hard"
                if normal_rect.collidepoint(mx, my):
                    return "normal"
        screen.fill((0, 0, 0))
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        screen.blit(hard_surf, hard_rect)
        screen.blit(normal_surf, normal_rect)
        pygame.display.flip()
        clock.tick(FPS)

def main():
    global shop_open, money, BEAM_LENGTH, BULLET_COOLDOWN_FRAMES, MULTISHOT_COUNT, pending_shop_click
    difficulty = title_screen()
    # Set brightness based on difficulty
    if difficulty == "hard":
        DARKNESS_ALPHA = 255
        WALL_COLOR = (50, 50, 50)
        FLOOR_COLOR = (20, 20, 20)
    else:
        DARKNESS_ALPHA = 150
        WALL_COLOR = (70, 70, 70)
        FLOOR_COLOR = (40, 40, 40)
    dungeon, rooms = generate_dungeon()
    # spawn player in first room centre
    start_room = rooms[0]
    player = Player(start_room.centerx * TILE_SIZE, start_room.centery * TILE_SIZE)
    bullets = []
    enemies = []
    frame_counter = 0
    pending_shop_click = None  # store click position for shop processing
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    # toggle shop
                    shop_open = not shop_open
                    print(f"Shop {'opened' if shop_open else 'closed'}")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click – shoot or shop interaction
                    mx, my = event.pos
                    if shop_open:
                        # store click for processing after UI is drawn (rects are defined then)
                        pending_shop_click = (mx, my)
                    else:
                        # enforce bullet cooldown
                        if frame_counter - getattr(main, 'last_shot', -9999) < BULLET_COOLDOWN_FRAMES:
                            pass
                        else:
                            # direction vector from player centre to mouse
                            base_dir_x = mx - (player.x + player.rect.width / 2)
                            base_dir_y = my - (player.y + player.rect.height / 2)
                            base_len = math.hypot(base_dir_x, base_dir_y)
                            if base_len == 0:
                                continue
                            base_angle = math.atan2(base_dir_y, base_dir_x)
                            # fire MULTISHOT_COUNT bullets spread around base_angle
                            spread = math.radians(10)  # total spread angle
                            for i in range(MULTISHOT_COUNT):
                                angle_offset = (i - (MULTISHOT_COUNT - 1) / 2) * (spread / max(MULTISHOT_COUNT-1,1))
                                angle = base_angle + angle_offset
                                dir_vec = (math.cos(angle), math.sin(angle))
                                bullet = Bullet(player.x + player.rect.width / 2, player.y + player.rect.height / 2, dir_vec)
                                bullets.append(bullet)
                            main.last_shot = frame_counter

        # Input handling
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += PLAYER_SPEED
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += PLAYER_SPEED
        if dx != 0 or dy != 0:
            # normalize diagonal speed
            if dx != 0 and dy != 0:
                dx *= 0.7071
                dy *= 0.7071
            player.move(dx, dy, dungeon)

        # Update bullets
        bullets = [b for b in bullets if b.update(dungeon)]

        # Spawn enemies periodically
        if frame_counter % ENEMY_SPAWN_RATE == 0:
            # pick a random floor tile far from player
            while True:
                tx = random.randint(0, MAP_WIDTH - 1)
                ty = random.randint(0, MAP_HEIGHT - 1)
                if dungeon[tx][ty] == 0:
                    # distance check
                    px_tile = int(player.x / TILE_SIZE)
                    py_tile = int(player.y / TILE_SIZE)
                    if distance((tx, ty), (px_tile, py_tile)) > 6:
                        enemy = Enemy(tx * TILE_SIZE, ty * TILE_SIZE)
                        enemies.append(enemy)
                        break

        # Update enemies
        for enemy in enemies:
            enemy.update(player, dungeon)

        # Collision: bullets vs enemies
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    # reward player with money for a kill
                    money += 5
                    print(f"Killed enemy! Money now: {money}")
                    if bullet in bullets:
                        bullets.remove(bullet)
                    break

        # Collision: enemy vs player
        for enemy in enemies[:]:
            if enemy.rect.colliderect(player.rect):
                player.hp -= 1
                enemies.remove(enemy)
                if player.hp <= 0:
                    print("Game Over!")
                    pygame.quit()
                    sys.exit()

        # Rendering
        screen.fill((30, 30, 30))
        # draw dungeon floor/walls using difficulty colors
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if dungeon[x][y] == 1:
                    pygame.draw.rect(screen, WALL_COLOR, rect)
                else:
                    pygame.draw.rect(screen, FLOOR_COLOR, rect)
        # draw entities (player, bullets, and enemies)
        player.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        # HUD – health and money
        font = pygame.font.SysFont(None, 24)
        hp_surf = font.render(f"HP: {player.hp}", True, (255, 255, 255))
        screen.blit(hp_surf, (10, 10))
        money_surf = font.render(f"$ {money}", True, (255, 215, 0))
        screen.blit(money_surf, (10, 30))

        # Flashlight beam effect: dark overlay with transparent cone from player to mouse, player always visible, beam stops at walls
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Create a full‑screen dark overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, DARKNESS_ALPHA))  # darkness based on difficulty
        # Compute angle from player centre to mouse
        player_center_x = player.x + player.rect.width / 2
        player_center_y = player.y + player.rect.height / 2
        angle = math.atan2(mouse_y - player_center_y, mouse_x - player_center_x)
        half_angle = math.radians(BEAM_ANGLE_DEG / 2)
        # Offset the cone start a bit behind the player so the player is always lit
        OFFSET = 15
        start_x = player_center_x - OFFSET * math.cos(angle)
        start_y = player_center_y - OFFSET * math.sin(angle)
        # Cast rays to the edges of the cone, stopping at walls
        tip1_x, tip1_y = cast_ray(start_x, start_y, angle - half_angle, BEAM_LENGTH, dungeon)
        tip2_x, tip2_y = cast_ray(start_x, start_y, angle + half_angle, BEAM_LENGTH, dungeon)
        # Polygon points: start point, tip1, tip2
        cone_points = [(start_x, start_y), (tip1_x, tip1_y), (tip2_x, tip2_y)]
        pygame.draw.polygon(overlay, (0, 0, 0, 0), cone_points)
        pygame.draw.circle(overlay, (0, 0, 0, 0), (int(player_center_x), int(player_center_y)), 20)
        screen.blit(overlay, (0, 0))

        # Shop UI overlay
        if shop_open:
            shop_surf = pygame.Surface((300, 200), pygame.SRCALPHA)
            shop_surf.fill((30, 30, 30, 220))
            shop_rect = shop_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(shop_surf, shop_rect)
            opt_font = pygame.font.SysFont(None, 28)
            bf_text = opt_font.render(f"Bigger Flashlight (${COST_FLASHLIGHT})", True, (255, 255, 255))
            bf_rect = bf_text.get_rect(topleft=(shop_rect.left + 20, shop_rect.top + 30))
            screen.blit(bf_text, bf_rect)
            fs_text = opt_font.render(f"Faster Shooting (${COST_FASTER_SHOOT})", True, (255, 255, 255))
            fs_rect = fs_text.get_rect(topleft=(shop_rect.left + 20, shop_rect.top + 70))
            screen.blit(fs_text, fs_rect)
            ms_text = opt_font.render(f"Multishot (${COST_MULTISHOT})", True, (255, 255, 255))
            ms_rect = ms_text.get_rect(topleft=(shop_rect.left + 20, shop_rect.top + 110))
            screen.blit(ms_text, ms_rect)
            # store rects globally for click handling
            global SHOP_BF_RECT, SHOP_FS_RECT, SHOP_MS_RECT
            SHOP_BF_RECT, SHOP_FS_RECT, SHOP_MS_RECT = bf_rect, fs_rect, ms_rect

            # Process pending shop click if any
            if pending_shop_click:
                mx, my = pending_shop_click
                if SHOP_BF_RECT.collidepoint(mx, my) and money >= COST_FLASHLIGHT:
                    BEAM_LENGTH += 100  # make a noticeable increase
                    money -= COST_FLASHLIGHT
                    print(f"Bought Bigger Flashlight. New length: {BEAM_LENGTH}, money left: {money}")
                    shop_open = False
                elif SHOP_FS_RECT.collidepoint(mx, my) and money >= COST_FASTER_SHOOT:
                    BULLET_COOLDOWN_FRAMES = max(0, BULLET_COOLDOWN_FRAMES - 5)
                    money -= COST_FASTER_SHOOT
                    print(f"Bought Faster Shooting. New cooldown: {BULLET_COOLDOWN_FRAMES}, money left: {money}")
                    shop_open = False
                elif SHOP_MS_RECT.collidepoint(mx, my) and money >= COST_MULTISHOT:
                    MULTISHOT_COUNT += 1
                    money -= COST_MULTISHOT
                    print(f"Bought Multishot. New count: {MULTISHOT_COUNT}, money left: {money}")
                    shop_open = False
                pending_shop_click = None

        pygame.display.flip()
        clock.tick(FPS)
        frame_counter += 1

if __name__ == "__main__":
    main()
