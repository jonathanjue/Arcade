import time
import pygame

TILE = 30
GRID = 20
WIDTH = TILE * GRID
HEIGHT = TILE * GRID + 40  # Extra for HUD

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
GREEN_HEAD = (0, 255, 0)
YELLOW = (255, 255, 0)
STAR_COLOR = (255, 255, 255)
PROJ_COLOR = (255, 255, 200)

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 64)

    def draw(self, game):
        self.screen.fill(BLACK)

        # Draw pellet
        if game.pellet:
            px, py = game.pellet
            center = (px * TILE + TILE // 2, py * TILE + TILE // 2)
            pygame.draw.circle(self.screen, YELLOW, center, TILE // 3)

        # Draw powerup (blinking)
        if game.powerup:
            if int(time.time() * 5) % 2 == 0:
                px, py = game.powerup
                cx = px * TILE + TILE // 2
                cy = py * TILE + TILE // 2
                # Star shape (simplified as diamond)
                points = [
                    (cx, cy - 12),
                    (cx + 8, cy),
                    (cx, cy + 12),
                    (cx - 8, cy),
                ]
                pygame.draw.polygon(self.screen, STAR_COLOR, points)

        # Draw snake
        for i, (sx, sy) in enumerate(game.snake.segments):
            color = GREEN_HEAD if i == 0 else GREEN
            rect = pygame.Rect(sx * TILE + 1, sy * TILE + 1, TILE - 2, TILE - 2)
            pygame.draw.rect(self.screen, color, rect, border_radius=4)

        # Draw ghosts
        for ghost in game.ghosts:
            if not ghost.dead:
                gx, gy = ghost.pos
                rect = pygame.Rect(gx * TILE + 2, gy * TILE + 2, TILE - 4, TILE - 4)
                pygame.draw.rect(self.screen, ghost.color, rect, border_radius=6)
                # Eyes
                eye_y = gy * TILE + 10
                pygame.draw.circle(self.screen, WHITE, (gx * TILE + 9, eye_y), 3)
                pygame.draw.circle(self.screen, WHITE, (gx * TILE + 21, eye_y), 3)
                pygame.draw.circle(self.screen, BLACK, (gx * TILE + 9, eye_y), 1)
                pygame.draw.circle(self.screen, BLACK, (gx * TILE + 21, eye_y), 1)

        # Draw projectiles
        for proj in game.projectiles:
            px, py = proj.pos
            center = (px * TILE + TILE // 2, py * TILE + TILE // 2)
            pygame.draw.circle(self.screen, PROJ_COLOR, center, 5)

        # HUD
        hud_y = GRID * TILE + 5
        power_status = "ACTIVE" if game.powerup_active else "READY"
        hud_text = f"Score: {game.score}  |  Length: {len(game.snake.segments)}  |  Power: {power_status}"
        hud_surface = self.font.render(hud_text, True, WHITE)
        self.screen.blit(hud_surface, (10, hud_y))

        # Game over overlay
        if game.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            if game.won:
                msg = "YOU WIN!"
            else:
                msg = "GAME OVER"
            text = self.big_font.render(msg, True, WHITE)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            self.screen.blit(text, rect)

            score_text = self.font.render(f"Final Score: {game.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            self.screen.blit(score_text, score_rect)

            restart_text = self.font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()
