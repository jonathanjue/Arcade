import pygame
import random
import math

GROUND_Y = 500

STAGES = {
    "tokyo_high": {
        "name": "Tokyo Jujutsu High",
        "bg_color": (35, 45, 60),
        "ground_color": (50, 55, 65),
        "accent_color": (80, 120, 90),
    },
    "shibuya": {
        "name": "Shibuya Crossing",
        "bg_color": (25, 20, 35),
        "ground_color": (45, 40, 55),
        "accent_color": (255, 100, 50),
    },
    "cursed_womb": {
        "name": "Cursed Spirit Womb",
        "bg_color": (20, 15, 25),
        "ground_color": (40, 30, 45),
        "accent_color": (150, 50, 100),
    },
    "goodwill_forest": {
        "name": "Goodwill Event Arena",
        "bg_color": (30, 50, 35),
        "ground_color": (55, 65, 50),
        "accent_color": (100, 180, 80),
    },
    "malevolent_shrine": {
        "name": "Malevolent Shrine",
        "bg_color": (40, 15, 15),
        "ground_color": (60, 30, 30),
        "accent_color": (255, 50, 50),
    },
    "culling_game": {
        "name": "Culling Game Arena",
        "bg_color": (30, 30, 40),
        "ground_color": (50, 50, 60),
        "accent_color": (100, 150, 255),
    },
}


class Stage:
    def __init__(self, stage_id="shibuya"):
        self.stage_id = stage_id
        data = STAGES.get(stage_id, STAGES["shibuya"])
        self.name = data["name"]
        self.bg_color = data["bg_color"]
        self.ground_color = data["ground_color"]
        self.accent_color = data["accent_color"]
        self.buildings = self._generate_buildings()
        self.ambient_particles = []
        self.frame = 0

    def _generate_buildings(self):
        buildings = []
        x = 0
        screen_w = 1280
        while x < screen_w + 100:
            w = random.randint(60, 140)
            h = random.randint(120, 350)
            windows = random.randint(3, 8)
            shade = random.randint(-15, 15)
            color = (
                max(0, min(255, self.bg_color[0] + 15 + shade)),
                max(0, min(255, self.bg_color[1] + 12 + shade)),
                max(0, min(255, self.bg_color[2] + 18 + shade)),
            )
            lit_windows = []
            for row in range(windows):
                for col in range(w // 25):
                    if random.random() > 0.4:
                        win_color = random.choice([
                            (255, 200, 100),
                            (100, 180, 255),
                            (200, 200, 180),
                        ])
                        lit_windows.append((col, row, win_color))
            buildings.append({"x": x, "w": w, "h": h, "windows": windows, "color": color, "lit": lit_windows})
            x += w + random.randint(8, 25)
        return buildings

    def update(self):
        self.frame += 1
        # Ambient particles
        if random.random() > 0.75:
            self.ambient_particles.append({
                "x": random.randint(0, 1280),
                "y": GROUND_Y + 70,
                "vy": random.uniform(-0.5, -0.1),
                "vx": random.uniform(-0.2, 0.2),
                "life": random.randint(60, 150),
                "max_life": 150,
                "size": random.uniform(1, 3),
                "color": self.accent_color,
            })
        # Update particles
        for p in self.ambient_particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1
        self.ambient_particles = [p for p in self.ambient_particles if p["life"] > 0]

    def draw(self, surface):
        sw, sh = surface.get_size()
        # Sky gradient
        for y in range(sh):
            pct = y / sh
            r = int(self.bg_color[0] + pct * 12)
            g = int(self.bg_color[1] + pct * 10)
            b = int(self.bg_color[2] + pct * 15)
            pygame.draw.line(surface, (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))), (0, y), (sw, y))

        # Moon/light source
        moon_x = sw - 150
        moon_y = 80
        moon_surf = pygame.Surface((120, 120), pygame.SRCALPHA)
        pygame.draw.circle(moon_surf, (*self.accent_color, 40), (60, 60), 50)
        pygame.draw.circle(moon_surf, (*self.accent_color, 80), (60, 60), 30)
        pygame.draw.circle(moon_surf, (255, 255, 230, 120), (60, 60), 18)
        surface.blit(moon_surf, (moon_x - 60, moon_y - 60))

        # Buildings (parallax layer)
        for b in self.buildings:
            b_y = GROUND_Y - b["h"] + 80
            # Building body
            pygame.draw.rect(surface, b["color"], (b["x"], b_y, b["w"], b["h"]))
            # Roof detail
            pygame.draw.rect(surface, self.accent_color, (b["x"] + b["w"]//4, b_y - 8, b["w"]//2, 8))
            # Windows
            for col, row, wcolor in b["lit"]:
                wx = b["x"] + 10 + col * 25
                wy = b_y + 15 + row * (b["h"] // b["windows"])
                # Flicker some windows
                if random.random() > 0.99:
                    wcolor = (50, 50, 50)
                pygame.draw.rect(surface, wcolor, (wx, wy, 12, 15))
                # Window glow
                glow = pygame.Surface((18, 21), pygame.SRCALPHA)
                pygame.draw.rect(glow, (*wcolor, 30), (0, 0, 18, 21))
                surface.blit(glow, (wx - 3, wy - 3))

        # Ground
        pygame.draw.rect(surface, self.ground_color, (0, GROUND_Y + 80, sw, sh - GROUND_Y))
        # Ground detail lines
        for i in range(0, sw, 40):
            line_shade = random.randint(-10, 10)
            color = (
                max(0, min(255, self.ground_color[0] + line_shade)),
                max(0, min(255, self.ground_color[1] + line_shade)),
                max(0, min(255, self.ground_color[2] + line_shade)),
            )
            pygame.draw.line(surface, color, (i, GROUND_Y + 82), (i + 20, GROUND_Y + 82), 1)
        # Ground edge
        pygame.draw.line(surface, self.accent_color, (0, GROUND_Y + 80), (sw, GROUND_Y + 80), 2)

        # Ambient particles
        for p in self.ambient_particles:
            alpha = int(200 * (p["life"] / p["max_life"]))
            color = p["color"]
            size = max(1, int(p["size"]))
            pygame.draw.circle(surface, color, (int(p["x"]), int(p["y"])), size)

    def draw_health_bars_bg(self, surface):
        """Draw semi-transparent background behind health bars"""
        bg = pygame.Surface((1280, 80), pygame.SRCALPHA)
        pygame.draw.rect(bg, (0, 0, 0, 100), (0, 0, 1280, 80))
        surface.blit(bg, (0, 0))
