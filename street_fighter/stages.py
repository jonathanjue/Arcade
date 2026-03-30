"""
stages.py - Pre-rendered 2D fighting game stage backgrounds.

Each stage provides:
  - prerender(surface_width, surface_height) -> pygame.Surface
  - get_ground_y() -> int (520)

Static elements are drawn once during prerender using seeded random.
Only animated particles (returned separately) change per frame.
"""

import pygame
import random
import math

GROUND_Y = 520


def get_ground_y():
    return GROUND_Y


# ---------------------------------------------------------------------------
# Dojo
# ---------------------------------------------------------------------------

class DojoStage:
    """Wooden floor, paper walls, moonlight through window."""

    def __init__(self):
        self._seed = 42
        self._surface = None

    def get_ground_y(self):
        return GROUND_Y

    def prerender(self, width, height):
        rng = random.Random(self._seed)
        surf = pygame.Surface((width, height))

        # --- Background: dark room ---
        surf.fill((45, 35, 25))

        # --- Paper walls (shoji screens) ---
        wall_color = (210, 195, 170)
        wall_dark = (180, 165, 140)
        panel_w = 90
        panel_h = 320
        panel_top = 60

        # Left wall panels
        for i in range(4):
            x = 10 + i * (panel_w + 8)
            y = panel_top
            pygame.draw.rect(surf, wall_color, (x, y, panel_w, panel_h))
            # Cross bars
            pygame.draw.line(surf, wall_dark, (x, y + panel_h // 3), (x + panel_w, y + panel_h // 3), 2)
            pygame.draw.line(surf, wall_dark, (x, y + 2 * panel_h // 3), (x + panel_w, y + 2 * panel_h // 3), 2)
            pygame.draw.line(surf, wall_dark, (x + panel_w // 2, y), (x + panel_w // 2, y + panel_h), 2)
            # Subtle paper texture noise
            for _ in range(30):
                nx = rng.randint(x + 2, x + panel_w - 2)
                ny = rng.randint(y + 2, y + panel_h - 2)
                c = rng.randint(195, 220)
                surf.set_at((nx, ny), (c, c - 10, c - 20))

        # Right wall panels
        for i in range(4):
            x = width - 10 - (i + 1) * panel_w - i * 8
            y = panel_top
            pygame.draw.rect(surf, wall_color, (x, y, panel_w, panel_h))
            pygame.draw.line(surf, wall_dark, (x, y + panel_h // 3), (x + panel_w, y + panel_h // 3), 2)
            pygame.draw.line(surf, wall_dark, (x, y + 2 * panel_h // 3), (x + panel_w, y + 2 * panel_h // 3), 2)
            pygame.draw.line(surf, wall_dark, (x + panel_w // 2, y), (x + panel_w // 2, y + panel_h), 2)
            for _ in range(30):
                nx = rng.randint(x + 2, x + panel_w - 2)
                ny = rng.randint(y + 2, y + panel_h - 2)
                c = rng.randint(195, 220)
                surf.set_at((nx, ny), (c, c - 10, c - 20))

        # --- Center back wall with window (moonlight source) ---
        back_wall = pygame.Rect(width // 2 - 160, 40, 320, 340)
        pygame.draw.rect(surf, (60, 50, 40), back_wall)
        pygame.draw.rect(surf, (80, 65, 50), back_wall, 3)

        # Window
        win_rect = pygame.Rect(width // 2 - 60, 80, 120, 180)
        # Night sky in window
        pygame.draw.rect(surf, (15, 15, 40), win_rect)
        # Moon
        moon_cx = width // 2 + 10
        moon_cy = 140
        pygame.draw.circle(surf, (230, 230, 210), (moon_cx, moon_cy), 28)
        pygame.draw.circle(surf, (210, 210, 195), (moon_cx - 5, moon_cy - 5), 22)
        # A few stars
        for _ in range(8):
            sx = rng.randint(win_rect.left + 5, win_rect.right - 5)
            sy = rng.randint(win_rect.top + 5, win_rect.bottom - 5)
            brightness = rng.randint(180, 255)
            surf.set_at((sx, sy), (brightness, brightness, brightness))
        # Window frame cross
        pygame.draw.line(surf, (80, 65, 50), (win_rect.centerx, win_rect.top), (win_rect.centerx, win_rect.bottom), 3)
        pygame.draw.line(surf, (80, 65, 50), (win_rect.left, win_rect.centery), (win_rect.right, win_rect.centery), 3)
        # Window border
        pygame.draw.rect(surf, (90, 75, 55), win_rect, 4)

        # Moonlight beam on floor
        beam_pts = [
            (win_rect.left - 20, GROUND_Y),
            (win_rect.right + 20, GROUND_Y),
            (win_rect.right + 10, win_rect.bottom),
            (win_rect.left - 10, win_rect.bottom),
        ]
        beam_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(beam_surf, (200, 200, 180, 25), beam_pts)
        surf.blit(beam_surf, (0, 0))

        # --- Wooden floor ---
        floor_y = GROUND_Y
        board_h = 18
        for row in range((height - floor_y) // board_h + 1):
            y = floor_y + row * board_h
            offset = (row % 2) * 40
            for col in range(width // 80 + 2):
                x = col * 80 + offset - 80
                base_r = rng.randint(120, 150)
                base_g = rng.randint(75, 95)
                base_b = rng.randint(40, 55)
                board_rect = pygame.Rect(x, y, 78, board_h - 1)
                pygame.draw.rect(surf, (base_r, base_g, base_b), board_rect)
                # Wood grain lines
                for _ in range(3):
                    gy = y + rng.randint(2, board_h - 3)
                    gx1 = x + rng.randint(0, 10)
                    gx2 = x + 78 - rng.randint(0, 10)
                    grain_c = (base_r - 15, base_g - 10, base_b - 5)
                    pygame.draw.line(surf, grain_c, (gx1, gy), (gx2, gy), 1)

        # --- Tatami mat details on floor edges ---
        tatami_color = (160, 150, 110)
        tatami_dark = (140, 130, 95)
        # Left tatami
        pygame.draw.rect(surf, tatami_color, (30, GROUND_Y + 5, 100, 20))
        pygame.draw.rect(surf, tatami_dark, (30, GROUND_Y + 5, 100, 20), 1)
        # Right tatami
        pygame.draw.rect(surf, tatami_color, (width - 130, GROUND_Y + 5, 100, 20))
        pygame.draw.rect(surf, tatami_dark, (width - 130, GROUND_Y + 5, 100, 20), 1)

        # --- Ceiling beam ---
        pygame.draw.rect(surf, (70, 55, 40), (0, 30, width, 12))
        # Decorative pillars
        for px in [width // 2 - 170, width // 2 + 170]:
            pygame.draw.rect(surf, (90, 60, 35), (px - 8, 30, 16, 370))
            pygame.draw.rect(surf, (100, 70, 40), (px - 10, 30, 20, 8))

        # --- Ambient vignette overlay ---
        vignette = pygame.Surface((width, height), pygame.SRCALPHA)
        for i in range(60):
            alpha = int(1.8 * i)
            pygame.draw.rect(vignette, (0, 0, 0, min(alpha, 120)),
                             (i, i, width - 2 * i, height - 2 * i), 2)
        surf.blit(vignette, (0, 0))

        self._surface = surf
        return surf


# ---------------------------------------------------------------------------
# Street
# ---------------------------------------------------------------------------

class StreetStage:
    """City night, neon signs, buildings, street lights."""

    def __init__(self):
        self._seed = 77
        self._surface = None

    def get_ground_y(self):
        return GROUND_Y

    def prerender(self, width, height):
        rng = random.Random(self._seed)
        surf = pygame.Surface((width, height))

        # --- Night sky gradient ---
        for y in range(GROUND_Y):
            t = y / GROUND_Y
            r = int(10 + t * 15)
            g = int(8 + t * 12)
            b = int(30 + t * 20)
            pygame.draw.line(surf, (r, g, b), (0, y), (width, y))

        # --- Stars ---
        for _ in range(40):
            sx = rng.randint(0, width)
            sy = rng.randint(0, GROUND_Y // 2)
            bright = rng.randint(150, 255)
            surf.set_at((sx, sy), (bright, bright, min(255, bright + rng.randint(0, 20))))

        # --- Background buildings (far) ---
        for i in range(12):
            bw = rng.randint(50, 100)
            bh = rng.randint(120, 280)
            bx = rng.randint(-20, width - bw + 20)
            by = GROUND_Y - bh
            shade = rng.randint(20, 45)
            pygame.draw.rect(surf, (shade, shade, shade + 10), (bx, by, bw, bh))
            # Windows
            for wy in range(by + 10, GROUND_Y - 15, 20):
                for wx in range(bx + 8, bx + bw - 8, 16):
                    if rng.random() > 0.35:
                        wcolor = rng.choice([
                            (255, 230, 120),
                            (200, 200, 255),
                            (255, 200, 100),
                            (180, 220, 255),
                        ])
                        pygame.draw.rect(surf, wcolor, (wx, wy, 8, 10))
                    else:
                        pygame.draw.rect(surf, (shade + 8, shade + 8, shade + 12), (wx, wy, 8, 10))

        # --- Mid-ground buildings ---
        for i in range(6):
            bw = rng.randint(70, 140)
            bh = rng.randint(180, 350)
            bx = rng.randint(-10, width - bw + 10)
            by = GROUND_Y - bh
            shade = rng.randint(30, 55)
            pygame.draw.rect(surf, (shade, shade - 3, shade + 5), (bx, by, bw, bh))
            # Rooftop detail
            pygame.draw.rect(surf, (shade + 10, shade + 8, shade + 12), (bx + 5, by - 8, bw - 10, 8))
            # Antenna
            if rng.random() > 0.5:
                ax = bx + bw // 2
                pygame.draw.line(surf, (60, 60, 60), (ax, by - 8), (ax, by - 30), 2)
                pygame.draw.circle(surf, (255, 30, 30), (ax, by - 30), 3)
            # Windows
            for wy in range(by + 12, GROUND_Y - 15, 18):
                for wx in range(bx + 6, bx + bw - 6, 14):
                    if rng.random() > 0.3:
                        wcolor = rng.choice([
                            (255, 235, 130),
                            (210, 210, 255),
                            (255, 190, 90),
                            (170, 200, 240),
                        ])
                        pygame.draw.rect(surf, wcolor, (wx, wy, 7, 9))
                    else:
                        pygame.draw.rect(surf, (shade + 5, shade + 3, shade + 8), (wx, wy, 7, 9))

        # --- Street / asphalt ---
        pygame.draw.rect(surf, (35, 35, 40), (0, GROUND_Y, width, height - GROUND_Y))
        # Curb
        pygame.draw.rect(surf, (55, 55, 55), (0, GROUND_Y, width, 4))
        # Road markings
        for mx in range(0, width, 60):
            pygame.draw.rect(surf, (70, 70, 65), (mx + 10, GROUND_Y + 80, 30, 4))
        # Sidewalk
        pygame.draw.rect(surf, (50, 50, 48), (0, GROUND_Y + 4, width, 20))
        # Sidewalk lines
        for sx in range(0, width, 40):
            pygame.draw.line(surf, (45, 45, 43), (sx, GROUND_Y + 4), (sx, GROUND_Y + 24), 1)

        # --- Neon signs ---
        neon_colors = [
            (255, 50, 100),   # pink
            (50, 200, 255),   # cyan
            (255, 100, 50),   # orange
            (100, 255, 100),  # green
            (255, 255, 50),   # yellow
        ]
        neon_signs = []
        for _ in range(5):
            nx = rng.randint(30, width - 120)
            ny = rng.randint(100, GROUND_Y - 100)
            nw = rng.randint(60, 120)
            nh = rng.randint(25, 50)
            nc = rng.choice(neon_colors)
            neon_signs.append((nx, ny, nw, nh, nc))
            # Sign backing
            pygame.draw.rect(surf, (20, 20, 25), (nx - 2, ny - 2, nw + 4, nh + 4))
            pygame.draw.rect(surf, nc, (nx, ny, nw, nh), 2)
            # Glow effect
            glow_surf = pygame.Surface((nw + 20, nh + 20), pygame.SRCALPHA)
            for g in range(8, 0, -1):
                alpha = 15 - g
                pygame.draw.rect(glow_surf, (*nc, alpha),
                                 (10 - g, 10 - g, nw + 2 * g, nh + 2 * g), 1)
            surf.blit(glow_surf, (nx - 10, ny - 10))
            # Simple text-like lines inside sign
            for tl in range(2):
                ly = ny + 8 + tl * 12
                lw = rng.randint(nw // 2, nw - 10)
                lx = nx + rng.randint(2, nw - lw - 2)
                pygame.draw.line(surf, nc, (lx, ly), (lx + lw, ly), 2)

        # --- Street lamps ---
        for lx in [120, width // 2 - 50, width - 120]:
            # Pole
            pygame.draw.rect(surf, (60, 55, 50), (lx, GROUND_Y - 160, 5, 160))
            # Arm
            pygame.draw.line(surf, (60, 55, 50), (lx + 2, GROUND_Y - 155), (lx + 25, GROUND_Y - 140), 3)
            # Lamp housing
            pygame.draw.polygon(surf, (80, 75, 65), [
                (lx + 15, GROUND_Y - 145),
                (lx + 35, GROUND_Y - 145),
                (lx + 32, GROUND_Y - 135),
                (lx + 18, GROUND_Y - 135),
            ])
            # Light glow
            light_surf = pygame.Surface((80, 100), pygame.SRCALPHA)
            for r in range(40, 0, -1):
                alpha = max(1, 12 - r // 4)
                pygame.draw.circle(light_surf, (255, 230, 150, alpha), (25, 10), r)
            surf.blit(light_surf, (lx + 5, GROUND_Y - 150))

        # --- Foreground: dumpster / fire hydrant ---
        # Fire hydrant
        hx = width - 60
        hy = GROUND_Y - 30
        pygame.draw.rect(surf, (180, 30, 30), (hx, hy, 18, 28))
        pygame.draw.rect(surf, (160, 25, 25), (hx - 3, hy + 2, 24, 8))
        pygame.draw.circle(surf, (180, 30, 30), (hx + 9, hy), 9)

        # --- Vignette ---
        vignette = pygame.Surface((width, height), pygame.SRCALPHA)
        for i in range(80):
            alpha = int(1.5 * i)
            pygame.draw.rect(vignette, (0, 0, 0, min(alpha, 140)),
                             (i, i, width - 2 * i, height - 2 * i), 2)
        surf.blit(vignette, (0, 0))

        self._surface = surf
        return surf


# ---------------------------------------------------------------------------
# Arena
# ---------------------------------------------------------------------------

class ArenaStage:
    """Fighting ring with ropes, crowd silhouettes, spotlights."""

    def __init__(self):
        self._seed = 123
        self._surface = None

    def get_ground_y(self):
        return GROUND_Y

    def prerender(self, width, height):
        rng = random.Random(self._seed)
        surf = pygame.Surface((width, height))

        # --- Dark arena background ---
        surf.fill((25, 20, 30))

        # --- Crowd silhouettes (upper section) ---
        crowd_top = 30
        crowd_bottom = GROUND_Y - 120
        for _ in range(300):
            cx = rng.randint(0, width)
            cy = rng.randint(crowd_top, crowd_bottom)
            head_r = rng.randint(6, 10)
            shade = rng.randint(15, 35)
            # Head
            pygame.draw.circle(surf, (shade, shade, shade + 5), (cx, cy), head_r)
            # Shoulders
            pygame.draw.ellipse(surf, (shade, shade, shade + 5),
                                (cx - head_r - 3, cy + head_r - 2, 2 * head_r + 6, head_r + 4))

        # --- Crowd rows (more structured, front rows) ---
        for row in range(3):
            ry = crowd_bottom - 30 + row * 25
            for col in range(width // 14 + 2):
                cx = col * 14 + rng.randint(-3, 3)
                shade = rng.randint(20, 40)
                hr = rng.randint(7, 10)
                pygame.draw.circle(surf, (shade, shade - 2, shade + 3), (cx, ry), hr)
                pygame.draw.ellipse(surf, (shade, shade - 2, shade + 3),
                                    (cx - hr - 2, ry + hr - 2, 2 * hr + 4, hr + 3))

        # --- Ring / platform ---
        # Platform surface
        ring_left = 60
        ring_right = width - 60
        ring_w = ring_right - ring_left

        # Raised platform side (depth)
        platform_depth = 30
        side_color = (60, 55, 50)
        pygame.draw.polygon(surf, side_color, [
            (ring_left, GROUND_Y),
            (ring_right, GROUND_Y),
            (ring_right + 10, GROUND_Y + platform_depth),
            (ring_left - 10, GROUND_Y + platform_depth),
        ])
        # Front face of platform
        pygame.draw.polygon(surf, (50, 45, 40), [
            (ring_left - 10, GROUND_Y + platform_depth),
            (ring_right + 10, GROUND_Y + platform_depth),
            (ring_right + 10, height),
            (ring_left - 10, height),
        ])
        # Platform top surface
        ring_color = (140, 130, 120)
        pygame.draw.rect(surf, ring_color, (ring_left, GROUND_Y - 6, ring_w, 8))
        # Canvas mat
        mat_color = (180, 50, 50)
        pygame.draw.rect(surf, mat_color, (ring_left + 5, GROUND_Y - 5, ring_w - 10, 6))
        # Mat texture lines
        for mx in range(ring_left + 15, ring_right - 10, 30):
            pygame.draw.line(surf, (170, 45, 45), (mx, GROUND_Y - 5), (mx, GROUND_Y + 1), 1)

        # --- Ring posts ---
        post_positions = [ring_left + 5, ring_right - 5]
        mid_left = ring_left + ring_w // 3
        mid_right = ring_left + 2 * ring_w // 3
        all_posts = [ring_left + 5, mid_left, mid_right, ring_right - 5]

        post_color = (180, 180, 180)
        post_highlight = (220, 220, 220)
        for px in all_posts:
            # Post
            pygame.draw.rect(surf, post_color, (px - 4, GROUND_Y - 80, 8, 82))
            pygame.draw.rect(surf, post_highlight, (px - 4, GROUND_Y - 80, 3, 82))
            # Post cap
            pygame.draw.circle(surf, (200, 200, 200), (px, GROUND_Y - 80), 6)

        # --- Ropes (3 levels) ---
        rope_colors = [
            (220, 220, 220),  # white
            (200, 200, 200),
            (180, 180, 180),
        ]
        rope_ys = [GROUND_Y - 70, GROUND_Y - 50, GROUND_Y - 30]
        for ry, rc in zip(rope_ys, rope_colors):
            # Rope shadow
            pygame.draw.line(surf, (80, 80, 80), (ring_left, ry + 2), (ring_right, ry + 2), 4)
            # Main rope
            pygame.draw.line(surf, rc, (ring_left, ry), (ring_right, ry), 3)
            # Rope highlight
            pygame.draw.line(surf, (255, 255, 255), (ring_left, ry - 1), (ring_right, ry - 1), 1)

        # --- Turnbuckles (where ropes meet posts) ---
        for px in all_posts:
            for ry in rope_ys:
                pygame.draw.circle(surf, (160, 160, 160), (px, ry), 5)
                pygame.draw.circle(surf, (200, 200, 200), (px, ry), 3)

        # --- Spotlights (light cones from above) ---
        spotlight_positions = [
            (width // 4, 0),
            (width // 2, 0),
            (3 * width // 4, 0),
        ]
        spot_colors = [
            (255, 240, 200),
            (200, 220, 255),
            (255, 200, 200),
        ]
        for (sx, _), sc in zip(spotlight_positions, spot_colors):
            cone_surf = pygame.Surface((width, height), pygame.SRCALPHA)
            cone_w = 180
            # Light cone
            pts = [
                (sx - 8, 0),
                (sx + 8, 0),
                (sx + cone_w, GROUND_Y),
                (sx - cone_w, GROUND_Y),
            ]
            pygame.draw.polygon(cone_surf, (*sc, 12), pts)
            # Brighter inner cone
            inner_w = 80
            pts_inner = [
                (sx - 3, 0),
                (sx + 3, 0),
                (sx + inner_w, GROUND_Y),
                (sx - inner_w, GROUND_Y),
            ]
            pygame.draw.polygon(cone_surf, (*sc, 18), pts_inner)
            surf.blit(cone_surf, (0, 0))

        # --- Spotlight fixtures on ceiling ---
        for sx, _ in spotlight_positions:
            pygame.draw.rect(surf, (50, 50, 55), (sx - 12, 0, 24, 15))
            pygame.draw.rect(surf, (70, 70, 75), (sx - 10, 0, 20, 12))
            # Light bulb glow
            pygame.draw.circle(surf, (255, 250, 220), (sx, 15), 5)

        # --- Ring apron / skirt ---
        apron_color = (40, 40, 45)
        pygame.draw.rect(surf, apron_color, (ring_left, GROUND_Y + 2, ring_w, platform_depth - 2))
        # Sponsor-like text blocks on apron
        for i in range(3):
            bx = ring_left + 40 + i * (ring_w // 3 - 20)
            by = GROUND_Y + 8
            bw = rng.randint(50, 80)
            bh = 14
            pygame.draw.rect(surf, (60, 60, 65), (bx, by, bw, bh))

        # --- Corner pads (colored) ---
        corner_colors = [(200, 50, 50), (50, 50, 200)]
        for i, px in enumerate([ring_left + 5, ring_right - 5]):
            cc = corner_colors[i % 2]
            pygame.draw.rect(surf, cc, (px - 8, GROUND_Y - 78, 16, 75))
            pygame.draw.rect(surf, (min(cc[0] + 40, 255), min(cc[1] + 40, 255), min(cc[2] + 40, 255)),
                             (px - 8, GROUND_Y - 78, 16, 3), 0)

        # --- Floor under ring ---
        pygame.draw.rect(surf, (30, 28, 35), (0, GROUND_Y + platform_depth, width, height - GROUND_Y - platform_depth))

        # --- Vignette ---
        vignette = pygame.Surface((width, height), pygame.SRCALPHA)
        for i in range(70):
            alpha = int(1.6 * i)
            pygame.draw.rect(vignette, (0, 0, 0, min(alpha, 130)),
                             (i, i, width - 2 * i, height - 2 * i), 2)
        surf.blit(vignette, (0, 0))

        self._surface = surf
        return surf


# ---------------------------------------------------------------------------
# Stage registry
# ---------------------------------------------------------------------------

STAGES = {
    'dojo': DojoStage,
    'street': StreetStage,
    'arena': ArenaStage,
}


def get_stage(name):
    """Return a stage instance by name. Raises KeyError if unknown."""
    return STAGES[name]()


def list_stages():
    """Return list of available stage names."""
    return list(STAGES.keys())
