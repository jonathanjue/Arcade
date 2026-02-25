import pygame
import math

# Hacker Defense Grid - Waves & Walls Update

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40
FPS = 60

# Colors
BLACK = (10, 10, 20)
GRID_COLOR = (30, 40, 50)
PATH_COLOR = (50, 50, 70)
WALL_COLOR = (100, 100, 120)
ENEMY_COLOR = (255, 50, 50)
TOWER_COLOR = (50, 150, 255)
RANGE_COLOR = (50, 150, 255, 50)
TEXT_COLOR = (0, 255, 0)

class Waypoint:
    def __init__(self, x, y):
        self.x, self.y = x, y

class Enemy:
    def __init__(self, path, health, speed=100.0):
        self.path = path
        self.index = 0
        self.x, self.y = float(path[0].x), float(path[0].y)
        self.speed = speed
        self.health = health
        self.max_health = health
        self.alive = True
        self.money_value = 5

    def update(self, dt, base_damage_func):
        if not self.alive:
            return

        # Move towards next waypoint
        if self.index < len(self.path) - 1:
            target = self.path[self.index + 1]
            dx = target.x - self.x
            dy = target.y - self.y
            dist = math.hypot(dx, dy)

            if dist > 0:
                travel = self.speed * dt
                if travel >= dist:
                    self.x, self.y = target.x, target.y
                    self.index += 1
                else:
                    self.x += (dx / dist) * travel
                    self.y += (dy / dist) * travel
        else:
            # Reached the end
            self.alive = False
            base_damage_func(10) # Deal damage to base

    def draw(self, surface):
        if not self.alive:
            return
        pygame.draw.circle(surface, ENEMY_COLOR, (int(self.x), int(self.y)), 10)

        # Health bar
        if self.health < self.max_health:
            ratio = self.health / self.max_health
            pygame.draw.rect(surface, (255, 0, 0), (self.x - 10, self.y - 18, 20, 4))
            pygame.draw.rect(surface, (0, 255, 0), (self.x - 10, self.y - 18, 20 * ratio, 4))

class Tower:
    def __init__(self, x, y, tower_type="basic"):
        self.x, self.y = x, y
        self.tower_type = tower_type
        self.setup_tower()
        self.cooldown = 0.0
        self.level = 1
        self.upgrade_cost = 30
        self.sell_value = 20
        self.money_value = 10
        self.slow_amount = 0.5
        self.slow_duration = 2.0
        self.freeze_duration = 1.0
        self.freeze_cooldown = 5.0
        self.freeze_timer = 0.0
        self.burn_damage = 5
        self.burn_duration = 3.0
        self.shock_damage = 10
        self.shock_cooldown = 3.0
        self.shock_timer = 0.0
        self.chain_range = 50
        self.poison_damage = 3
        self.poison_duration = 4.0
        self.armor_break_amount = 0.3
        self.armor_break_duration = 3.0
        self.range_boost_amount = 20
        self.damage_boost_amount = 0.2
        self.speed_boost_amount = 0.3
        self.grav_pull_amount = 50
        self.split_bonus = 2.0
        self.execution_threshold = 0.3
        self.corruption_amount = 0.5
        self.emp_cooldown = 8.0
        self.emp_timer = 0.0
        self.emp_duration = 2.0
        self.reactor_power = 1.0
        self.reactor_power_rate = 0.1
        self.reactor_max_power = 3.0
        self.reactor_cooldown = 10.0
        self.reactor_timer = 0.0

    def setup_tower(self):
        if self.tower_type == "basic":
            self.range = 100
            self.damage = 30
            self.cooldown_time = 0.5
        elif self.tower_type == "sniper":
            self.range = 300
            self.damage = 80
            self.cooldown_time = 2.0
        elif self.tower_type == "rapid":
            self.range = 80
            self.damage = 10
            self.cooldown_time = 0.1
        elif self.tower_type == "spread":
            self.range = 120
            self.damage = 15
            self.cooldown_time = 0.8
        elif self.tower_type == "slow":
            self.range = 90
            self.damage = 5
            self.cooldown_time = 1.0
        elif self.tower_type == "freeze":
            self.range = 100
            self.damage = 0
            self.cooldown_time = 0.5
        elif self.tower_type == "burn":
            self.range = 100
            self.damage = 10
            self.cooldown_time = 1.0
        elif self.tower_type == "shock":
            self.range = 150
            self.damage = 0
            self.cooldown_time = 3.0
        elif self.tower_type == "chain":
            self.range = 100
            self.damage = 25
            self.cooldown_time = 1.0
        elif self.tower_type == "poison":
            self.range = 100
            self.damage = 5
            self.cooldown_time = 1.5
        elif self.tower_type == "armor_breaker":
            self.range = 100
            self.damage = 20
            self.cooldown_time = 1.2
        elif self.tower_type == "money":
            self.range = 100
            self.damage = 5
            self.cooldown_time = 2.0
        elif self.tower_type == "range_booster":
            self.range = 80
            self.damage = 0
            self.cooldown_time = 0.0
        elif self.tower_type == "damage_booster":
            self.range = 80
            self.damage = 0
            self.cooldown_time = 0.0
        elif self.tower_type == "speed_booster":
            self.range = 80
            self.damage = 0
            self.cooldown_time = 0.0
        elif self.tower_type == "laser_core":
            self.range = 200
            self.damage = 15
            self.cooldown_time = 0.0
        elif self.tower_type == "drain":
            self.range = 120
            self.damage = 25
            self.cooldown_time = 1.0
        elif self.tower_type == "gravity_well":
            self.range = 150
            self.damage = 5
            self.cooldown_time = 0.5
        elif self.tower_type == "split":
            self.range = 120
            self.damage = 20
            self.cooldown_time = 1.0
        elif self.tower_type == "anti_swarm":
            self.range = 100
            self.damage = 15
            self.cooldown_time = 1.0
        elif self.tower_type == "execution":
            self.range = 100
            self.damage = 10
            self.cooldown_time = 1.5
        elif self.tower_type == "corruption":
            self.range = 100
            self.damage = 15
            self.cooldown_time = 1.2
        elif self.tower_type == "pulse_shield":
            self.range = 120
            self.damage = 0
            self.cooldown_time = 0.0
        elif self.tower_type == "emp":
            self.range = 180
            self.damage = 0
            self.cooldown_time = 0.0
        elif self.tower_type == "reactor":
            self.range = 100
            self.damage = 20
            self.cooldown_time = 0.0

    def update(self, dt, enemies):
        if self.cooldown > 0:
            self.cooldown -= dt
        if self.freeze_timer > 0:
            self.freeze_timer -= dt
        if self.shock_timer > 0:
            self.shock_timer -= dt
        if self.emp_timer > 0:
            self.emp_timer -= dt
        if self.reactor_timer > 0:
            self.reactor_timer -= dt
        else:
            self.reactor_power = min(self.reactor_power + self.reactor_power_rate * dt, self.reactor_max_power)

        if self.cooldown <= 0:
            if self.tower_type == "basic":
                # Find first enemy in range
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            # Shoot!
                            enemy.health -= self.damage * self.reactor_power
                            if enemy.health <= 0:
                                enemy.alive = False
                            self.cooldown = self.cooldown_time
                            return # Only shoot one per update tick (single target)
            elif self.tower_type == "sniper":
                # Find enemy closest to base
                closest = None
                min_index = float('inf')
                for enemy in enemies:
                    if enemy.alive and enemy.index < min_index:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            closest = enemy
                            min_index = enemy.index
                if closest:
                    closest.health -= self.damage * self.reactor_power
                    if closest.health <= 0:
                        closest.alive = False
                    self.cooldown = self.cooldown_time
            elif self.tower_type == "rapid":
                # Find first enemy in range
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            # Shoot!
                            enemy.health -= self.damage * self.reactor_power
                            if enemy.health <= 0:
                                enemy.alive = False
                            self.cooldown = self.cooldown_time
                            return # Only shoot one per update tick (single target)
            elif self.tower_type == "spread":
                # Damage all enemies in range
                hit_count = 0
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            enemy.health -= self.damage * self.reactor_power
                            if enemy.health <= 0:
                                enemy.alive = False
                            hit_count += 1
                if hit_count > 0:
                    self.cooldown = self.cooldown_time
            elif self.tower_type == "slow":
                # Apply slow to all enemies in range
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            # Apply slow effect (this would need to be tracked on the enemy)
                            pass
                self.cooldown = self.cooldown_time
            elif self.tower_type == "freeze":
                # Periodically freeze one enemy
                if self.freeze_timer <= 0:
                    # Find first enemy in range
                    for enemy in enemies:
                        if enemy.alive:
                            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                            if dist <= self.range:
                                # Freeze enemy (would need freeze state on enemy)
                                self.freeze_timer = self.freeze_cooldown
                                break
            elif self.tower_type == "burn":
                # Apply burn to first enemy in range
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            # Apply burn effect (would need burn state on enemy)
                            self.cooldown = self.cooldown_time
                            return
            elif self.tower_type == "shock":
                # Periodically damage all enemies in range
                if self.shock_timer <= 0:
                    for enemy in enemies:
                        if enemy.alive:
                            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                            if dist <= self.range:
                                enemy.health -= self.shock_damage * self.reactor_power
                                if enemy.health <= 0:
                                    enemy.alive = False
                    self.shock_timer = self.shock_cooldown
            elif self.tower_type == "chain":
                # Damage one enemy and chain to nearby enemy
                main_target = None
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            main_target = enemy
                            break
                if main_target:
                    main_target.health -= self.damage * self.reactor_power
                    if main_target.health <= 0:
                        main_target.alive = False
                    # Chain to nearby enemy
                    chain_target = None
                    chain_dist = float('inf')
                    for enemy in enemies:
                        if enemy.alive and enemy != main_target:
                            dist = math.hypot(enemy.x - main_target.x, enemy.y - main_target.y)
                            if dist < chain_dist and dist <= self.chain_range:
                                chain_target = enemy
                                chain_dist = dist
                    if chain_target:
                        chain_target.health -= self.damage * 0.5 * self.reactor_power
                        if chain_target.health <= 0:
                            chain_target.alive = False
                    self.cooldown = self.cooldown_time
            elif self.tower_type == "poison":
                # Apply poison to first enemy in range
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            # Apply poison effect (would need poison state on enemy)
                            self.cooldown = self.cooldown_time
                            return
            elif self.tower_type == "armor_breaker":
                # Damage and reduce armor of first enemy in range
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            enemy.health -= self.damage * self.reactor_power
                            if enemy.health <= 0:
                                enemy.alive = False
                            # Apply armor break effect (would need armor state on enemy)
                            self.cooldown = self.cooldown_time
                            return
            elif self.tower_type == "money":
                # Low damage, bonus money on kill
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            enemy.health -= self.damage * self.reactor_power
                            if enemy.health <= 0:
                                enemy.alive = False
                                # Bonus money effect
                            self.cooldown = self.cooldown_time
                            return
            elif self.tower_type == "range_booster":
                # Increase range of nearby towers
                for tower in self.towers:
                    if tower != self:
                        dist = math.hypot(tower.x - self.x, tower.y - self.y)
                        if dist <= self.range:
                            # Increase tower's range
                            pass
                self.cooldown = self.cooldown_time
            elif self.tower_type == "damage_booster":
                # Increase damage of nearby towers
                for tower in self.towers:
                    if tower != self:
                        dist = math.hypot(tower.x - self.x, tower.y - self.y)
                        if dist <= self.range:
                            # Increase tower's damage
                            pass
                self.cooldown = self.cooldown_time
            elif self.tower_type == "speed_booster":
                # Increase attack speed of nearby towers
                for tower in self.towers:
                    if tower != self:
                        dist = math.hypot(tower.x - self.x, tower.y - self.y)
                        if dist <= self.range:
                            # Increase tower's attack speed
                            pass
                self.cooldown = self.cooldown_time
            elif self.tower_type == "laser_core":
                # Damage strongest enemy in range
                strongest = None
                max_health = -1
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range and enemy.health > max_health:
                            strongest = enemy
                            max_health = enemy.health
                if strongest:
                    strongest.health -= self.damage * self.reactor_power
                    if strongest.health <= 0:
                        strongest.alive = False
                    self.cooldown = self.cooldown_time
            elif self.tower_type == "drain":
                # Damage enemy and heal base
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            enemy.health -= self.damage * self.reactor_power
                            if enemy.health <= 0:
                                enemy.alive = False
                                # Heal base
                            self.cooldown = self.cooldown_time
                            return
            elif self.tower_type == "gravity_well":
                # Pull enemies toward center
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            # Apply gravity pull (would need to modify enemy movement)
                            pass
                self.cooldown = self.cooldown_time
            elif self.tower_type == "split":
                # Bonus damage if only one enemy in range
                targets = []
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            targets.append(enemy)
                if targets:
                    damage_multiplier = self.split_bonus if len(targets) == 1 else 1.0
                    for enemy in targets:
                        enemy.health -= self.damage * damage_multiplier * self.reactor_power
                        if enemy.health <= 0:
                            enemy.alive = False
                    self.cooldown = self.cooldown_time
            elif self.tower_type == "anti_swarm":
                # Damage increases with number of enemies
                targets = []
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            targets.append(enemy)
                if targets:
                    damage_multiplier = 1.0 + (len(targets) * 0.2)
                    for enemy in targets:
                        enemy.health -= self.damage * damage_multiplier * self.reactor_power
                        if enemy.health <= 0:
                            enemy.alive = False
                    self.cooldown = self.cooldown_time
            elif self.tower_type == "execution":
                # Massive bonus damage if enemy below threshold
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            damage_multiplier = self.split_bonus if enemy.health / enemy.max_health <= self.execution_threshold else 1.0
                            enemy.health -= self.damage * damage_multiplier * self.reactor_power
                            if enemy.health <= 0:
                                enemy.alive = False
                            self.cooldown = self.cooldown_time
                            return
            elif self.tower_type == "corruption":
                # Mark enemy for extra damage
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            # Mark enemy (would need mark state on enemy)
                            enemy.health -= self.damage * self.reactor_power
                            if enemy.health <= 0:
                                enemy.alive = False
                            self.cooldown = self.cooldown_time
                            return
            elif self.tower_type == "pulse_shield":
                # Create damage reduction zone
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            # Reduce damage to base (would need to track this)
                            pass
                self.cooldown = self.cooldown_time
            elif self.tower_type == "emp":
                # Stun all enemies
                if self.emp_timer <= 0:
                    for enemy in enemies:
                        if enemy.alive:
                            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                            if dist <= self.range:
                                # Stun enemy (would need stun state on enemy)
                                pass
                    self.emp_timer = self.emp_cooldown
            elif self.tower_type == "reactor":
                # Gain power over time
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        if dist <= self.range:
                            enemy.health -= self.damage * self.reactor_power
                            if enemy.health <= 0:
                                enemy.alive = False
                            self.cooldown = self.cooldown_time
                            return

    def draw(self, surface):
        rect = pygame.Rect(self.x - 15, self.y - 15, 30, 30)
        pygame.draw.rect(surface, TOWER_COLOR, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 2) # Border

        # Draw tower type indicator
        font = pygame.font.SysFont("Arial", 10)
        type_text = font.render(self.tower_type[0].upper(), True, (255, 255, 255))
        surface.blit(type_text, (self.x - 5, self.y - 5))

        # Draw range circle for selected tower
        if hasattr(self, 'is_selected') and self.is_selected:
            pygame.draw.circle(surface, RANGE_COLOR, (self.x, self.y), self.range, 1)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Hacker Defense Grid")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier New", 20, bold=True)

        # Build path around "walls"
        # Walls at (300, 100) to (500, 500) block the middle
        self.path = [
            Waypoint(0, 100),
            Waypoint(250, 100),
            Waypoint(250, 500),
            Waypoint(550, 500),
            Waypoint(550, 100),
            Waypoint(800, 100)
        ]

        # Visual walls
        self.walls = [
            pygame.Rect(300, 150, 200, 300) # Big block in the middle
        ]

        self.enemies = []
        self.towers = []
        self.money = 120
        self.base_health = 100
        self.game_over = False

        # Wave settings
        self.wave = 0
        self.enemies_in_wave = 0
        self.spawn_timer = 0
        self.enemies_to_spawn = 0
        self.wave_in_progress = False
        self.start_next_wave()

    def start_next_wave(self):
        self.wave += 1
        self.enemies_to_spawn = 10 + (self.wave * 2)  # More enemies per wave
        self.spawn_timer = 0
        self.wave_in_progress = True
        self.enemies = []  # Clear previous wave
        print(f"Wave {self.wave} starting!")

        # Give money bonus for completing wave
        self.money += 50 + (self.wave * 10)

    def damage_base(self, amount):
        self.base_health -= amount
        if self.base_health <= 0:
            self.base_health = 0
            self.game_over = True

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return # Exit cleanly without sys

                if event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_SPACE and not self.wave_in_progress:
                        # Start next wave when space is pressed
                        self.start_next_wave()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    if event.button == 1: # Left click
                        self.handle_click(event.pos)

            if not self.game_over:
                self.update(dt)

            self.draw()
            pygame.display.flip()

    def handle_click(self, pos):
        mx, my = pos
        # Snap to grid
        gx = (mx // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
        gy = (my // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2

        # Check if clicking on existing tower to select
        clicked_tower = None
        for tower in self.towers:
            if abs(tower.x - gx) < 20 and abs(tower.y - gy) < 20:
                clicked_tower = tower
                break

        if clicked_tower:
            # Deselect all towers
            for t in self.towers:
                t.is_selected = False
            # Select clicked tower
            clicked_tower.is_selected = True
            return

        # Deselect all towers if clicking empty space
        for t in self.towers:
            t.is_selected = False

        # Check if clicking on tower shop area (right side)
        if mx > WIDTH - 200 and my < 500:  # Right sidebar area
            tower_index = my // 40
            tower_types = [
                "basic", "sniper", "rapid", "spread", "slow", "freeze", "burn",
                "shock", "chain", "poison", "armor_breaker", "money", "range_booster",
                "damage_booster", "speed_booster", "laser_core", "drain", "gravity_well",
                "split", "anti_swarm", "execution", "corruption", "pulse_shield", "emp", "reactor"
            ]
            if tower_index < len(tower_types):
                self.selected_tower_type = tower_types[tower_index]
                return

        # If a tower type is selected, place it
        if hasattr(self, 'selected_tower_type'):
            # Check cost for selected tower type
            tower_costs = {
                "basic": 40, "sniper": 80, "rapid": 30, "spread": 50, "slow": 45,
                "freeze": 60, "burn": 55, "shock": 65, "chain": 70, "poison": 50,
                "armor_breaker": 75, "money": 40, "range_booster": 35, "damage_booster": 35,
                "speed_booster": 35, "laser_core": 90, "drain": 85, "gravity_well": 80,
                "split": 60, "anti_swarm": 70, "execution": 95, "corruption": 85,
                "pulse_shield": 40, "emp": 100, "reactor": 120
            }
            cost = tower_costs.get(self.selected_tower_type, 40)
            if self.money < cost:
                return

            # Check collision with path, walls, or existing towers
            on_path = False
            for i in range(len(self.path)-1):
                p1 = self.path[i]
                p2 = self.path[i+1]
                if min(p1.x, p2.x) - 20 <= gx <= max(p1.x, p2.x) + 20 and \
                   min(p1.y, p2.y) - 20 <= gy <= max(p1.y, p2.y) + 20:
                    on_path = True
                    break

            in_wall = False
            for wall in self.walls:
                if wall.collidepoint(gx, gy):
                    in_wall = True

            on_tower = any(t.x == gx and t.y == gy for t in self.towers)

            if not on_path and not in_wall and not on_tower:
                self.towers.append(Tower(gx, gy, self.selected_tower_type))
                self.money -= cost
                delattr(self, 'selected_tower_type')  # Clear selection after placing

    def update(self, dt):
        # Wave Spawning
        if self.enemies_to_spawn > 0:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                health = 50 + (self.wave * 20)
                self.enemies.append(Enemy(self.path, health))
                self.enemies_to_spawn -= 1
                self.spawn_timer = 0.5  # Faster spawn rate (more packed)
                print(f"Spawned enemy, total: {len(self.enemies)}")  # Debug

        # Update Entities - move enemies first
        for enemy in self.enemies:
            enemy.update(dt, self.damage_base)
            print(f"Enemy at: {enemy.x}, {enemy.y}, index: {enemy.index}")  # Debug
        
        # Remove dead/finished enemies
        alive_enemies = []
        money_earned = 0
        for e in self.enemies:
            if e.alive:
                alive_enemies.append(e)
            elif e.health <= 0:
                # Killed by player
                money_earned += e.money_value
        self.enemies = alive_enemies
        self.money += money_earned
        print(f"After update: {len(self.enemies)} enemies")  # Debug

        for tower in self.towers:
            tower.update(dt, self.enemies)

        # Check if wave is done
        if self.enemies_to_spawn == 0 and len(self.enemies) == 0:
            # Wave complete - offer upgrade or continue
            self.wave_in_progress = False
            self.offer_wave_choice()

    def offer_wave_choice(self):
        """Ask player if they want to upgrade towers or start next wave"""
        # For now, just auto-start next wave after short delay
        # In a real UI, this would be a prompt
        pygame.time.wait(2000)  # 2 second pause
        self.start_next_wave()

    def draw(self):
        self.screen.fill(BLACK)

        # Draw Grid background
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y))

        # Draw Walls
        for wall in self.walls:
            pygame.draw.rect(self.screen, WALL_COLOR, wall)

        # Draw Path
        if len(self.path) >= 2:
            points = [(p.x, p.y) for p in self.path]
            pygame.draw.lines(self.screen, PATH_COLOR, False, points, 5)

        # Draw Enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw Towers
        for tower in self.towers:
            tower.draw(self.screen)
            # Draw tower-specific effects
            if tower.tower_type == "range_booster" or tower.tower_type == "damage_booster" or tower.tower_type == "speed_booster":
                # Draw boost radius
                pygame.draw.circle(self.screen, (0, 255, 0, 30), (tower.x, tower.y), tower.range, 1)
            elif tower.tower_type == "gravity_well":
                # Draw gravity well effect
                pygame.draw.circle(self.screen, (100, 50, 200, 50), (tower.x, tower.y), tower.range)
            elif tower.tower_type == "emp":
                # Draw EMP effect when active
                if tower.emp_timer > 0:
                    pygame.draw.circle(self.screen, (255, 100, 0, 50), (tower.x, tower.y), tower.range)

        # Draw tower ranges for selected tower
        for tower in self.towers:
            if hasattr(tower, 'is_selected') and tower.is_selected:
                pygame.circle(self.screen, (50, 150, 255, 30), (tower.x, tower.y), tower.range, 1)

        # UI - Tower Shop on right side
        shop_width = 200
        shop_x = WIDTH - shop_width

        # Draw shop background
        pygame.draw.rect(self.screen, (30, 40, 50), (shop_x, 0, shop_width, HEIGHT))

        # Draw tower shop items
        tower_types = [
            "basic", "sniper", "rapid", "spread", "slow", "freeze", "burn",
            "shock", "chain", "poison", "armor_breaker", "money", "range_booster",
            "damage_booster", "speed_booster", "laser_core", "drain", "gravity_well",
            "split", "anti_swarm", "execution", "corruption", "pulse_shield", "emp", "reactor"
        ]

        tower_costs = {
            "basic": 40, "sniper": 80, "rapid": 30, "spread": 50, "slow": 45,
            "freeze": 60, "burn": 55, "shock": 65, "chain": 70, "poison": 50,
            "armor_breaker": 75, "money": 40, "range_booster": 35, "damage_booster": 35,
            "speed_booster": 35, "laser_core": 90, "drain": 85, "gravity_well": 80,
            "split": 60, "anti_swarm": 70, "execution": 95, "corruption": 85,
            "pulse_shield": 40, "emp": 100, "reactor": 120
        }

        for i, tower_type in enumerate(tower_types):
            y = i * 40
            if y > HEIGHT - 40:
                break

            # Draw tower type background
            if hasattr(self, 'selected_tower_type') and self.selected_tower_type == tower_type:
                pygame.draw.rect(self.screen, (50, 150, 255), (shop_x + 5, y + 5, shop_width - 10, 35))
            else:
                pygame.draw.rect(self.screen, (60, 70, 80), (shop_x + 5, y + 5, shop_width - 10, 35))

            # Draw tower type indicator
            font = pygame.font.SysFont("Arial", 12)
            type_text = font.render(tower_type[0].upper(), True, (255, 255, 255))
            self.screen.blit(type_text, (shop_x + 15, y + 15))

            # Draw tower cost
            cost = tower_costs.get(tower_type, 0)
            cost_text = font.render(f"${cost}", True, (255, 255, 255))
            self.screen.blit(cost_text, (shop_x + 100, y + 15))

        # Draw shop title
        title_font = pygame.font.SysFont("Arial", 16, bold=True)
        title_text = title_font.render("TOWER SHOP", True, (255, 255, 255))
        self.screen.blit(title_text, (shop_x + 15, 10))

        # UI - Game info
        money_text = self.font.render(f"Money: ${self.money}", True, TEXT_COLOR)
        wave_text = self.font.render(f"Wave: {self.wave}", True, TEXT_COLOR)
        hp_text = self.font.render(f"Base HP: {self.base_health}", True, (255, 50, 50) if self.base_health < 30 else TEXT_COLOR)

        self.screen.blit(money_text, (10, 10))
        self.screen.blit(wave_text, (10, 40))
        self.screen.blit(hp_text, (10, 70))

        if not self.wave_in_progress and self.enemies_to_spawn == 0 and len(self.enemies) == 0:
            next_wave = self.font.render("Wave Complete! Press Space for next wave", True, (0, 255, 0))
            self.screen.blit(next_wave, (WIDTH//2 - 150, HEIGHT//2 - 50))
        elif self.enemies_to_spawn > 0:
            next_wave = self.font.render("Incoming...", True, (255, 255, 0))
            self.screen.blit(next_wave, (WIDTH - 150, 10))

        if self.game_over:
            over_text = self.font.render("GAME OVER", True, (255, 0, 0))
            scale_text = pygame.transform.scale(over_text, (400, 100))
            self.screen.blit(scale_text, (WIDTH//2 - 200, HEIGHT//2 - 50))

        # Draw tower info for selected tower
        for tower in self.towers:
            if hasattr(tower, 'is_selected') and tower.is_selected:
                info_text = self.font.render(f"Type: {tower.tower_type}", True, (255, 255, 255))
                range_text = self.font.render(f"Range: {tower.range}", True, (255, 255, 255))
                damage_text = self.font.render(f"Damage: {tower.damage}", True, (255, 255, 255))
                self.screen.blit(info_text, (WIDTH - 200, HEIGHT - 80))
                self.screen.blit(range_text, (WIDTH - 200, HEIGHT - 60))
                self.screen.blit(damage_text, (WIDTH - 200, HEIGHT - 40))

if __name__ == "__main__":
    game = Game()
    game.run()
