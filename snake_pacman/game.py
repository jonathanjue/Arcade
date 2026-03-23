import random
import time

GRID_SIZE = 20

class Snake:
    def __init__(self):
        self.segments = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.growing = False

    def set_direction(self, dx, dy):
        # Prevent reversing
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.next_direction = (dx, dy)

    def move(self):
        self.direction = self.next_direction
        head = self.segments[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # Wrap around
        new_head = (new_head[0] % GRID_SIZE, new_head[1] % GRID_SIZE)

        if self.growing:
            self.segments.insert(0, new_head)
            self.growing = False
        else:
            self.segments.insert(0, new_head)
            self.segments.pop()

    def grow(self):
        self.growing = True

    def head(self):
        return self.segments[0]

    def hit_self(self):
        return self.head() in self.segments[1:]

    def lose_segment(self):
        if len(self.segments) > 1:
            self.segments.pop()
            return True
        return False


class Ghost:
    SPAWNS = [(0, 0), (19, 0), (0, 19), (19, 19)]
    COLORS = [(255, 0, 0), (255, 105, 180), (0, 255, 255), (255, 165, 0)]

    def __init__(self, index):
        self.spawn = self.SPAWNS[index % 4]
        self.pos = self.spawn
        self.color = self.COLORS[index % 4]
        self.direction = (0, 0)
        self.dead = False
        self.respawn_time = 0

    def update(self, snake_head, tick_rate):
        if self.dead:
            if time.time() >= self.respawn_time:
                self.dead = False
                self.pos = self.spawn
            return

        # Move toward snake 70% of the time
        if random.random() < 0.7:
            dx = snake_head[0] - self.pos[0]
            dy = snake_head[1] - self.pos[1]
            options = []
            if dx > 0: options.append((1, 0))
            if dx < 0: options.append((-1, 0))
            if dy > 0: options.append((0, 1))
            if dy < 0: options.append((0, -1))
            if options:
                self.direction = random.choice(options)
        else:
            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            if self.direction != (0, 0):
                rev = (-self.direction[0], -self.direction[1])
                dirs = [d for d in dirs if d != rev]
            self.direction = random.choice(dirs)

        new_pos = (
            (self.pos[0] + self.direction[0]) % GRID_SIZE,
            (self.pos[1] + self.direction[1]) % GRID_SIZE
        )
        self.pos = new_pos

    def kill(self):
        self.dead = True
        self.respawn_time = time.time() + 5


class Projectile:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction
        self.distance = 0

    def move(self):
        self.pos = (
            (self.pos[0] + self.direction[0]) % GRID_SIZE,
            (self.pos[1] + self.direction[1]) % GRID_SIZE
        )
        self.distance += 1
        return self.distance < 10


class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.ghosts = [Ghost(i) for i in range(4)]
        self.pellet = self._random_empty()
        self.powerup = None
        self.powerup_spawn_time = time.time() + 30
        self.powerup_active = False
        self.powerup_end_time = 0
        self.projectiles = []
        self.score = 0
        self.game_over = False
        self.won = False
        self.ghost_tick_accum = 0
        self.last_ghost_tick = 100  # ms

    def _random_empty(self):
        occupied = set(self.snake.segments)
        for g in self.ghosts:
            occupied.add(g.pos)
        while True:
            pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if pos not in occupied:
                return pos

    def _get_ghost_tick_rate(self):
        rate = max(50, 100 - (self.score // 100) * 10)
        return rate

    def shoot(self):
        if not self.powerup_active:
            return
        if len(self.projectiles) >= 3:
            return
        self.projectiles.append(Projectile(self.snake.head(), self.snake.direction))

    def update(self, dt_ms):
        if self.game_over:
            return

        # Move snake
        self.snake.move()

        # Check self collision
        if self.snake.hit_self():
            self.game_over = True
            return

        head = self.snake.head()

        # Eat pellet
        if head == self.pellet:
            self.snake.grow()
            self.score += 10
            self.pellet = self._random_empty()
            if self.score >= 500:
                self.won = True
                self.game_over = True
                return

        # Pick up powerup
        if self.powerup and head == self.powerup:
            self.powerup_active = True
            self.powerup_end_time = time.time() + 10
            self.powerup = None

        # Powerup timer
        if self.powerup_active and time.time() >= self.powerup_end_time:
            self.powerup_active = False

        # Spawn powerup
        if not self.powerup and not self.powerup_active:
            if time.time() >= self.powerup_spawn_time:
                self.powerup = self._random_empty()
                self.powerup_spawn_time = time.time() + 30
                self.powerup_despawn = time.time() + 15

        # Despawn powerup if not picked up
        if self.powerup and time.time() >= getattr(self, 'powerup_despawn', float('inf')):
            self.powerup = None

        # Update ghosts
        self.ghost_tick_accum += dt_ms
        ghost_rate = self._get_ghost_tick_rate()
        if self.ghost_tick_accum >= ghost_rate:
            self.ghost_tick_accum = 0
            for ghost in self.ghosts:
                ghost.update(head, ghost_rate)

        # Ghost collision with head
        for ghost in self.ghosts:
            if not ghost.dead and ghost.pos == head:
                if not self.snake.lose_segment():
                    self.game_over = True
                    return
                ghost.pos = ghost.spawn

        # Update projectiles
        alive_projectiles = []
        for proj in self.projectiles:
            if proj.move():
                hit = False
                for ghost in self.ghosts:
                    if not ghost.dead and ghost.pos == proj.pos:
                        ghost.kill()
                        self.score += 25
                        hit = True
                        break
                if not hit:
                    alive_projectiles.append(proj)
        self.projectiles = alive_projectiles
