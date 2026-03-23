import pygame
import sys
from game import Game
from renderer import Renderer, WIDTH, HEIGHT

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake-Man")
clock = pygame.time.Clock()

game = Game()
renderer = Renderer(screen)

MOVE_INTERVAL = 100  # ms between snake moves
move_timer = 0

running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game.game_over:
                if event.key == pygame.K_r:
                    game.reset()
                    move_timer = 0
            else:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    game.snake.set_direction(0, -1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    game.snake.set_direction(0, 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.snake.set_direction(-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.snake.set_direction(1, 0)
                elif event.key == pygame.K_SPACE:
                    game.shoot()

    if not game.game_over:
        move_timer += dt
        if move_timer >= MOVE_INTERVAL:
            move_timer = 0
            game.update(MOVE_INTERVAL)

    renderer.draw(game)

pygame.quit()
sys.exit()
