import math
import sys
from dataclasses import dataclass, field

import pygame

# ---------------------------------------------------------------------------
# Global constants
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 960, 540
FPS = 60

COLORS = {
    "bg": (20, 20, 28),
    "wall": (120, 120, 130),
    "player": (50, 150, 255),
    "guard": (230, 60, 60),
    "guard_alert": (255, 40, 40),
    "camera": (245, 220, 70),
    "item": (40, 220, 90),
    "exit": (120, 220, 255),
    "text": (235, 235, 240),
    "pellet": (255, 140, 0),
    "spotted_text": (255, 60, 60),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def vec_from_angle(angle_rad: float) -> pygame.Vector2:
    return pygame.Vector2(math.cos(angle_rad), math.sin(angle_rad))


def line_blocked_by_walls(p1: pygame.Vector2, p2: pygame.Vector2, walls: list[pygame.Rect]) -> bool:
    for w in walls:
        if w.clipline((p1.x, p1.y), (p2.x, p2.y)):
            return True
    return False


def angle_between(a: pygame.Vector2, b: pygame.Vector2) -> float:
    if a.length_squared() == 0 or b.length_squared() == 0:
        return math.pi
    return math.acos(clamp(a.normalize().dot(b.normalize()), -1.0, 1.0))


def draw_vision_cone(surface, origin, angle, fov, dist, color):
    """Draw a filled vision cone on an alpha surface."""
    points = [origin]
    steps = 20
    start = angle - fov / 2
    for i in range(steps + 1):
        a = start + fov * i / steps
        points.append(origin + vec_from_angle(a) * dist)
    if len(points) >= 3:
        pygame.draw.polygon(surface, color, [(int(p.x), int(p.y)) for p in points])


def move_with_wall_collision(pos: pygame.Vector2, size: int, move: pygame.Vector2, walls: list[pygame.Rect]) -> pygame.Vector2:
    """Move a square entity by *move* while sliding along walls.
    Returns the new top-left position."""
    rect = pygame.Rect(int(pos.x), int(pos.y), size, size)

    # X step
    rect.x += int(round(move.x))
    for w in walls:
        if rect.colliderect(w):
            if move.x > 0:
                rect.right = w.left
            elif move.x < 0:
                rect.left = w.right

    # Y step
    rect.y += int(round(move.y))
    for w in walls:
        if rect.colliderect(w):
            if move.y > 0:
                rect.bottom = w.top
            elif move.y < 0:
                rect.top = w.bottom

    # Keep inside screen
    rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
    return pygame.Vector2(rect.x, rect.y)


# ---------------------------------------------------------------------------
# Game Objects
# ---------------------------------------------------------------------------


class Player:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, 22, 22)
        self.speed = 210  # px/s
        self.alive = True

    def update(self, dt: float, walls: list[pygame.Rect], keys) -> bool:
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        moving = dx != 0 or dy != 0
        if not moving:
            return False
        vel = pygame.Vector2(dx, dy)
        if vel.length_squared() > 0:
            vel = vel.normalize() * self.speed * dt
        self.rect.x += int(round(vel.x))
        for w in walls:
            if self.rect.colliderect(w):
                if vel.x > 0:
                    self.rect.right = w.left
                elif vel.x < 0:
                    self.rect.left = w.right
        self.rect.y += int(round(vel.y))
        for w in walls:
            if self.rect.colliderect(w):
                if vel.y > 0:
                    self.rect.bottom = w.top
                elif vel.y < 0:
                    self.rect.top = w.bottom
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
        return True

    @property
    def center(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.center)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, COLORS["player"], self.rect)


class Projectile:
    def __init__(self, pos, direction, speed: float = 420.0, radius: int = 5):
        self.pos = pygame.Vector2(pos)
        self.vel = direction.normalize() * speed if direction.length() > 0 else pygame.Vector2(0, 0)
        self.radius = radius
        self.alive = True

    @property
    def rect(self):
        return pygame.Rect(
            int(self.pos.x - self.radius),
            int(self.pos.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def update(self, dt: float, walls: list[pygame.Rect]):
        self.pos += self.vel * dt
        # Die on wall hit
        for w in walls:
            if self.rect.colliderect(w):
                self.alive = False
                return
        # Die off-screen
        if not (0 <= self.pos.x <= WIDTH and 0 <= self.pos.y <= HEIGHT):
            self.alive = False

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, COLORS["pellet"], (int(self.pos.x), int(self.pos.y)), self.radius)


class Guard:
    """A guard that patrols waypoints, never walks through walls,
    and when the alert is raised chases + shoots the player."""

    def __init__(self, patrol_points: list[tuple[int, int]]):
        self.patrol = [pygame.Vector2(p) for p in patrol_points]
        self.pos = pygame.Vector2(self.patrol[0])
        self.size = 20
        self.speed_patrol = 100
        self.speed_chase = 160
        self.target_i = 1 if len(self.patrol) > 1 else 0
        self.fov = math.radians(70)
        self.vision_dist = 230
        self.facing = pygame.Vector2(1, 0)
        self.shoot_cooldown = 0.0
        self.shoot_interval = 0.55  # seconds between shots

    @property
    def rect(self) -> pygame.Rect:
        hs = self.size // 2
        return pygame.Rect(int(self.pos.x - hs), int(self.pos.y - hs), self.size, self.size)

    # ------ vision ------
    def sees_player(self, player: Player, walls: list[pygame.Rect]) -> bool:
        origin = pygame.Vector2(self.rect.center)
        to_p = player.center - origin
        if to_p.length() > self.vision_dist:
            return False
        if angle_between(self.facing, to_p) > self.fov / 2:
            return False
        if line_blocked_by_walls(origin, player.center, walls):
            return False
        return True

    def has_line_of_sight(self, player: Player, walls: list[pygame.Rect]) -> bool:
        """Can this guard see the player regardless of FOV cone?
        Used for shooting once alerted (guards turn to face player)."""
        origin = pygame.Vector2(self.rect.center)
        to_p = player.center - origin
        if to_p.length() > self.vision_dist * 1.5:  # slightly longer range when alerted
            return False
        if line_blocked_by_walls(origin, player.center, walls):
            return False
        return True

    # ------ movement ------
    def _patrol_move(self, dt: float, time_scale: float, walls: list[pygame.Rect]):
        """Follow waypoints, respecting walls."""
        if len(self.patrol) < 2:
            return
        target = self.patrol[self.target_i]
        to_target = target - self.pos
        if to_target.length() < 6:
            self.target_i = (self.target_i + 1) % len(self.patrol)
            target = self.patrol[self.target_i]
            to_target = target - self.pos
        if to_target.length_squared() == 0:
            return
        direction = to_target.normalize()
        move = direction * self.speed_patrol * dt * max(0.0, time_scale)
        new_pos = move_with_wall_collision(
            pygame.Vector2(self.rect.topleft), self.size, move, walls
        )
        self.pos = pygame.Vector2(new_pos.x + self.size / 2, new_pos.y + self.size / 2)
        self.facing = direction

    def _chase_move(self, dt: float, player: Player, walls: list[pygame.Rect]):
        """Move toward the player, never through walls."""
        to_player = player.center - self.pos
        if to_player.length_squared() == 0:
            return
        direction = to_player.normalize()
        move = direction * self.speed_chase * dt
        new_pos = move_with_wall_collision(
            pygame.Vector2(self.rect.topleft), self.size, move, walls
        )
        self.pos = pygame.Vector2(new_pos.x + self.size / 2, new_pos.y + self.size / 2)
        self.facing = direction

    # ------ main update ------
    def update(
        self,
        dt: float,
        time_scale: float,
        player: Player,
        walls: list[pygame.Rect],
        projectiles: list,
        spotted: bool,
    ):
        self.shoot_cooldown = max(0.0, self.shoot_cooldown - dt)

        if spotted:
            # Chase the player
            self._chase_move(dt, player, walls)
            # Shoot if line-of-sight (wall check, no FOV restriction when alerted)
            if self.has_line_of_sight(player, walls) and self.shoot_cooldown <= 0.0:
                dir_to = player.center - pygame.Vector2(self.rect.center)
                if dir_to.length() > 0:
                    projectiles.append(Projectile(self.rect.center, dir_to))
                    self.shoot_cooldown = self.shoot_interval
        else:
            # Normal patrol (time-scaled)
            self._patrol_move(dt, time_scale, walls)

    # ------ drawing ------
    def draw(self, screen: pygame.Surface, spotted: bool):
        color = COLORS["guard_alert"] if spotted else COLORS["guard"]
        pygame.draw.rect(screen, color, self.rect)
        # Small direction indicator
        tip = self.pos + self.facing * (self.size * 0.7)
        pygame.draw.line(screen, (255, 200, 200), (int(self.pos.x), int(self.pos.y)), (int(tip.x), int(tip.y)), 2)

    def draw_cone(self, cone_surface: pygame.Surface, spotted: bool):
        origin = pygame.Vector2(self.rect.center)
        ang = math.atan2(self.facing.y, self.facing.x)
        if spotted:
            # Wider awareness when alerted
            draw_vision_cone(cone_surface, origin, ang, math.radians(120), int(self.vision_dist * 1.2), (255, 50, 50, 40))
        else:
            draw_vision_cone(cone_surface, origin, ang, self.fov, self.vision_dist, (255, 70, 70, 50))


class Camera:
    def __init__(self, x: int, y: int, min_angle_deg: float, max_angle_deg: float):
        self.pos = pygame.Vector2(x, y)
        self.size = 16
        self.min_ang = math.radians(min_angle_deg)
        self.max_ang = math.radians(max_angle_deg)
        self.angle = (self.min_ang + self.max_ang) / 2
        self.rot_dir = 1
        self.rot_speed = math.radians(45)
        self.fov = math.radians(50)
        self.vision_dist = 260

    @property
    def rect(self) -> pygame.Rect:
        hs = self.size // 2
        return pygame.Rect(int(self.pos.x - hs), int(self.pos.y - hs), self.size, self.size)

    def update(self, dt: float, time_scale: float):
        self.angle += self.rot_speed * dt * self.rot_dir * time_scale
        if self.angle < self.min_ang:
            self.angle = self.min_ang
            self.rot_dir *= -1
        if self.angle > self.max_ang:
            self.angle = self.max_ang
            self.rot_dir *= -1

    def sees_player(self, player: Player, walls: list[pygame.Rect]) -> bool:
        origin = pygame.Vector2(self.rect.center)
        to_p = player.center - origin
        if to_p.length() > self.vision_dist:
            return False
        facing = vec_from_angle(self.angle)
        if angle_between(facing, to_p) > self.fov / 2:
            return False
        if line_blocked_by_walls(origin, player.center, walls):
            return False
        return True

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, COLORS["camera"], self.rect)
        tip = pygame.Vector2(self.rect.center) + vec_from_angle(self.angle) * 14
        pygame.draw.line(screen, (255, 250, 200), self.rect.center, (int(tip.x), int(tip.y)), 2)

    def draw_cone(self, cone_surface: pygame.Surface):
        origin = pygame.Vector2(self.rect.center)
        draw_vision_cone(cone_surface, origin, self.angle, self.fov, self.vision_dist, (255, 235, 90, 50))


@dataclass
class Item:
    pos: pygame.Vector2
    radius: int = 8
    collected: bool = False

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            int(self.pos.x - self.radius),
            int(self.pos.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def draw(self, screen: pygame.Surface):
        if self.collected:
            return
        pygame.draw.circle(screen, COLORS["item"], (int(self.pos.x), int(self.pos.y)), self.radius)


# ---------------------------------------------------------------------------
# Level builder — patrol paths are carefully set to stay between walls
# ---------------------------------------------------------------------------

def build_level():
    walls = [
        # Outer boundary
        pygame.Rect(0, 0, WIDTH, 18),       # top
        pygame.Rect(0, HEIGHT - 18, WIDTH, 18),  # bottom
        pygame.Rect(0, 0, 18, HEIGHT),       # left
        pygame.Rect(WIDTH - 18, 0, 18, HEIGHT),  # right
        # Interior walls
        pygame.Rect(120, 90, 18, 360),       # wall A (vertical)
        pygame.Rect(260, 90, 18, 260),       # wall B (vertical)
        pygame.Rect(260, 350, 250, 18),      # wall C (horizontal)
        pygame.Rect(430, 140, 18, 120),      # wall D (vertical, short)
        pygame.Rect(520, 90, 18, 280),       # wall E (vertical)
        pygame.Rect(650, 180, 18, 270),      # wall F (vertical)
        pygame.Rect(740, 90, 18, 250),       # wall G (vertical)
        pygame.Rect(740, 340, 140, 18),      # wall H (horizontal)
    ]

    player = Player(60, 60)

    # Guard 1: patrols in the corridor between wall A (x=138) and wall B (x=260)
    # Stays in the open area: x around 190, y from 110 down to 330
    guards = [
        Guard([
            (190, 110),   # top of corridor
            (190, 330),   # bottom of corridor
        ]),
        # Guard 2: patrols in the room between wall E (x=538) and wall F (x=650)
        # y from 110 to 160 (above wall C which is at y=350, but wall E ends at y=370)
        Guard([
            (590, 110),   # top
            (590, 160),   # near wall D bottom
            (630, 160),   # shift right
            (630, 110),   # back up
        ]),
        # Guard 3: patrols lower-right area between wall F (x=668) and wall G (x=740)
        # Actually give this one a wider patrol in the open space right of wall G
        Guard([
            (800, 110),   # top-right room
            (900, 110),
            (900, 320),
            (800, 320),
        ]),
    ]

    cameras = [
        Camera(310, 430, -110, -20),
        Camera(860, 120, 130, 220),
    ]

    items = [
        Item(pygame.Vector2(90, 480)),
        Item(pygame.Vector2(470, 110)),
        Item(pygame.Vector2(610, 430)),
        Item(pygame.Vector2(890, 480)),
    ]

    exit_zone = pygame.Rect(900, 30, 42, 42)
    return player, walls, guards, cameras, items, exit_zone


# ---------------------------------------------------------------------------
# Main game loop
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Time Slow Heist")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 28)
    big = pygame.font.SysFont(None, 56)
    spotted_font = pygame.font.SysFont(None, 40)

    player, walls, guards, cameras, items, exit_zone = build_level()
    projectiles: list[Projectile] = []
    spotted = False
    spotted_flash_timer = 0.0  # for flashing "SPOTTED!" text
    state = "play"  # play | lose | win

    while True:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        # Restart
        if state != "play":
            if keys[pygame.K_r]:
                player, walls, guards, cameras, items, exit_zone = build_level()
                projectiles.clear()
                spotted = False
                spotted_flash_timer = 0.0
                state = "play"

        if state == "play":
            # --- Player movement ---
            player_moving = player.update(dt, walls, keys)
            time_scale = 1.0 if player_moving else 0.0

            # --- Item collection ---
            for it in items:
                if not it.collected and player.rect.colliderect(it.rect):
                    it.collected = True

            # --- Detection: guards or cameras spot you → alert (not instant death) ---
            if not spotted:
                for g in guards:
                    if g.sees_player(player, walls):
                        spotted = True
                        spotted_flash_timer = 2.0  # flash for 2 seconds
                        break
                if not spotted:
                    for c in cameras:
                        if c.sees_player(player, walls):
                            spotted = True
                            spotted_flash_timer = 2.0
                            break

            # --- Update guards ---
            # When spotted, guards run at full speed regardless of time_scale
            for g in guards:
                g.update(dt, time_scale, player, walls, projectiles, spotted)

            # --- Update cameras (still time-scaled) ---
            for c in cameras:
                c.update(dt, time_scale)

            # --- Update projectiles ---
            for p in projectiles:
                p.update(dt, walls)
            projectiles = [p for p in projectiles if p.alive]

            # --- Check if player is hit by a pellet → die ---
            for p in projectiles:
                if p.rect.colliderect(player.rect):
                    state = "lose"
                    break

            # --- Win condition ---
            all_collected = all(it.collected for it in items)
            if state == "play" and all_collected and player.rect.colliderect(exit_zone):
                state = "win"

            # --- Spotted flash timer ---
            if spotted_flash_timer > 0:
                spotted_flash_timer = max(0.0, spotted_flash_timer - dt)

        # ===================================================================
        # DRAW
        # ===================================================================
        screen.fill(COLORS["bg"])

        # Vision cones (alpha overlay)
        cone = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for g in guards:
            g.draw_cone(cone, spotted)
        for c in cameras:
            c.draw_cone(cone)
        screen.blit(cone, (0, 0))

        # Walls
        for w in walls:
            pygame.draw.rect(screen, COLORS["wall"], w)

        # Exit zone
        pygame.draw.rect(screen, COLORS["exit"], exit_zone)
        exit_label = font.render("EXIT", True, (20, 20, 28))
        screen.blit(exit_label, (exit_zone.x + 4, exit_zone.y + 12))

        # Items
        for it in items:
            it.draw(screen)

        # Projectiles
        for p in projectiles:
            p.draw(screen)

        # Guards
        for g in guards:
            g.draw(screen, spotted)

        # Cameras
        for c in cameras:
            c.draw(screen)

        # Player
        player.draw(screen)

        # --- HUD ---
        remaining = sum(1 for it in items if not it.collected)
        hud_text = f"Items left: {remaining}"
        hud = font.render(hud_text, True, COLORS["text"])
        screen.blit(hud, (18, HEIGHT - 30))

        # "SPOTTED!" indicator top-left when alert is active
        if spotted:
            # Flash effect for first 2 seconds, then solid
            if spotted_flash_timer > 0:
                show = int(spotted_flash_timer * 6) % 2 == 0  # blink
            else:
                show = True
            if show:
                spotted_surf = spotted_font.render("⚠ SPOTTED!", True, COLORS["spotted_text"])
                screen.blit(spotted_surf, (18, 22))

        # --- End screens ---
        if state == "lose":
            # Dim overlay
            dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            dim.fill((0, 0, 0, 120))
            screen.blit(dim, (0, 0))
            msg = big.render("CAUGHT!", True, (255, 120, 120))
            sub = font.render("Press R to restart", True, COLORS["text"])
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 60))
            screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2))

        if state == "win":
            dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            dim.fill((0, 0, 0, 120))
            screen.blit(dim, (0, 0))
            msg = big.render("ESCAPED!", True, (120, 255, 190))
            sub = font.render("Press R to play again", True, COLORS["text"])
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 60))
            screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()


if __name__ == "__main__":
    main()
