import pygame
import random
import math

# Difficulty settings
DIFFICULTY = {
    "easy":   {"reaction_delay": 20, "combo_max": 2, "block_chance": 0.15, "special_chance": 0.1,  "punish_chance": 0.1,  "adaptation": 0.0},
    "normal": {"reaction_delay": 12, "combo_max": 3, "block_chance": 0.40, "special_chance": 0.3,  "punish_chance": 0.3,  "adaptation": 0.1},
    "hard":   {"reaction_delay": 6,  "combo_max": 4, "block_chance": 0.65, "special_chance": 0.5,  "punish_chance": 0.6,  "adaptation": 0.3},
    "cursed": {"reaction_delay": 2,  "combo_max": 6, "block_chance": 0.85, "special_chance": 0.7,  "punish_chance": 0.85, "adaptation": 0.5},
}

class AIController:
    def __init__(self, char_id, difficulty="normal"):
        self.char_id = char_id
        self.difficulty = difficulty
        self.settings = DIFFICULTY[difficulty]
        self.reaction_timer = 0
        self.current_action = None
        self.action_timer = 0
        self.move_history = []
        self.adapted_moves = {}  # Track what player does often
        self.state = "neutral"  # neutral, offense, defense, punish
        self.plan = []
        self.plan_index = 0
        self.last_player_move = None
        self.combo_index = 0

    def reset(self):
        self.reaction_timer = 0
        self.current_action = None
        self.action_timer = 0
        self.plan = []
        self.plan_index = 0
        self.combo_index = 0

    def update(self, fighter, opponent, combat_system):
        """Main AI update - returns simulated key presses"""
        self.reaction_timer += 1

        # Reaction delay check
        if self.reaction_timer < self.settings["reaction_delay"]:
            return self._get_current_keys()

        self.reaction_timer = 0

        # Determine state
        dist = abs(fighter.x - opponent.x)
        self._update_state(fighter, opponent, dist)

        # Execute plan or make new decision
        if self.plan and self.plan_index < len(self.plan):
            action = self.plan[self.plan_index]
            self.plan_index += 1
            return self._execute_action(action, fighter, opponent)
        else:
            self.plan = []
            self.plan_index = 0
            return self._make_decision(fighter, opponent, dist)

    def _update_state(self, fighter, opponent, dist):
        """Determine AI state based on situation"""
        if opponent.state in ["attack", "special", "super"] and dist < 120:
            self.state = "defend"
        elif fighter.cursed_energy >= 100 and dist < 200:
            self.state = "super"
        elif opponent.hp < fighter.hp * 0.5 and fighter.cursed_energy >= 50:
            self.state = "offense_aggro"
        elif dist < 100:
            self.state = "close"
        elif dist < 250:
            self.state = "mid"
        else:
            self.state = "far"

    def _make_decision(self, fighter, opponent, dist):
        """Choose action based on state"""
        keys = self._empty_keys()

        if self.state == "defend":
            # Block or dodge
            if random.random() < self.settings["block_chance"]:
                keys[pygame.K_s] = True
                # If close, try to punish after block
                if random.random() < self.settings["punish_chance"] and dist < 80:
                    self.plan = ["punish"]
                    self.plan_index = 0
            elif random.random() < 0.3:
                # Dodge back
                keys[pygame.K_a] = True
                keys[pygame.K_a] = True  # Double tap for dodge
            return keys

        elif self.state == "super":
            # Use ultimate
            self.plan = self._get_super_input(fighter)
            self.plan_index = 0
            return self._empty_keys()

        elif self.state == "offense_aggro":
            # Rush in and combo
            self.plan = self._get_combo_plan(fighter, max_hits=self.settings["combo_max"])
            self.plan_index = 0
            return self._empty_keys()

        elif self.state == "close":
            # Mix up attacks
            roll = random.random()
            if roll < 0.35:
                # Light attack
                keys[pygame.K_j] = True
            elif roll < 0.55:
                # Heavy attack
                keys[pygame.K_k] = True
            elif roll < 0.70 and random.random() < self.settings["special_chance"]:
                # Special move
                self.plan = self._get_special_input(fighter)
                self.plan_index = 0
            elif roll < 0.85:
                # Low attack (crouch + kick)
                keys[pygame.K_s] = True
                keys[pygame.K_k] = True
            else:
                # Block
                keys[pygame.K_s] = True
            return keys

        elif self.state == "mid":
            # Approach or use ranged moves
            if random.random() < 0.5:
                # Walk towards
                if fighter.x < opponent.x:
                    keys[pygame.K_d] = True
                else:
                    keys[pygame.K_a] = True
            elif random.random() < self.settings["special_chance"]:
                # Ranged special
                self.plan = self._get_ranged_input(fighter)
                self.plan_index = 0
            return keys

        else:  # far
            # Approach
            if fighter.x < opponent.x:
                keys[pygame.K_d] = True
            else:
                keys[pygame.K_a] = True
            # Dash if far enough
            if dist > 400:
                if fighter.x < opponent.x:
                    keys[pygame.K_d] = True
                else:
                    keys[pygame.K_a] = True
            return keys

    def _get_combo_plan(self, fighter, max_hits=3):
        """Generate a combo sequence"""
        moves = []
        char_data = fighter.char_data
        available = []

        # Get available moves
        for move_name, move_data in char_data.get("moves", {}).items():
            ce_cost = move_data.get("ce_cost", 0)
            if fighter.cursed_energy >= ce_cost:
                available.append((move_name, move_data))

        # Sort by damage
        available.sort(key=lambda x: x[1].get("damage", 0), reverse=True)

        # Build combo
        for i in range(min(max_hits, len(available))):
            move_name, move_data = available[i % len(available)]
            input_str = move_data.get("input", "J")
            moves.append(input_str)

        return moves

    def _get_special_input(self, fighter):
        """Get a special move input"""
        char_data = fighter.char_data
        specials = []
        for move_name, move_data in char_data.get("moves", {}).items():
            if move_data.get("type") in ["special", "ultimate"]:
                if fighter.cursed_energy >= move_data.get("ce_cost", 0):
                    specials.append(move_data.get("input", "J"))
        if specials:
            return [random.choice(specials)]
        return ["J"]

    def _get_ranged_input(self, fighter):
        """Get a ranged move input"""
        char_data = fighter.char_data
        ranged = []
        for move_name, move_data in char_data.get("moves", {}).items():
            if move_data.get("projectile") or move_data.get("range", 0) > 150:
                if fighter.cursed_energy >= move_data.get("ce_cost", 0):
                    ranged.append(move_data.get("input", "J"))
        if ranged:
            return [random.choice(ranged)]
        return ["J"]

    def _get_super_input(self, fighter):
        """Get super/ultimate input"""
        char_data = fighter.char_data
        for super_name, super_data in char_data.get("supers", {}).items():
            if fighter.cursed_energy >= super_data.get("ce_cost", 100):
                return [super_data.get("input", "J")]
        return self._get_special_input(fighter)

    def _execute_action(self, action, fighter, opponent):
        """Convert action string to key presses"""
        keys = self._empty_keys()

        if action == "punish":
            keys[pygame.K_j] = True
            return keys

        # Parse input notation (e.g., "236J" = down, down-forward, forward + J)
        if action == "J":
            keys[pygame.K_j] = True
        elif action == "K":
            keys[pygame.K_k] = True
        elif action == "L":
            keys[pygame.K_l] = True
        elif action == "6J" or action == "6K":
            keys[pygame.K_d] = True
            keys[pygame.K_j] = True if "J" in action else False
            keys[pygame.K_k] = True if "K" in action else False
        elif action == "2J" or action == "2K":
            keys[pygame.K_s] = True
            keys[pygame.K_j] = True if "J" in action else False
            keys[pygame.K_k] = True if "K" in action else False
        elif action == "8J" or action == "8K":
            keys[pygame.K_w] = True
            keys[pygame.K_j] = True if "J" in action else False
            keys[pygame.K_k] = True if "K" in action else False
        elif action.startswith("236"):
            # Quarter circle forward
            keys[pygame.K_s] = True
            key = "J" if "J" in action else "K"
            # Simplified: just do the final input
            keys[pygame.K_d] = True
            keys[getattr(pygame, f"K_{key.lower()}")] = True
        elif action.startswith("214"):
            # Quarter circle back
            keys[pygame.K_s] = True
            key = "J" if "J" in action else "K"
            keys[pygame.K_a] = True
            keys[getattr(pygame, f"K_{key.lower()}")] = True
        elif action.startswith("22"):
            # Double down
            keys[pygame.K_s] = True
            key = "J" if "J" in action else "K"
            keys[getattr(pygame, f"K_{key.lower()}")] = True
        elif action.startswith("66"):
            # Double forward
            keys[pygame.K_d] = True
            keys[pygame.K_d] = True
            key = "J" if "J" in action else "K"
            keys[getattr(pygame, f"K_{key.lower()}")] = True
        elif action.startswith("236236") or action.startswith("214214"):
            # Double quarter circle
            keys[pygame.K_l] = True
            keys[pygame.K_SPACE] = True
        elif action.startswith("222"):
            # Triple down (domain)
            keys[pygame.K_s] = True
            keys[pygame.K_SPACE] = True
        elif action.startswith("2146"):
            # Half circle
            keys[pygame.K_a] = True
            keys[pygame.K_d] = True
            keys[pygame.K_j] = True
        else:
            # Default
            keys[pygame.K_j] = True

        return keys

    def _empty_keys(self):
        return {k: False for k in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SPACE]}

    def _get_current_keys(self):
        """Return current held keys during action execution"""
        return self._empty_keys()

    def learn_from_player(self, player_action):
        """Track player habits for adaptation"""
        self.last_player_move = player_action
        self.adapted_moves[player_action] = self.adapted_moves.get(player_action, 0) + 1

    def get_counter_for(self, player_action):
        """Return counter action based on adaptation"""
        if random.random() > self.settings["adaptation"]:
            return None

        counters = {
            "attack": "block",
            "special": "dodge",
            "jump": "anti_air",
            "block": "grab",
        }
        return counters.get(player_action)


class BossAI(AIController):
    """Enhanced AI for story bosses"""
    def __init__(self, char_id, difficulty="hard", phase=1):
        super().__init__(char_id, difficulty)
        self.phase = phase
        self.phase_transition_hp = 0.5  # Switch phase at 50% HP
        self.pattern_index = 0

    def _make_decision(self, fighter, opponent, dist):
        # Boss-specific patterns
        if self.char_id == "mahito" and self.phase == 2:
            return self._mahito_phase2(fighter, opponent, dist)
        elif self.char_id == "sukuna":
            return self._sukuna_pattern(fighter, opponent, dist)
        elif self.char_id == "jogo":
            return self._jogo_pattern(fighter, opponent, dist)
        return super()._make_decision(fighter, opponent, dist)

    def _mahito_phase2(self, fighter, opponent, dist):
        """Mahito's aggressive phase 2"""
        keys = self._empty_keys()
        if dist < 100:
            if random.random() < 0.6:
                keys[pygame.K_j] = True  # Soul strike spam
            else:
                self.plan = ["236J", "22J"]  # Transfig + Triple arms
                self.plan_index = 0
        else:
            if fighter.x < opponent.x:
                keys[pygame.K_d] = True
            else:
                keys[pygame.K_a] = True
            if random.random() < 0.3:
                keys[pygame.K_w] = True  # Jump approach
        return keys

    def _sukuna_pattern(self, fighter, opponent, dist):
        """Sukuna's taunting pattern"""
        keys = self._empty_keys()
        # Sukuna uses dismantle frequently at range
        if dist > 150:
            if random.random() < 0.6:
                self.plan = ["236J", "236J", "236J"]  # Triple dismantle
                self.plan_index = 0
            else:
                if fighter.x < opponent.x:
                    keys[pygame.K_d] = True
                else:
                    keys[pygame.K_a] = True
        else:
            # Close range - use cleave or fire arrow
            if random.random() < 0.4:
                self.plan = ["236K"]  # Cleave
            elif random.random() < 0.3:
                self.plan = ["214J"]  # Fire arrow
            else:
                keys[pygame.K_j] = True
            self.plan_index = 0
        # Domain at low HP
        if fighter.hp < fighter.max_hp * 0.25 and fighter.cursed_energy >= 100:
            self.plan = ["222K"]
            self.plan_index = 0
        return keys

    def _jogo_pattern(self, fighter, opponent, dist):
        """Jogo's zoning pattern"""
        keys = self._empty_keys()
        if dist > 200:
            # Zone with projectiles
            roll = random.random()
            if roll < 0.4:
                self.plan = ["236J"]  # Volcano blast
            elif roll < 0.7:
                self.plan = ["236K"]  # Ember swarm
            else:
                self.plan = ["22J"]  # Meteor
            self.plan_index = 0
        elif dist > 100:
            if random.random() < 0.5:
                self.plan = ["214J"]  # Heat aura
            else:
                if fighter.x < opponent.x:
                    keys[pygame.K_a] = True  # Back away
                else:
                    keys[pygame.K_d] = True
            self.plan_index = 0
        else:
            # Too close - blast away
            self.plan = ["214J", "236J"]
            self.plan_index = 0
        return keys
