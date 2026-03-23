# Echo Tag Protocol (FPS prototype)
# Build on an existing FPS preset (e.g., a simple shooter in this repo).
# This prototype adds a Pulse Scanner ability that reveals invisible enemies.

import pygame, random, sys, time

# ------------------------------------------------------------
# Config
# ------------------------------------------------------------
SCREEN_W, SCREEN_H = 800, 600
FPS = 60
PULSE_RADIUS = 150          # pixels
PULSE_DURATION = 5000       # ms visible after pulse (ring lasts 5 s)
PULSE_COOLDOWN = 5000       # ms between pulses
ENEMY_COLOR_VISIBLE = (255, 0, 0)
ENEMY_COLOR_INVISIBLE = (255, 0, 0, 30)  # semi‑transparent when hidden
PLAYER_COLOR = (0, 255, 0)

# ------------------------------------------------------------
# Helper classes
# ------------------------------------------------------------
class Enemy:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.visible_until = 0  # pygame.time.get_ticks() when visibility ends
        self.rect = pygame.Rect(x, y, 30, 30)
        # simple random movement
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        # bounce off walls
        if self.x < 0 or self.x > SCREEN_W - 30:
            self.vx *= -1
        if self.y < 0 or self.y > SCREEN_H - 30:
            self.vy *= -1
        self.rect.topleft = (self.x, self.y)

    def draw(self, surf, now):
        # Only draw when visible; otherwise remain hidden
        if now < self.visible_until:
            pygame.draw.rect(surf, ENEMY_COLOR_VISIBLE, self.rect)
        # else: do not draw anything (enemy stays invisible)

class Player:
    def __init__(self):
        self.x = SCREEN_W // 2
        self.y = SCREEN_H // 2
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.last_pulse = -PULSE_COOLDOWN
        self.pulse_start = -PULSE_DURATION  # timestamp of last pulse start
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(0, min(self.x, SCREEN_W - 30))
        self.y = max(0, min(self.y, SCREEN_H - 30))
        self.rect.topleft = (self.x, self.y)

    def can_pulse(self, now):
        return now - self.last_pulse >= PULSE_COOLDOWN

    def pulse(self, now, enemies):
        self.last_pulse = now
        self.pulse_start = now
        # reveal any enemy whose centre is within the pulse radius
        for e in enemies:
            dist_sq = (e.x - self.x) ** 2 + (e.y - self.y) ** 2
            if dist_sq <= PULSE_RADIUS ** 2:
                e.visible_until = now + PULSE_DURATION

# ------------------------------------------------------------
# Main loop
# ------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Echo Tag Protocol')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    player = Player()
    enemies = [Enemy(random.randint(0, SCREEN_W-30), random.randint(0, SCREEN_H-30)) for _ in range(10)]
    bullets = []  # list of active bullets

    running = True
    while running:
        dt = clock.tick(FPS)
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and player.can_pulse(now):
                    player.pulse(now, enemies)
                # Shoot with space bar
                if event.key == pygame.K_SPACE:
                    # spawn bullet at player centre
                    bullet_x = player.x + 15
                    bullet_y = player.y + 15
                    # bullet moves upward for simplicity
                    bullets.append({'rect': pygame.Rect(bullet_x-2, bullet_y-2, 4, 4), 'vx': 0, 'vy': -8})

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_w]: dy = -1
        if keys[pygame.K_s]: dy = 1
        if keys[pygame.K_a]: dx = -1
        if keys[pygame.K_d]: dx = 1
        if dx or dy:
            player.move(dx, dy)

        # Update enemies
        for e in enemies:
            e.update()

        # Update bullets
        for b in bullets[:]:
            b['rect'].x += b['vx']
            b['rect'].y += b['vy']
            # Remove if off-screen
            if b['rect'].right < 0 or b['rect'].left > SCREEN_W or b['rect'].bottom < 0 or b['rect'].top > SCREEN_H:
                bullets.remove(b)
                continue
            # Check collision with enemies while pulse is active (allow shooting during pulse)
            if now - player.pulse_start < PULSE_DURATION:
                for e in enemies[:]:
                    if e.rect.colliderect(b['rect']):
                        # enemy hit – remove enemy and bullet
                        enemies.remove(e)
                        if b in bullets:
                            bullets.remove(b)
                        break
        # Rendering
        screen.fill((30, 30, 30))
        # draw pulse ring if active (blue expanding ring)
        if now - player.pulse_start < PULSE_DURATION:
            # radius grows linearly to PULSE_RADIUS over the duration
            progress = (now - player.pulse_start) / PULSE_DURATION
            radius = int(progress * PULSE_RADIUS)
            pygame.draw.circle(screen, (0, 0, 255), (player.x+15, player.y+15), radius, 2)
        else:
            # draw ready indicator when pulse is off cooldown
            if player.can_pulse(now):
                pygame.draw.circle(screen, (0, 120, 255), (player.x+15, player.y+15), PULSE_RADIUS, 1)
        # draw enemies (only visible ones will render)
        for e in enemies:
            e.draw(screen, now)
        # draw bullets
        for b in bullets:
            pygame.draw.rect(screen, (255, 255, 0), b['rect'])
        pygame.draw.rect(screen, PLAYER_COLOR, player.rect)
        # HUD
        cd = max(0, (player.last_pulse + PULSE_COOLDOWN - now) // 1000)
        hud = f'Pulse cooldown: {cd}s'
        txt = font.render(hud, True, (255,255,255))
        screen.blit(txt, (5,5))
        pygame.display.flip()

        # Allow quitting with ESC key
        if keys[pygame.K_ESCAPE]:
            running = False
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
