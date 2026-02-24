import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1100, 900
GRID_WIDTH = 800
SIDEBAR_WIDTH = 300
CELL_SIZE = 10
BASE_FPS = 15  # 1x speed
SPEED_LEVELS = [0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 8.0, 10.0]
SPEED_LABELS = ["0.25x", "0.5x", "1x", "1.5x", "2x", "3x", "4x", "5x", "8x", "10x"]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
RED = (220, 50, 50)
CELL_COLOR = (20, 20, 20)
GHOST_COLOR = (100, 160, 255, 120)
GRID_BG = (245, 245, 245)
GRID_LINE = (210, 210, 210)
SIDEBAR_BG = (38, 38, 38)
SIDEBAR_TEXT = (220, 220, 220)
BUTTON_BG = (55, 55, 55)
BUTTON_HOVER = (75, 75, 95)
BUTTON_ACTIVE = (70, 100, 160)
BUTTON_BORDER = (80, 80, 80)
CATEGORY_COLOR = (130, 170, 220)

ROWS = HEIGHT // CELL_SIZE
COLS = GRID_WIDTH // CELL_SIZE

# ─── PRESETS ───────────────────────────────────────────────────────────────────

PRESET_CATEGORIES = [
    ("Controls", ["Clear"]),
    ("Still Lifes", ["Block", "Beehive", "Loaf", "Boat", "Tub"]),
    ("Oscillators", ["Blinker", "Toad", "Beacon", "Pulsar", "Penta-decathlon", "Clock", "Figure Eight"]),
    ("Spaceships", ["Glider", "LWSS", "MWSS", "HWSS"]),
    ("Guns", ["Gosper Glider Gun", "Simkin Glider Gun"]),
    ("Duplicators", [
        "Blocker Duplicator",
        "4-Way Replicator",
        "Switch Engine",
        "Block Layer 1",
        "Glider Duplicator",
        "Infinite Growth 1",
        "Infinite Growth 2",
        "10-Cell Infinite",
        "Line Grower",
        "Max Spacefiller",
    ]),
    ("Methuselahs", ["R-pentomino", "Diehard", "Acorn", "Pi-heptomino", "B-heptomino", "Thunderbird"]),
    ("Puffers & Rakes", ["Puffer Train", "Space Rake"]),
    ("Misc / Fun", ["Pentadecathlon Ring", "Diamond", "Cross", "Lobster Claw", "Bomb", "Random Soup"]),
]

PRESETS = {
    "Clear": [],

    # ── Still Lifes ──
    "Block": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "Beehive": [(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 2)],
    "Loaf": [(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 3), (3, 2)],
    "Boat": [(0, 0), (0, 1), (1, 0), (1, 2), (2, 1)],
    "Tub": [(0, 1), (1, 0), (1, 2), (2, 1)],

    # ── Oscillators ──
    "Blinker": [(0, 0), (1, 0), (2, 0)],
    "Toad": [(1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2)],
    "Beacon": [(0, 0), (0, 1), (1, 0), (1, 1), (2, 2), (2, 3), (3, 2), (3, 3)],
    "Pulsar": [
        (2, 4), (2, 5), (2, 6), (2, 10), (2, 11), (2, 12),
        (4, 2), (4, 7), (4, 9), (4, 14),
        (5, 2), (5, 7), (5, 9), (5, 14),
        (6, 2), (6, 7), (6, 9), (6, 14),
        (7, 4), (7, 5), (7, 6), (7, 10), (7, 11), (7, 12),
        (9, 4), (9, 5), (9, 6), (9, 10), (9, 11), (9, 12),
        (10, 2), (10, 7), (10, 9), (10, 14),
        (11, 2), (11, 7), (11, 9), (11, 14),
        (12, 2), (12, 7), (12, 9), (12, 14),
        (14, 4), (14, 5), (14, 6), (14, 10), (14, 11), (14, 12),
    ],
    "Penta-decathlon": [
        (0, 1), (1, 1), (2, 0), (2, 2), (3, 1), (4, 1),
        (5, 1), (6, 1), (7, 0), (7, 2), (8, 1), (9, 1),
    ],
    "Clock": [(0, 1), (1, 2), (1, 3), (2, 0), (2, 1), (3, 2)],
    "Figure Eight": [
        (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2),
        (3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5),
    ],

    # ── Spaceships ──
    "Glider": [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
    "LWSS": [
        (0, 1), (0, 4), (1, 0), (2, 0), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3),
    ],
    "MWSS": [
        (0, 2), (1, 0), (1, 4), (2, 5), (3, 0), (3, 5), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
    ],
    "HWSS": [
        (0, 2), (0, 3), (1, 0), (1, 5), (2, 6), (3, 0), (3, 6),
        (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
    ],

    # ── Guns ──
    "Gosper Glider Gun": [
        (5, 1), (5, 2), (6, 1), (6, 2),
        (5, 11), (6, 11), (7, 11),
        (4, 12), (3, 13), (3, 14),
        (8, 12), (9, 13), (9, 14),
        (6, 15),
        (4, 16), (5, 17), (6, 17), (7, 17), (6, 18), (8, 16),
        (3, 21), (4, 21), (5, 21),
        (3, 22), (4, 22), (5, 22),
        (2, 23), (6, 23),
        (1, 25), (2, 25), (6, 25), (7, 25),
        (3, 35), (4, 35), (3, 36), (4, 36),
    ],
    "Simkin Glider Gun": [
        (0, 0), (0, 1), (1, 0), (1, 1),
        (0, 7), (0, 8), (1, 7), (1, 8),
        (3, 4), (3, 5), (4, 4), (4, 5),
        (9, 22), (9, 23), (10, 24), (11, 24), (11, 25),
        (10, 20), (11, 20), (12, 21), (13, 21), (13, 22),
        (9, 31), (9, 32), (9, 33),
        (10, 31),
        (11, 32),
        (18, 21), (18, 22), (19, 21), (19, 22),
    ],

    # ── Duplicators ──
    # These patterns grow indefinitely, replicating structure outward

    # "Blocker Duplicator" — a switch-engine predecessor that leaves blocks behind
    # (switch engine found by Charles Corderman)
    "Blocker Duplicator": [
        (0, 2), (0, 3), (0, 4),
        (1, 1), (1, 4),
        (2, 4),
        (3, 3),
        (4, 0), (4, 1),
        (5, 0), (5, 2),
    ],

    # "4-Way Replicator" — 4 R-pentominoes aimed outward from center, creates
    # explosive symmetric growth in all 4 directions
    "4-Way Replicator": [
        # Top R-pentomino (rotated)
        (0, 9), (0, 10), (1, 10), (1, 11), (2, 10),
        # Right R-pentomino (rotated)
        (9, 18), (9, 19), (10, 17), (10, 18), (11, 18),
        # Bottom R-pentomino (rotated)
        (18, 10), (18, 11), (19, 9), (19, 10), (20, 10),
        # Left R-pentomino (rotated)
        (10, 0), (10, 1), (9, 1), (11, 1), (9, 2),
    ],

    # "Infinite Growth 1" — classic 10-cell infinite growth pattern by Paul Callahan
    # Grows a line of cells infinitely to the right
    "Infinite Growth 1": [
        (0, 6),
        (1, 4), (1, 6), (1, 7),
        (2, 4), (2, 6),
        (3, 4),
        (4, 2),
        (5, 0), (5, 2),
    ],

    # "Infinite Growth 2" — 5x5 block infinite growth, expands into large debris field
    "Infinite Growth 2": [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        (0, 9), (0, 10), (0, 11), (0, 12), (0, 13),
        (0, 17), (0, 18), (0, 19),
        (0, 26), (0, 27), (0, 28), (0, 29), (0, 30), (0, 31), (0, 32),
        (0, 34), (0, 35), (0, 36), (0, 37), (0, 38),
    ],

    # "10-Cell Infinite" — the smallest known infinite growth pattern (10 cells)
    "10-Cell Infinite": [
        (0, 6),
        (1, 4), (1, 6), (1, 7),
        (2, 4), (2, 6),
        (3, 4),
        (4, 2),
        (5, 0), (5, 2),
    ],

    # "Switch Engine" — Charles Corderman's switch engine.
    # Moves diagonally leaving debris; one of the first infinite growth patterns found.
    "Switch Engine": [
        (0, 0), (0, 1),
        (1, 0), (1, 1),
        (2, 0), (2, 1),
        (3, 2),
        (4, 2), (4, 3),
        (5, 3),
    ],

    # "Block Layer 1" — a switch-engine-based pattern that lays down a trail of
    # blocks as it moves. Uses a stabilised switch engine predecessor.
    "Block Layer 1": [
        (0, 6),
        (1, 4), (1, 6), (1, 7),
        (2, 4), (2, 6),
        (3, 4),
        (4, 2),
        (5, 0), (5, 2),
        # stabiliser block that turns debris into a clean block trail
        (0, 10), (0, 11),
        (1, 10), (1, 11),
    ],

    # "Glider Duplicator" — Two Gosper guns facing each other offset so their
    # glider streams collide and produce two new glider streams at 90 degrees.
    # Net effect: one direction of gliders is "duplicated" into two directions.
    "Glider Duplicator": [
        # --- Gun 1 (standard Gosper glider gun) ---
        (5, 1), (5, 2), (6, 1), (6, 2),
        (5, 11), (6, 11), (7, 11),
        (4, 12), (3, 13), (3, 14),
        (8, 12), (9, 13), (9, 14),
        (6, 15),
        (4, 16), (5, 17), (6, 17), (7, 17), (6, 18), (8, 16),
        (3, 21), (4, 21), (5, 21),
        (3, 22), (4, 22), (5, 22),
        (2, 23), (6, 23),
        (1, 25), (2, 25), (6, 25), (7, 25),
        (3, 35), (4, 35), (3, 36), (4, 36),
        # --- Gun 2 (mirrored, offset down-right so streams collide) ---
        (20, 1), (20, 2), (19, 1), (19, 2),
        (20, 11), (19, 11), (18, 11),
        (21, 12), (22, 13), (22, 14),
        (17, 12), (16, 13), (16, 14),
        (19, 15),
        (21, 16), (20, 17), (19, 17), (18, 17), (19, 18), (17, 16),
        (22, 21), (21, 21), (20, 21),
        (22, 22), (21, 22), (20, 22),
        (23, 23), (19, 23),
        (24, 25), (23, 25), (19, 25), (18, 25),
        (22, 35), (21, 35), (22, 36), (21, 36),
    ],

    # "Max Spacefiller" — a pattern that fills space as fast as possible,
    # growing at the speed of light (c/2 diagonal). Based on two puffer
    # trains plus rakes that fill in between them.
    "Max Spacefiller": [
        # Front LWSS-like leader (top wing)
        (0, 14), (0, 15), (0, 16), (0, 17),
        (1, 13), (1, 17),
        (2, 17),
        (3, 13), (3, 16),
        # Front leader (bottom wing, mirrored)
        (7, 14), (7, 15), (7, 16), (7, 17),
        (6, 13), (6, 17),
        (5, 17),
        (4, 13), (4, 16),
        # Filler rake (top)
        (0, 5), (0, 6), (0, 7), (0, 8),
        (1, 4), (1, 8),
        (2, 8),
        (3, 4), (3, 7),
        # Filler rake (bottom, mirrored)
        (7, 5), (7, 6), (7, 7), (7, 8),
        (6, 4), (6, 8),
        (5, 8),
        (4, 4), (4, 7),
        # Puffer backbone (center)
        (2, 0), (3, 0), (4, 0), (5, 0),
        (1, 1), (6, 1),
        (0, 2), (7, 2),
        (0, 3), (7, 3),
    ],

    # "Line Grower" — produces a growing diagonal line of debris
    # (Lidka predecessor, starts small but grows for thousands of generations)
    "Line Grower": [
        (0, 1),
        (1, 2),
        (2, 0), (2, 1), (2, 2),
        # Second glider aimed at it to cause chain reaction
        (5, 10), (5, 11),
        (6, 10), (6, 11),
        # Spark
        (3, 8), (3, 9),
        (4, 8), (4, 9),
    ],

    # ── Methuselahs ──
    "R-pentomino": [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)],
    "Diehard": [(0, 6), (1, 0), (1, 1), (2, 1), (2, 5), (2, 6), (2, 7)],
    "Acorn": [(0, 1), (1, 3), (2, 0), (2, 1), (2, 4), (2, 5), (2, 6)],
    "Pi-heptomino": [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)],
    "B-heptomino": [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2), (3, 0)],
    "Thunderbird": [(0, 0), (0, 1), (0, 2), (2, 1), (3, 1), (4, 1)],

    # ── Puffers & Rakes ──
    "Puffer Train": [
        (0, 2), (1, 0), (1, 4), (2, 5), (3, 0), (3, 5), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
        (8, 0), (9, 1), (10, 0), (10, 1),
        (12, 0), (13, 1), (14, 0), (14, 1),
        (16, 2), (17, 0), (17, 4), (18, 5), (19, 0), (19, 5), (20, 1), (20, 2), (20, 3), (20, 4), (20, 5),
    ],
    "Space Rake": [
        (0, 7), (0, 8), (0, 9), (0, 10),
        (1, 6), (1, 10),
        (2, 10),
        (3, 6), (3, 9),
        (5, 0), (5, 1), (5, 2), (5, 3),
        (6, 0), (6, 4),
        (7, 0),
        (8, 1), (8, 4),
        (10, 3), (10, 4), (10, 5),
        (11, 3),
        (12, 4),
    ],

    # ── Misc / Fun ──
    "Pentadecathlon Ring": [
        (0, 5), (1, 5), (2, 4), (2, 6), (3, 5), (4, 5),
        (5, 5), (6, 5), (7, 4), (7, 6), (8, 5), (9, 5),
        (0, 15), (1, 15), (2, 14), (2, 16), (3, 15), (4, 15),
        (5, 15), (6, 15), (7, 14), (7, 16), (8, 15), (9, 15),
    ],
    "Diamond": [
        (0, 5), (1, 4), (1, 6), (2, 3), (2, 7),
        (3, 2), (3, 8), (4, 1), (4, 9),
        (5, 0), (5, 10),
        (6, 1), (6, 9), (7, 2), (7, 8),
        (8, 3), (8, 7), (9, 4), (9, 6), (10, 5),
    ],
    "Cross": [
        (0, 4), (0, 5), (0, 6),
        (1, 4), (1, 5), (1, 6),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10),
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10),
        (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10),
        (5, 4), (5, 5), (5, 6),
        (6, 4), (6, 5), (6, 6),
        (7, 4), (7, 5), (7, 6),
    ],
    "Lobster Claw": [
        (0, 2), (0, 3),
        (1, 0), (1, 1), (1, 4),
        (2, 0), (2, 4),
        (3, 1), (3, 3),
        (4, 2),
        (6, 2),
        (7, 1), (7, 3),
        (8, 0), (8, 4),
        (9, 0), (9, 1), (9, 4),
        (10, 2), (10, 3),
    ],

    # "Bomb" — a massive dense blob that explodes outward and destroys
    # anything in its path. Produces huge chaotic debris field.
    "Bomb": [],  # Generated dynamically

    "Random Soup": [],  # Generated dynamically
}


class GameOfLife:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Conway's Game of Life")
        self.clock = pygame.time.Clock()
        self.grid = set()
        self.running = False
        self.playing = False
        self.generation = 0
        self.population = 0
        self.font = pygame.font.SysFont("Segoe UI", 16)
        self.font_small = pygame.font.SysFont("Segoe UI", 13)
        self.font_title = pygame.font.SysFont("Segoe UI", 20, bold=True)
        self.font_cat = pygame.font.SysFont("Segoe UI", 14, bold=True)
        self.scroll_offset = 0
        self.max_scroll = 0
        self.preset_rects = {}
        self.dragging = False
        self._drag_erase = False
        self.speed_index = 2  # Default 1x

        # Stamp tool state
        self.stamp_name = None
        self.stamp_cells = []
        self.ghost_surface = None

        # Build sidebar items
        self.sidebar_items = []
        for cat_name, preset_names in PRESET_CATEGORIES:
            self.sidebar_items.append(("category", cat_name))
            for p in preset_names:
                self.sidebar_items.append(("preset", p))

    # ── Stamp helpers ──

    def select_stamp(self, name):
        """Select a preset as the active stamp tool."""
        if name == "Clear":
            self.grid.clear()
            self.generation = 0
            self.population = 0
            self.stamp_name = None
            self.stamp_cells = []
            self.ghost_surface = None
            return

        if name == "Random Soup":
            cx, cy = ROWS // 2, COLS // 2
            for _ in range(400):
                self.grid.add((cx + random.randint(-15, 15), cy + random.randint(-15, 15)))
            self.population = len(self.grid)
            self.stamp_name = None
            self.stamp_cells = []
            self.ghost_surface = None
            return

        if name == "Bomb":
            # Generate a dense 12x12 filled square — causes massive explosion
            cells = []
            for r in range(12):
                for c in range(12):
                    cells.append((r, c))
            self.stamp_name = name
            self.stamp_cells = cells
            self._build_ghost(cells)
            return

        cells = PRESETS.get(name, [])
        if not cells:
            return

        # Toggle off if clicking same stamp
        if self.stamp_name == name:
            self.stamp_name = None
            self.stamp_cells = []
            self.ghost_surface = None
            return

        self.stamp_name = name
        self.stamp_cells = cells
        self._build_ghost(cells)

    def _build_ghost(self, cells):
        """Pre-render ghost preview surface for a set of cells."""
        if not cells:
            self.ghost_surface = None
            return
        max_r = max(r for r, c in cells) + 1
        max_c = max(c for r, c in cells) + 1
        self.ghost_surface = pygame.Surface(
            (max_c * CELL_SIZE, max_r * CELL_SIZE), pygame.SRCALPHA
        )
        for r, c in cells:
            rect = pygame.Rect(c * CELL_SIZE + 1, r * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1)
            pygame.draw.rect(self.ghost_surface, GHOST_COLOR, rect)

    def place_stamp(self, grid_r, grid_c):
        """Place the current stamp at the given grid position (adds to existing)."""
        for r, c in self.stamp_cells:
            self.grid.add((grid_r + r, grid_c + c))
        self.population = len(self.grid)

    # ── Drawing ──

    def draw_grid_lines(self):
        for x in range(0, GRID_WIDTH + 1, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_LINE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT + 1, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_LINE, (0, y), (GRID_WIDTH, y))

    def draw_cells(self):
        for (r, c) in self.grid:
            x = c * CELL_SIZE
            y = r * CELL_SIZE
            if 0 <= x < GRID_WIDTH and 0 <= y < HEIGHT:
                rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 1, CELL_SIZE - 1)
                pygame.draw.rect(self.screen, CELL_COLOR, rect)

    def draw_stamp_preview(self):
        if not self.stamp_name or not self.ghost_surface:
            return
        mx, my = pygame.mouse.get_pos()
        if mx >= GRID_WIDTH:
            return
        grid_c = mx // CELL_SIZE
        grid_r = my // CELL_SIZE
        self.screen.blit(self.ghost_surface, (grid_c * CELL_SIZE, grid_r * CELL_SIZE))

    def draw_sidebar(self):
        sidebar_rect = pygame.Rect(GRID_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
        pygame.draw.rect(self.screen, SIDEBAR_BG, sidebar_rect)

        # Title
        title = self.font_title.render("Game of Life", True, WHITE)
        self.screen.blit(title, (GRID_WIDTH + 15, 12))

        # Stats
        gen_text = self.font_small.render(
            f"Gen: {self.generation}   Pop: {self.population}", True, SIDEBAR_TEXT
        )
        self.screen.blit(gen_text, (GRID_WIDTH + 15, 40))

        # Status
        if self.playing:
            status_surf = self.font.render("\u25b6 RUNNING", True, GREEN)
        else:
            status_surf = self.font.render("\u23f8 PAUSED", True, RED)
        self.screen.blit(status_surf, (GRID_WIDTH + 15, 60))

        # ── Speed Meter ──
        y_speed = 84
        speed_label = self.font_small.render("Speed:", True, SIDEBAR_TEXT)
        self.screen.blit(speed_label, (GRID_WIDTH + 15, y_speed))

        bar_x = GRID_WIDTH + 70
        bar_y = y_speed + 2
        bar_w = SIDEBAR_WIDTH - 85
        bar_h = 14
        pygame.draw.rect(self.screen, (25, 25, 25), (bar_x, bar_y, bar_w, bar_h), border_radius=7)

        fill_ratio = self.speed_index / (len(SPEED_LEVELS) - 1)
        fill_w = int(bar_w * fill_ratio)
        if fill_w > 0:
            if fill_ratio < 0.5:
                r_c = int(50 + fill_ratio * 2 * 200)
                g_c = 205
            else:
                r_c = 255
                g_c = int(205 - (fill_ratio - 0.5) * 2 * 180)
            bar_color = (r_c, g_c, 50)
            pygame.draw.rect(self.screen, bar_color, (bar_x, bar_y, fill_w, bar_h), border_radius=7)

        pygame.draw.rect(self.screen, (80, 80, 80), (bar_x, bar_y, bar_w, bar_h), 1, border_radius=7)
        spd_text = self.font_small.render(SPEED_LABELS[self.speed_index], True, WHITE)
        spd_rect = spd_text.get_rect(center=(bar_x + bar_w // 2, bar_y + bar_h // 2))
        self.screen.blit(spd_text, spd_rect)

        # ── Stamp Mode Indicator ──
        y_mode = y_speed + 20
        if self.stamp_name:
            mode_text = f"\U0001f528 Placing: {self.stamp_name}"
            mode_color = (100, 180, 255)
            hint_text = "Click grid to place \u00b7 Esc/Right-click cancel"
        else:
            mode_text = "\u270f\ufe0f Draw Mode"
            mode_color = (180, 180, 180)
            hint_text = "Click a preset to stamp it"
        mode_surf = self.font_small.render(mode_text, True, mode_color)
        self.screen.blit(mode_surf, (GRID_WIDTH + 15, y_mode))
        hint_surf = pygame.font.SysFont("Segoe UI", 11).render(hint_text, True, (120, 120, 120))
        self.screen.blit(hint_surf, (GRID_WIDTH + 15, y_mode + 16))

        # Controls
        controls = [
            "Space: Play / Pause",
            "C: Clear    R: Random",
            "+/-: Speed    Click: Draw",
            "Esc: Cancel stamp",
        ]
        y_off = y_mode + 38
        for line in controls:
            surf = self.font_small.render(line, True, (150, 150, 150))
            self.screen.blit(surf, (GRID_WIDTH + 15, y_off))
            y_off += 18

        # Divider
        y_off += 5
        pygame.draw.line(self.screen, (60, 60, 60), (GRID_WIDTH + 10, y_off), (WIDTH - 10, y_off))
        y_off += 10

        # ── Scrollable preset area ──
        presets_top = y_off
        presets_height = HEIGHT - presets_top
        preset_surface = pygame.Surface((SIDEBAR_WIDTH, presets_height))
        preset_surface.fill(SIDEBAR_BG)

        clip_rect = pygame.Rect(GRID_WIDTH, presets_top, SIDEBAR_WIDTH, presets_height)

        mx, my = pygame.mouse.get_pos()
        self.preset_rects = {}
        item_y = -self.scroll_offset
        item_height_button = 28
        item_height_cat = 26
        padding = 4

        total_height = 0
        for item_type, _ in self.sidebar_items:
            if item_type == "category":
                total_height += item_height_cat + padding
            else:
                total_height += item_height_button + padding
        self.max_scroll = max(0, total_height - presets_height + 10)

        for item_type, name in self.sidebar_items:
            if item_type == "category":
                if 0 <= item_y + item_height_cat and item_y < presets_height:
                    cat_surf = self.font_cat.render(f"\u2500 {name} \u2500", True, CATEGORY_COLOR)
                    preset_surface.blit(cat_surf, (10, item_y + 4))
                item_y += item_height_cat + padding
            else:
                btn_rect_local = pygame.Rect(10, item_y, SIDEBAR_WIDTH - 20, item_height_button)
                btn_rect_screen = pygame.Rect(
                    GRID_WIDTH + 10, presets_top + item_y, SIDEBAR_WIDTH - 20, item_height_button
                )

                if 0 <= item_y + item_height_button and item_y < presets_height:
                    is_active = self.stamp_name == name
                    hovered = clip_rect.collidepoint(mx, my) and btn_rect_screen.collidepoint(mx, my)

                    if is_active:
                        bg = BUTTON_ACTIVE
                    elif hovered:
                        bg = BUTTON_HOVER
                    else:
                        bg = BUTTON_BG

                    pygame.draw.rect(preset_surface, bg, btn_rect_local, border_radius=4)
                    pygame.draw.rect(preset_surface, BUTTON_BORDER, btn_rect_local, 1, border_radius=4)

                    text_surf = self.font_small.render(name, True, WHITE)
                    text_rect = text_surf.get_rect(center=btn_rect_local.center)
                    preset_surface.blit(text_surf, text_rect)

                self.preset_rects[name] = btn_rect_screen
                item_y += item_height_button + padding

        self.screen.blit(preset_surface, (GRID_WIDTH, presets_top))
        self._presets_top = presets_top

    # ── Simulation ──

    def get_neighbors(self, r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if (r + dr, c + dc) in self.grid:
                    count += 1
        return count

    def update_grid(self):
        if not self.playing:
            return

        new_grid = set()
        candidates = set()

        for (r, c) in self.grid:
            candidates.add((r, c))
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    candidates.add((r + dr, c + dc))

        for (r, c) in candidates:
            neigh = self.get_neighbors(r, c)
            alive = (r, c) in self.grid
            if alive and neigh in (2, 3):
                new_grid.add((r, c))
            elif not alive and neigh == 3:
                new_grid.add((r, c))

        self.grid = new_grid
        self.generation += 1
        self.population = len(self.grid)

    # ── Input ──

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # ── MOUSEWHEEL (pygame 2.x proper scroll) ──
            elif event.type == pygame.MOUSEWHEEL:
                mx, _ = pygame.mouse.get_pos()
                if mx > GRID_WIDTH:
                    self.scroll_offset -= event.y * 35
                    self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Legacy scroll (button 4/5) as fallback
                if event.button == 4:
                    if mx > GRID_WIDTH:
                        self.scroll_offset = max(0, self.scroll_offset - 35)
                elif event.button == 5:
                    if mx > GRID_WIDTH:
                        self.scroll_offset = min(self.max_scroll, self.scroll_offset + 35)

                # Right-click cancels stamp
                elif event.button == 3:
                    if self.stamp_name:
                        self.stamp_name = None
                        self.stamp_cells = []
                        self.ghost_surface = None

                # Left click
                elif event.button == 1:
                    if mx > GRID_WIDTH:
                        for name, rect in self.preset_rects.items():
                            if rect.collidepoint(mx, my) and my >= self._presets_top:
                                self.select_stamp(name)
                                break
                    else:
                        grid_c = mx // CELL_SIZE
                        grid_r = my // CELL_SIZE

                        if self.stamp_name and self.stamp_cells:
                            self.place_stamp(grid_r, grid_c)
                        else:
                            if (grid_r, grid_c) in self.grid:
                                self.grid.remove((grid_r, grid_c))
                                self.dragging = True
                                self._drag_erase = True
                            else:
                                self.grid.add((grid_r, grid_c))
                                self.dragging = True
                                self._drag_erase = False
                            self.population = len(self.grid)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False

            elif event.type == pygame.MOUSEMOTION and self.dragging and not self.stamp_name:
                mx, my = pygame.mouse.get_pos()
                if mx < GRID_WIDTH:
                    grid_c = mx // CELL_SIZE
                    grid_r = my // CELL_SIZE
                    if self._drag_erase:
                        self.grid.discard((grid_r, grid_c))
                    else:
                        self.grid.add((grid_r, grid_c))
                    self.population = len(self.grid)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.playing = not self.playing
                elif event.key == pygame.K_c:
                    self.grid.clear()
                    self.playing = False
                    self.generation = 0
                    self.population = 0
                elif event.key == pygame.K_r:
                    self.select_stamp("Random Soup")
                elif event.key == pygame.K_ESCAPE:
                    self.stamp_name = None
                    self.stamp_cells = []
                    self.ghost_surface = None
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                    self.speed_index = min(len(SPEED_LEVELS) - 1, self.speed_index + 1)
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    self.speed_index = max(0, self.speed_index - 1)

    # ── Main Loop ──

    def run(self):
        self.running = True
        while self.running:
            self.screen.fill(GRID_BG)
            self.handle_input()
            self.update_grid()

            self.draw_grid_lines()
            self.draw_cells()
            self.draw_stamp_preview()
            self.draw_sidebar()

            pygame.display.flip()
            current_fps = int(BASE_FPS * SPEED_LEVELS[self.speed_index])
            self.clock.tick(max(1, current_fps))

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = GameOfLife()
    game.run()
