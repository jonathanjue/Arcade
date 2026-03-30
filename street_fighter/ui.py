"""
UI Module for 2D Street Fighting Game
Handles all UI drawing: health bars, meters, menus, character select, KO screen, move HUD.
Resolution: 1080x720
"""

import pygame
import math
import time as time_module

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# Core palette
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
RED         = (220, 30, 30)
DARK_RED    = (140, 0, 0)
GREEN       = (30, 200, 30)
DARK_GREEN  = (0, 120, 0)
BLUE        = (30, 80, 220)
DARK_BLUE   = (0, 40, 140)
YELLOW      = (255, 220, 0)
ORANGE      = (255, 150, 0)
CYAN        = (0, 220, 255)
MAGENTA     = (220, 0, 220)
GRAY        = (140, 140, 140)
DARK_GRAY   = (60, 60, 60)
LIGHT_GRAY  = (200, 200, 200)
GOLD        = (255, 215, 0)
SILVER      = (192, 192, 192)
P1_COLOR    = (0, 120, 255)
P2_COLOR    = (220, 30, 30)
CE_COLOR    = (0, 200, 255)
CE_BG       = (0, 60, 100)
KO_FLASH    = (255, 50, 50)
MENU_BG     = (20, 20, 40)
SELECT_BG   = (15, 15, 35)

# ---------------------------------------------------------------------------
# Helper: gradient surface
# ---------------------------------------------------------------------------

def _make_gradient(width, height, top_color, bottom_color):
    """Return a Surface filled with a vertical gradient."""
    surf = pygame.Surface((max(width, 1), max(height, 1)), pygame.SRCALPHA)
    if height < 1 or width < 1:
        return surf
    for y in range(height):
        ratio = y / max(height - 1, 1)
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        pygame.draw.line(surf, (r, g, b), (0, y), (width, y))
    return surf


# ---------------------------------------------------------------------------
# 1. Health bar
# ---------------------------------------------------------------------------

def draw_health_bar(surface, x, y, current, max_val, color, name, flip=False):
    """
    Draw a gradient-filled health bar with name label.

    Parameters
    ----------
    surface  : pygame.Surface – destination
    x, y     : int – top-left corner of the bar area
    current  : float – current health value
    max_val  : float – maximum health value
    color    : tuple – base RGB color (used for gradient top)
    name     : str – fighter name drawn above the bar
    flip     : bool – if True the bar fills from right-to-left (player 2)
    """
    BAR_W = 420
    BAR_H = 28
    BORDER = 3
    LABEL_H = 22

    # Background (dark)
    bg_rect = pygame.Rect(x, y + LABEL_H, BAR_W, BAR_H)
    pygame.draw.rect(surface, DARK_GRAY, bg_rect)
    pygame.draw.rect(surface, BLACK, bg_rect, BORDER)

    # Health fill
    ratio = max(0.0, min(1.0, current / max_val)) if max_val > 0 else 0
    fill_w = int(BAR_W * ratio)
    if fill_w > 0:
        # pick gradient colors based on health
        if ratio > 0.5:
            top_c = color
            bot_c = (max(color[0] - 60, 0), max(color[1] - 60, 0), max(color[2] - 60, 0))
        elif ratio > 0.25:
            top_c = YELLOW
            bot_c = ORANGE
        else:
            top_c = RED
            bot_c = DARK_RED

        gradient = _make_gradient(fill_w, BAR_H - BORDER * 2, top_c, bot_c)
        if flip:
            fill_x = x + BAR_W - fill_w
        else:
            fill_x = x
        fill_rect = pygame.Rect(fill_x, y + LABEL_H + BORDER, fill_w, BAR_H - BORDER * 2)
        surface.blit(gradient, fill_rect)

    # Shine highlight
    if fill_w > 0:
        shine_h = max(2, BAR_H // 4)
        shine_surf = pygame.Surface((fill_w, shine_h), pygame.SRCALPHA)
        shine_surf.fill((255, 255, 255, 50))
        if flip:
            shine_x = x + BAR_W - fill_w
        else:
            shine_x = x
        surface.blit(shine_surf, (shine_x, y + LABEL_H + BORDER))

    # Name label
    font = pygame.font.SysFont('arial', 18, bold=True)
    name_surf = font.render(name.upper(), True, WHITE)
    if flip:
        name_rect = name_surf.get_rect(topright=(x + BAR_W, y))
    else:
        name_rect = name_surf.get_rect(topleft=(x, y))
    surface.blit(name_surf, name_rect)

    # Numeric HP
    num_font = pygame.font.SysFont('arial', 14)
    hp_text = f"{int(current)}/{int(max_val)}"
    hp_surf = num_font.render(hp_text, True, LIGHT_GRAY)
    if flip:
        hp_rect = hp_surf.get_rect(topleft=(x + 4, y + LABEL_H + BAR_H - 2))
    else:
        hp_rect = hp_surf.get_rect(topright=(x + BAR_W - 4, y + LABEL_H + BAR_H - 2))
    surface.blit(hp_surf, hp_rect)


# ---------------------------------------------------------------------------
# 2. CE (special / super) bar
# ---------------------------------------------------------------------------

def draw_ce_bar(surface, x, y, current, max_val):
    """
    Draw the 'Critical Edge' / super meter below a health bar.

    Parameters
    ----------
    surface  : pygame.Surface
    x, y     : int – top-left position
    current  : float
    max_val  : float
    """
    BAR_W = 420
    BAR_H = 14
    BORDER = 2

    # Background
    bg_rect = pygame.Rect(x, y, BAR_W, BAR_H)
    pygame.draw.rect(surface, CE_BG, bg_rect)
    pygame.draw.rect(surface, BLACK, bg_rect, BORDER)

    ratio = max(0.0, min(1.0, current / max_val)) if max_val > 0 else 0
    fill_w = int(BAR_W * ratio)
    if fill_w > 0:
        # glow effect when full
        if ratio >= 1.0:
            pulse = (math.sin(time_module.time() * 6) + 1) / 2
            top_c = (
                int(CYAN[0] + (WHITE[0] - CYAN[0]) * pulse),
                int(CYAN[1] + (WHITE[1] - CYAN[1]) * pulse),
                int(CYAN[2] + (WHITE[2] - CYAN[2]) * pulse),
            )
            bot_c = CYAN
        else:
            top_c = CYAN
            bot_c = (0, 100, 180)

        gradient = _make_gradient(fill_w, BAR_H - BORDER * 2, top_c, bot_c)
        surface.blit(gradient, (x + BORDER, y + BORDER))

    # Segment markers (every 25 %)
    for seg in range(1, 4):
        sx = x + int(BAR_W * seg / 4)
        pygame.draw.line(surface, WHITE, (sx, y + BORDER), (sx, y + BAR_H - BORDER), 1)

    # Label
    font = pygame.font.SysFont('arial', 11, bold=True)
    label = font.render("CE", True, CYAN)
    surface.blit(label, (x + BAR_W + 6, y - 1))


# ---------------------------------------------------------------------------
# 3. Round counter
# ---------------------------------------------------------------------------

def draw_round_counter(surface, p1_wins, p2_wins, round_num):
    """
    Draw round indicator dots and round number centered at the top.

    Parameters
    ----------
    p1_wins  : int – rounds won by player 1
    p2_wins  : int – rounds won by player 2
    round_num: int – current round number (1-indexed)
    """
    cx = SCREEN_WIDTH // 2
    y_base = 8

    # "ROUND N" text
    font_big = pygame.font.SysFont('arial', 22, bold=True)
    rnd_surf = font_big.render(f"ROUND {round_num}", True, YELLOW)
    rnd_rect = rnd_surf.get_rect(center=(cx, y_base + 12))
    surface.blit(rnd_surf, rnd_rect)

    # Dot layout:  [P1 dots]  ---  center  ---  [P2 dots]
    dot_r = 7
    dot_gap = 22
    total_wins = 2  # best of 3
    # P1 dots on the left of center
    p1_start_x = cx - 60
    for i in range(total_wins):
        dx = p1_start_x - (total_wins - 1 - i) * dot_gap
        dy = y_base + 34
        if i < p1_wins:
            pygame.draw.circle(surface, P1_COLOR, (dx, dy), dot_r)
        pygame.draw.circle(surface, GRAY, (dx, dy), dot_r, 2)

    # P2 dots on the right of center
    p2_start_x = cx + 60
    for i in range(total_wins):
        dx = p2_start_x + i * dot_gap
        dy = y_base + 34
        if i < p2_wins:
            pygame.draw.circle(surface, P2_COLOR, (dx, dy), dot_r)
        pygame.draw.circle(surface, GRAY, (dx, dy), dot_r, 2)


# ---------------------------------------------------------------------------
# 4. Title Screen
# ---------------------------------------------------------------------------

class TitleScreen:
    """Main menu with arrow-key navigation."""

    MENU_ITEMS = ["VS MODE", "STORY", "QUIT"]

    def __init__(self):
        self.selected = 0
        self.title_font = pygame.font.SysFont('arial', 72, bold=True)
        self.item_font = pygame.font.SysFont('arial', 36)
        self.sub_font = pygame.font.SysFont('arial', 16)
        self.flash_timer = 0
        self.star_positions = [(i * 137 % SCREEN_WIDTH, i * 97 % SCREEN_HEIGHT)
                               for i in range(60)]

    # -- input -----------------------------------------------------------
    def handle_event(self, event):
        """Returns menu index when Enter/Return pressed, else None."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.MENU_ITEMS)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.MENU_ITEMS)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.selected
        return None

    # -- draw ------------------------------------------------------------
    def draw(self, surface):
        surface.fill(MENU_BG)

        # Decorative stars
        for sx, sy in self.star_positions:
            brightness = 80 + int(40 * math.sin(time_module.time() * 2 + sx))
            pygame.draw.circle(surface, (brightness, brightness, brightness), (sx, sy), 1)

        # Title
        title_surf = self.title_font.render("STREET FIGHTER", True, RED)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 160))
        # Shadow
        shadow = self.title_font.render("STREET FIGHTER", True, DARK_RED)
        surface.blit(shadow, (title_rect.x + 3, title_rect.y + 3))
        surface.blit(title_surf, title_rect)

        # Subtitle
        sub = self.sub_font.render("A 2D Fighting Game", True, LIGHT_GRAY)
        surface.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2, 220)))

        # Menu items
        start_y = 320
        for idx, label in enumerate(self.MENU_ITEMS):
            color = YELLOW if idx == self.selected else WHITE
            prefix = ">  " if idx == self.selected else "   "
            item_surf = self.item_font.render(prefix + label, True, color)
            item_rect = item_surf.get_rect(center=(SCREEN_WIDTH // 2, start_y + idx * 56))
            surface.blit(item_surf, item_rect)

        # Footer
        foot = self.sub_font.render("UP/DOWN to navigate  |  ENTER to select", True, GRAY)
        surface.blit(foot, foot.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)))


# ---------------------------------------------------------------------------
# 5. Character Select
# ---------------------------------------------------------------------------

# Default roster entries  (name, color, moves dict)
_DEFAULT_ROSTER = [
    {"name": "RYU",      "color": (200, 200, 200),
     "moves": {"LP": "Light Punch", "HP": "Heavy Punch", "LK": "Light Kick",
               "HK": "Heavy Kick", "HADOUKEN": "QCF+P", "SHORYUKEN": "DP+P"}},
    {"name": "KEN",      "color": (220, 50, 50),
     "moves": {"LP": "Light Punch", "HP": "Heavy Punch", "LK": "Light Kick",
               "HK": "Heavy Kick", "HADOUKEN": "QCF+P", "SHORYUKEN": "DP+P"}},
    {"name": "CHUN-LI",  "color": (50, 50, 220),
     "moves": {"LP": "Light Punch", "HP": "Heavy Punch", "LK": "Light Kick",
               "HK": "Heavy Kick", "KIKOKEN": "QCF+P", "SPINNING BIRD": "Charge U+K"}},
    {"name": "GUILE",    "color": (50, 180, 50),
     "moves": {"LP": "Light Punch", "HP": "Heavy Punch", "LK": "Light Kick",
               "HK": "Heavy Kick", "SONIC BOOM": "Charge F+P", "SOMERSAULT": "Charge U+K"}},
    {"name": "BLANKA",   "color": (180, 180, 0),
     "moves": {"LP": "Light Punch", "HP": "Heavy Punch", "LK": "Light Kick",
               "HK": "Heavy Kick", "ROLL": "Charge F+P", "ELEC": "Mash P"}},
    {"name": "DHALSIM",  "color": (200, 130, 50),
     "moves": {"LP": "Light Punch", "HP": "Heavy Punch", "LK": "Light Kick",
               "HK": "Heavy Kick", "YOGA FIRE": "QCF+P", "YOGA TELEPORT": "DP+KK"}},
]


class CharacterSelect:
    """Grid of 6 characters with preview panel and move list."""

    def __init__(self, roster=None):
        self.roster = roster if roster is not None else list(_DEFAULT_ROSTER)
        self.cursor = 0          # 0-5 grid index
        self.confirmed = False
        self.p1_selection = None
        self.p2_selection = None
        self.current_player = 1  # which player is selecting

        self.title_font = pygame.font.SysFont('arial', 32, bold=True)
        self.name_font = pygame.font.SysFont('arial', 24, bold=True)
        self.info_font = pygame.font.SysFont('arial', 16)
        self.small_font = pygame.font.SysFont('arial', 14)

        # Grid layout constants
        self.GRID_COLS = 3
        self.GRID_ROWS = 2
        self.CELL_W = 150
        self.CELL_H = 170
        self.GRID_X = 60
        self.GRID_Y = 100
        self.PREVIEW_X = 560
        self.PREVIEW_Y = 100

    # -- input -----------------------------------------------------------
    def handle_event(self, event):
        """
        Returns selected character index on confirm, else None.
        After first confirm, switches to player 2 selection.
        """
        if event.type != pygame.KEYDOWN:
            return None

        col = self.cursor % self.GRID_COLS
        row = self.cursor // self.GRID_COLS

        if event.key == pygame.K_LEFT:
            col = (col - 1) % self.GRID_COLS
        elif event.key == pygame.K_RIGHT:
            col = (col + 1) % self.GRID_COLS
        elif event.key == pygame.K_UP:
            row = (row - 1) % self.GRID_ROWS
        elif event.key == pygame.K_DOWN:
            row = (row + 1) % self.GRID_ROWS
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.current_player == 1:
                self.p1_selection = self.cursor
                self.current_player = 2
            else:
                self.p2_selection = self.cursor
                self.confirmed = True
            return self.cursor
        else:
            return None

        self.cursor = row * self.GRID_COLS + col
        return None

    # -- draw helpers ----------------------------------------------------
    def _draw_char_cell(self, surface, idx, highlighted):
        col = idx % self.GRID_COLS
        row = idx // self.GRID_COLS
        x = self.GRID_X + col * (self.CELL_W + 16)
        y = self.GRID_Y + row * (self.CELL_H + 16)
        char = self.roster[idx]

        rect = pygame.Rect(x, y, self.CELL_W, self.CELL_H)
        # Border
        if highlighted:
            border_color = YELLOW
            border_w = 3
        else:
            border_color = GRAY
            border_w = 2
        pygame.draw.rect(surface, SELECT_BG, rect)
        pygame.draw.rect(surface, border_color, rect, border_w)

        # Character silhouette placeholder
        sil_rect = pygame.Rect(x + 20, y + 10, self.CELL_W - 40, self.CELL_H - 55)
        pygame.draw.rect(surface, char["color"], sil_rect)
        # Simple stick figure
        cx_s = sil_rect.centerx
        cy_s = sil_rect.centery
        pygame.draw.circle(surface, WHITE, (cx_s, cy_s - 20), 12, 2)
        pygame.draw.line(surface, WHITE, (cx_s, cy_s - 8), (cx_s, cy_s + 20), 2)
        pygame.draw.line(surface, WHITE, (cx_s - 14, cy_s), (cx_s + 14, cy_s), 2)
        pygame.draw.line(surface, WHITE, (cx_s - 10, cy_s + 30), (cx_s, cy_s + 20), 2)
        pygame.draw.line(surface, WHITE, (cx_s + 10, cy_s + 30), (cx_s, cy_s + 20), 2)

        # Name under cell
        name_surf = self.name_font.render(char["name"], True, WHITE)
        surface.blit(name_surf, name_surf.get_rect(center=(x + self.CELL_W // 2,
                                                           y + self.CELL_H - 18)))

    def _draw_preview(self, surface, idx):
        char = self.roster[idx]
        px, py = self.PREVIEW_X, self.PREVIEW_Y

        # Preview box
        preview_rect = pygame.Rect(px, py, 440, 520)
        pygame.draw.rect(surface, (25, 25, 50), preview_rect)
        pygame.draw.rect(surface, GOLD, preview_rect, 2)

        # Player indicator
        p_label = f"P{self.current_player} SELECT"
        p_surf = self.title_font.render(p_label, True,
                                        P1_COLOR if self.current_player == 1 else P2_COLOR)
        surface.blit(p_surf, (px + 10, py + 8))

        # Large character preview
        big_rect = pygame.Rect(px + 30, py + 50, 180, 220)
        pygame.draw.rect(surface, char["color"], big_rect)
        # Larger stick figure
        cx_b = big_rect.centerx
        cy_b = big_rect.centery
        pygame.draw.circle(surface, WHITE, (cx_b, cy_b - 40), 24, 2)
        pygame.draw.line(surface, WHITE, (cx_b, cy_b - 16), (cx_b, cy_b + 40), 2)
        pygame.draw.line(surface, WHITE, (cx_b - 28, cy_b), (cx_b + 28, cy_b), 2)
        pygame.draw.line(surface, WHITE, (cx_b - 20, cy_b + 70), (cx_b, cy_b + 40), 2)
        pygame.draw.line(surface, WHITE, (cx_b + 20, cy_b + 70), (cx_b, cy_b + 40), 2)

        # Name
        n_surf = self.name_font.render(char["name"], True, GOLD)
        surface.blit(n_surf, (px + 10, py + 285))

        # Stats placeholder bars
        stats = [("POWER", 0.7), ("SPEED", 0.5), ("RANGE", 0.6), ("DEFENSE", 0.8)]
        for si, (sname, sval) in enumerate(stats):
            sy = py + 320 + si * 28
            s_label = self.info_font.render(sname, True, LIGHT_GRAY)
            surface.blit(s_label, (px + 10, sy))
            bar_rect = pygame.Rect(px + 100, sy + 2, 200, 14)
            pygame.draw.rect(surface, DARK_GRAY, bar_rect)
            fill_w = int(200 * sval)
            pygame.draw.rect(surface, CYAN, (px + 100, sy + 2, fill_w, 14))
            pygame.draw.rect(surface, GRAY, bar_rect, 1)

        # Move list
        self._draw_move_list(surface, char["moves"], px + 10, py + 440)

    def _draw_move_list(self, surface, moves_dict, x, y):
        title = self.info_font.render("MOVE LIST", True, YELLOW)
        surface.blit(title, (x, y))
        for i, (key, desc) in enumerate(list(moves_dict.items())[:4]):
            line = f"{key}: {desc}"
            t = self.small_font.render(line, True, LIGHT_GRAY)
            surface.blit(t, (x, y + 20 + i * 16))

    # -- public draw -----------------------------------------------------
    def draw(self, surface):
        surface.fill(SELECT_BG)
        # Title
        title = self.title_font.render("SELECT YOUR FIGHTER", True, WHITE)
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 40)))

        # Grid
        for idx in range(len(self.roster)):
            self._draw_char_cell(surface, idx, idx == self.cursor)

        # Preview
        self._draw_preview(surface, self.cursor)

        # Footer
        foot_font = pygame.font.SysFont('arial', 14)
        foot = foot_font.render("ARROWS to move  |  ENTER to confirm", True, GRAY)
        surface.blit(foot, foot.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)))


# ---------------------------------------------------------------------------
# 6. KO Screen
# ---------------------------------------------------------------------------

class KO_Screen:
    """
    KO animation overlay with round result text.
    Call update() each frame; draw() after background + fighters.
    """

    def __init__(self):
        self.active = False
        self.winner = 0           # 1 or 2
        self.start_time = 0
        self.duration = 3.0       # seconds
        self.ko_font = pygame.font.SysFont('arial', 120, bold=True)
        self.result_font = pygame.font.SysFont('arial', 36, bold=True)
        self.sub_font = pygame.font.SysFont('arial', 22)

    def trigger(self, winner):
        """Start the KO animation. winner = 1 or 2."""
        self.active = True
        self.winner = winner
        self.start_time = time_module.time()

    def update(self):
        """Returns True while animation is playing."""
        if not self.active:
            return False
        elapsed = time_module.time() - self.start_time
        if elapsed > self.duration:
            self.active = False
            return False
        return True

    def draw(self, surface):
        if not self.active:
            return
        elapsed = time_module.time() - self.start_time
        progress = min(1.0, elapsed / self.duration)

        # Flash overlay (fades out in first 0.6s)
        if elapsed < 0.6:
            alpha = int(200 * (1.0 - elapsed / 0.6))
            flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flash.fill((255, 255, 255, alpha))
            surface.blit(flash, (0, 0))

        # KO text – drops in from top with bounce
        drop_t = min(1.0, elapsed / 0.4)
        # Ease-out bounce approximation
        bounce = 1.0 - (1.0 - drop_t) ** 3
        ko_y = int(-100 + (SCREEN_HEIGHT // 2 - 60) * bounce)

        # Scale effect
        scale = 1.0 + 0.3 * max(0, 1.0 - elapsed / 0.3) if elapsed < 0.3 else 1.0
        ko_text = self.ko_font.render("K.O.!", True, KO_FLASH)
        w = int(ko_text.get_width() * scale)
        h = int(ko_text.get_height() * scale)
        if w > 0 and h > 0:
            ko_scaled = pygame.transform.scale(ko_text, (w, h))
            ko_rect = ko_scaled.get_rect(center=(SCREEN_WIDTH // 2, ko_y))
            # Shadow
            shadow = pygame.transform.scale(
                self.ko_font.render("K.O.!", True, DARK_RED), (w, h))
            surface.blit(shadow, (ko_rect.x + 4, ko_rect.y + 4))
            surface.blit(ko_scaled, ko_rect)

        # Result text (appears after 0.8s)
        if elapsed > 0.8:
            fade = min(1.0, (elapsed - 0.8) / 0.4)
            win_color = P1_COLOR if self.winner == 1 else P2_COLOR
            win_alpha = int(255 * fade)

            # "PLAYER X WINS!"
            result_str = f"PLAYER {self.winner} WINS!"
            result_surf = self.result_font.render(result_str, True, win_color)
            result_surf.set_alpha(win_alpha)
            result_rect = result_surf.get_rect(center=(SCREEN_WIDTH // 2,
                                                       SCREEN_HEIGHT // 2 + 40))
            surface.blit(result_surf, result_rect)

            # "ROUND OVER"
            sub_surf = self.sub_font.render("ROUND OVER", True, WHITE)
            sub_surf.set_alpha(int(255 * fade * 0.7))
            surface.blit(sub_surf, sub_surf.get_rect(center=(SCREEN_WIDTH // 2,
                                                             SCREEN_HEIGHT // 2 + 85)))

        # Bottom bar progress (shows remaining time)
        bar_w = int(SCREEN_WIDTH * progress)
        bar_h = 6
        pygame.draw.rect(surface, GOLD, (0, SCREEN_HEIGHT - bar_h, bar_w, bar_h))


# ---------------------------------------------------------------------------
# 7. Move HUD (in-fight)
# ---------------------------------------------------------------------------

def draw_move_hud(surface, moves_dict, x, y):
    """
    Draw a compact move list overlay during a fight.

    Parameters
    ----------
    surface   : pygame.Surface
    moves_dict: dict {input: move_name}  e.g. {"LP": "Light Punch", ...}
    x, y      : int – top-left position of the HUD box
    """
    if not moves_dict:
        return

    font_title = pygame.font.SysFont('arial', 14, bold=True)
    font_line = pygame.font.SysFont('arial', 12)

    entries = list(moves_dict.items())
    line_h = 16
    pad = 8
    box_w = 200
    box_h = pad * 2 + 20 + len(entries) * line_h

    # Background panel
    panel = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 160))
    surface.blit(panel, (x, y))
    pygame.draw.rect(surface, GRAY, (x, y, box_w, box_h), 1)

    # Title
    title = font_title.render("MOVES", True, YELLOW)
    surface.blit(title, (x + pad, y + pad))

    # Move entries
    for i, (inp, name) in enumerate(entries):
        line = f"{inp}: {name}"
        text_surf = font_line.render(line, True, LIGHT_GRAY)
        surface.blit(text_surf, (x + pad, y + pad + 20 + i * line_h))
