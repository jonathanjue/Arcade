import pygame, sys, math, time

# --- Configuration ---
WIDTH, HEIGHT = 800, 600
BG_COLOR = (200, 200, 200)  # light gray
FPS = 60

# Node types
NEUTRAL = "neutral"
DEFENSE = "defense"
INFECTED = "infected"

# Colors
COLOR_NEUTRAL = (150, 150, 150)
COLOR_DEFENSE = (0, 120, 255)
COLOR_INFECTED = (255, 0, 0)
COLOR_PLAYER = (255, 0, 0)
COLOR_LINE = (100, 100, 100)

# Simple graph layout (hard‑coded for demo)
# Each entry: (x, y, type, resistance_seconds)
NODES_DATA = [
    (200, 150, NEUTRAL, 3),   # 0
    (400, 150, DEFENSE, 5),   # 1
    (600, 150, NEUTRAL, 3),   # 2
    (200, 300, NEUTRAL, 4),   # 3
    (400, 300, NEUTRAL, 4),   # 4 (player start)
    (600, 300, DEFENSE, 6),   # 5
    (200, 450, NEUTRAL, 5),   # 6
    (400, 450, NEUTRAL, 5),   # 7
    (600, 450, NEUTRAL, 5),   # 8
]

# Connections (by index)
EDGES = [
    (0, 1), (1, 2),
    (0, 3), (1, 4), (2, 5),
    (3, 4), (4, 5),
    (3, 6), (4, 7), (5, 8),
    (6, 7), (7, 8)
]

class Node:
    RADIUS = 30
    def __init__(self, idx, pos, ntype, resistance):
        self.idx = idx
        self.pos = pygame.math.Vector2(pos)
        self.type = ntype
        self.base_resistance = resistance
        self.resistance = resistance  # seconds left to infect when player stays
        self.infected = False
        self.progress = 0.0  # 0..1 infection progress while player is on it
        self.last_update = None

    def reset(self):
        self.infected = False
        self.progress = 0.0
        self.resistance = self.base_resistance
        self.last_update = None

    def update(self, dt, player_on):
        if self.infected:
            return
        if player_on:
            # defense nodes slow infection by 2x
            factor = 2.0 if self.type == DEFENSE else 1.0
            self.progress += dt / (self.resistance * factor)
            if self.progress >= 1.0:
                self.infected = True
                self.type = INFECTED
        # no regression when player leaves – progress stays

    def draw(self, surf):
        color = COLOR_INFECTED if self.infected else (
            COLOR_DEFENSE if self.type == DEFENSE else COLOR_NEUTRAL)
        pygame.draw.circle(surf, color, (int(self.pos.x), int(self.pos.y)), self.RADIUS)
        # draw infection progress overlay for neutral nodes being infected
        if not self.infected and self.progress > 0:
            overlay = pygame.Surface((self.RADIUS*2, self.RADIUS*2), pygame.SRCALPHA)
            pygame.draw.circle(overlay, (255,0,0,120), (self.RADIUS, self.RADIUS), int(self.RADIUS*self.progress))
            surf.blit(overlay, (self.pos.x-self.RADIUS, self.pos.y-self.RADIUS))

class Player:
    RADIUS = 15
    SPEED = 200  # pixels per second
    def __init__(self, start_node):
        self.node = start_node  # current node index
        self.pos = pygame.math.Vector2(start_node.pos)
        self.target_node = None
        self.move_vec = pygame.math.Vector2(0,0)
        self.move_remaining = 0.0

    def set_target(self, node):
        if node is None:
            return
        self.target_node = node
        direction = node.pos - self.pos
        distance = direction.length()
        if distance == 0:
            self.move_vec = pygame.math.Vector2(0,0)
            self.move_remaining = 0
        else:
            self.move_vec = direction.normalize()
            self.move_remaining = distance

    def update(self, dt):
        if self.target_node:
            travel = self.SPEED * dt
            if travel >= self.move_remaining:
                # Arrive at target
                self.pos = self.target_node.pos
                self.node = self.target_node
                self.target_node = None
                self.move_remaining = 0
            else:
                self.pos += self.move_vec * travel
                self.move_remaining -= travel

    def draw(self, surf):
        pygame.draw.circle(surf, COLOR_PLAYER, (int(self.pos.x), int(self.pos.y)), self.RADIUS)

def build_graph():
    nodes = []
    for i, (x, y, t, r) in enumerate(NODES_DATA):
        nodes.append(Node(i, (x, y), t, r))
    # adjacency list
    adj = {i: [] for i in range(len(nodes))}
    for a, b in EDGES:
        adj[a].append(b)
        adj[b].append(a)
    return nodes, adj

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Infection Spread Game")
    clock = pygame.time.Clock()

    nodes, adjacency = build_graph()
    player = Player(nodes[4])  # start at node 4 (center)

    font = pygame.font.SysFont(None, 24)
    start_time = time.time()
    level_time_limit = 120  # seconds

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # movement keys – only allow if not already moving
                if player.target_node is None:
                    # find neighbours of current node
                    neighbours = adjacency[player.node.idx]
                    # map keys to neighbour indices (simple heuristic: up/down/left/right based on position)
                    keys = []
                    for n_idx in neighbours:
                        n = nodes[n_idx]
                        vec = n.pos - player.node.pos
                        angle = math.degrees(math.atan2(-vec.y, vec.x)) % 360
                        keys.append((angle, n))
                    # sort by angle for deterministic ordering
                    keys.sort(key=lambda a: a[0])
                    # assign directions: right (0°), up (90°), left (180°), down (270°)
                    direction_map = {}
                    for angle, n in keys:
                        if 315 <= angle or angle < 45:
                            direction_map[pygame.K_RIGHT] = n
                        elif 45 <= angle < 135:
                            direction_map[pygame.K_UP] = n
                        elif 135 <= angle < 225:
                            direction_map[pygame.K_LEFT] = n
                        else:
                            direction_map[pygame.K_DOWN] = n
                    # also support WASD
                    direction_map[pygame.K_d] = direction_map.get(pygame.K_RIGHT)
                    direction_map[pygame.K_w] = direction_map.get(pygame.K_UP)
                    direction_map[pygame.K_a] = direction_map.get(pygame.K_LEFT)
                    direction_map[pygame.K_s] = direction_map.get(pygame.K_DOWN)
                    # pick based on pressed key
                    if event.key in direction_map and direction_map[event.key]:
                        player.set_target(direction_map[event.key])
        # Update player movement
        player.update(dt)
        # Update nodes infection progress
        for node in nodes:
            player_on = (node.idx == player.node.idx) and (player.target_node is None)
            node.update(dt, player_on)
        # Check win/lose conditions
        all_infected = all(n.infected or n.type == INFECTED for n in nodes if n.type != DEFENSE)
        elapsed = time.time() - start_time
        if all_infected:
            msg = "All nodes infected! You win!"
            running = False
        elif elapsed > level_time_limit:
            msg = "Time's up! You lose."
            running = False
        # Draw
        screen.fill(BG_COLOR)
        # draw edges
        for a, b in EDGES:
            pygame.draw.line(screen, COLOR_LINE, nodes[a].pos, nodes[b].pos, 2)
        # draw nodes
        for node in nodes:
            node.draw(screen)
        # draw player
        player.draw(screen)
        # UI text
        timer_surf = font.render(f"Time: {int(level_time_limit - elapsed)}s", True, (0,0,0))
        screen.blit(timer_surf, (10,10))
        pygame.display.flip()
    # End screen
    screen.fill(BG_COLOR)
    end_surf = font.render(msg, True, (0,0,0))
    screen.blit(end_surf, (WIDTH//2 - end_surf.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
