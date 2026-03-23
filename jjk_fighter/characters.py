# Character definitions and moveset data

CHARACTERS = {
    "yuji": {
        "name": "Yuji Itadori",
        "title": "The Cursed Child",
        "archetype": "rushdown",
        "hp": 1000, "ce_max": 100, "speed": 5.5, "jump_power": -13,
        "color": (255, 150, 30),
        "unlock_cost": 0,
        "description": "Brawler with immense physical strength. No innate technique but devastating close-range combat.",
        "moves": {
            "jab":          {"input": "J",     "damage": 25, "ce_cost": 0,  "startup": 4, "active": 3, "recovery": 8,  "hitstun": 12, "kb_x": 3,  "kb_y": 0,  "type": "light",  "range": 50},
            "straight":     {"input": "6J",    "damage": 35, "ce_cost": 0,  "startup": 8, "active": 4, "recovery": 12, "hitstun": 15, "kb_x": 6,  "kb_y": -2, "type": "heavy",  "range": 65},
            "low_kick":     {"input": "2K",    "damage": 30, "ce_cost": 0,  "startup": 6, "active": 3, "recovery": 10, "hitstun": 14, "kb_x": 4,  "kb_y": 0,  "type": "light",  "range": 55, "low": True},
            "overhead_kick":{"input": "8K",    "damage": 45, "ce_cost": 0,  "startup": 10,"active": 5, "recovery": 14, "hitstun": 18, "kb_x": 5,  "kb_y": -5, "type": "heavy",  "range": 60, "overhead": True},
            "tackle":       {"input": "66K",   "damage": 40, "ce_cost": 0,  "startup": 12,"active": 6, "recovery": 16, "hitstun": 16, "kb_x": 8,  "kb_y": -3, "type": "heavy",  "range": 80},
            "divergent_fist":{"input": "236J",  "damage": 60, "ce_cost": 20, "startup": 10,"active": 5, "recovery": 18, "hitstun": 20, "kb_x": 10, "kb_y": -4, "type": "special", "range": 90, "vfx": "divergent_fist"},
            "manji_kick":   {"input": "214K",  "damage": 50, "ce_cost": 15, "startup": 3, "active": 8, "recovery": 15, "hitstun": 18, "kb_x": 7,  "kb_y": -6, "type": "special", "range": 55, "counter": True},
            "ce_punch":     {"input": "236K",  "damage": 70, "ce_cost": 30, "startup": 14,"active": 4, "recovery": 20, "hitstun": 22, "kb_x": 12, "kb_y": -5, "type": "special", "range": 70, "vfx": "ce_punch"},
            "black_flash":  {"input": "22J",   "damage": 120,"ce_cost": 40, "startup": 8, "active": 3, "recovery": 25, "hitstun": 30, "kb_x": 15, "kb_y": -10,"type": "ultimate","range": 60, "vfx": "black_flash", "guarantee_crit": True},
            "binding_vow":  {"input": "2146J", "damage": 0,  "ce_cost": 50, "startup": 20,"active": 0, "recovery": 15, "hitstun": 0,  "kb_x": 0,  "kb_y": 0,  "type": "buff",   "range": 0,  "buff": "next_black_flash"},
        },
        "supers": {
            "divine_combo": {"input": "236236J","ce_cost": 100,"damage": 250,"startup": 15,"active": 30,"recovery": 30,"type": "super","vfx": "yuji_super"}
        }
    },
    "gojo": {
        "name": "Satoru Gojo",
        "title": "The Strongest",
        "archetype": "zoner",
        "hp": 900, "ce_max": 200, "speed": 4.5, "jump_power": -12,
        "color": (30, 100, 255),
        "unlock_cost": 300,
        "description": "Master of Infinity. Controls space with Blue and Red. Near-invincible with Infinity barrier.",
        "moves": {
            "palm":         {"input": "J",     "damage": 20, "ce_cost": 0,  "startup": 5, "active": 3, "recovery": 8,  "hitstun": 10, "kb_x": 3,  "kb_y": 0,  "type": "light",  "range": 45},
            "blue_orb":     {"input": "236J",  "damage": 55, "ce_cost": 25, "startup": 12,"active": 20,"recovery": 15, "hitstun": 18, "kb_x": -8, "kb_y": 0,  "type": "special", "range": 300, "projectile": True, "vfx": "blue_orb", "pull": True},
            "blue_pull":    {"input": "236K",  "damage": 40, "ce_cost": 30, "startup": 8, "active": 10,"recovery": 14, "hitstun": 15, "kb_x": -12,"kb_y": 0,  "type": "special", "range": 250, "vfx": "blue_pull"},
            "red_repulse":  {"input": "214J",  "damage": 70, "ce_cost": 35, "startup": 15,"active": 5, "recovery": 18, "hitstun": 22, "kb_x": 15, "kb_y": -5, "type": "special", "range": 120, "vfx": "red_repulse"},
            "lapser_blue":  {"input": "22K",   "damage": 65, "ce_cost": 40, "startup": 18,"active": 40,"recovery": 20, "hitstun": 16, "kb_x": 2,  "kb_y": 0,  "type": "special", "range": 100, "trap": True, "vfx": "lapser_blue"},
            "hollow_purple":{"input": "236236J","damage": 180,"ce_cost": 60, "startup": 25,"active": 15,"recovery": 30, "hitstun": 35, "kb_x": 20, "kb_y": -8, "type": "super",   "range": 400, "vfx": "hollow_purple"},
        },
        "supers": {
            "unlimited_void":{"input": "222J",  "ce_cost": 100,"damage": 0,  "startup": 45,"active": 300,"recovery": 30,"type": "domain","vfx": "unlimited_void","effect": "stun_5s"}
        },
        "passive": {"name": "Infinity", "effect": "auto_block_when_ce_above_50"}
    },
    "sukuna": {
        "name": "Ryomen Sukuna",
        "title": "King of Curses",
        "archetype": "glass_cannon",
        "hp": 850, "ce_max": 150, "speed": 6, "jump_power": -13,
        "color": (255, 50, 50),
        "unlock_cost": 500,
        "description": "Overwhelming offense. Dismantle and Cleave cut through everything. True power of the King of Curses.",
        "moves": {
            "claw":         {"input": "J",     "damage": 28, "ce_cost": 0,  "startup": 4, "active": 3, "recovery": 7,  "hitstun": 11, "kb_x": 3,  "kb_y": 0,  "type": "light",  "range": 50},
            "dismantle":    {"input": "236J",  "damage": 45, "ce_cost": 15, "startup": 6, "active": 8, "recovery": 12, "hitstun": 16, "kb_x": 8,  "kb_y": -2, "type": "special", "range": 200, "projectile": True, "vfx": "dismantle"},
            "cleave":       {"input": "236K",  "damage": 65, "ce_cost": 25, "startup": 10,"active": 6, "recovery": 16, "hitstun": 20, "kb_x": 10, "kb_y": -4, "type": "special", "range": 100, "vfx": "cleave"},
            "fire_arrow":   {"input": "214J",  "damage": 80, "ce_cost": 35, "startup": 16,"active": 10,"recovery": 22, "hitstun": 25, "kb_x": 12, "kb_y": -6, "type": "special", "range": 250, "projectile": True, "vfx": "fire_arrow"},
            "spiderweb":    {"input": "22J",   "damage": 30, "ce_cost": 20, "startup": 8, "active": 60,"recovery": 15, "hitstun": 30, "kb_x": 0,  "kb_y": 0,  "type": "trap",   "range": 150, "trap": True, "vfx": "spiderweb"},
            "rev_cursed":   {"input": "214K",  "damage": 0,  "ce_cost": 40, "startup": 20,"active": 0, "recovery": 15, "hitstun": 0,  "kb_x": 0,  "kb_y": 0,  "type": "heal",   "range": 0,  "heal": 80, "vfx": "rev_cursed"},
            "world_slash":  {"input": "236236K","damage": 130,"ce_cost": 50, "startup": 12,"active": 4, "recovery": 25, "hitstun": 28, "kb_x": 18, "kb_y": -8, "type": "super",   "range": 350, "vfx": "world_slash"},
        },
        "supers": {
            "malevolent_shrine":{"input": "222K","ce_cost": 100,"damage": 200,"startup": 50,"active": 360,"recovery": 30,"type": "domain","vfx": "malevolent_shrine","effect": "continuous_damage"}
        }
    },
    "megumi": {
        "name": "Megumi Fushiguro",
        "title": "The Ten Shadows User",
        "archetype": "setplay",
        "hp": 950, "ce_max": 120, "speed": 5, "jump_power": -12,
        "color": (180, 50, 255),
        "unlock_cost": 200,
        "description": "Summon shikigami to fight alongside him. Controls space with shadows and summons.",
        "moves": {
            "shadow_stab":  {"input": "J",     "damage": 25, "ce_cost": 0,  "startup": 5, "active": 3, "recovery": 9,  "hitstun": 12, "kb_x": 3,  "kb_y": 0,  "type": "light",  "range": 55},
            "divine_dogs":  {"input": "236J",  "damage": 40, "ce_cost": 20, "startup": 15,"active": 30,"recovery": 12, "hitstun": 14, "kb_x": 5,  "kb_y": -2, "type": "special", "range": 200, "summon": True, "vfx": "shadow_dogs"},
            "nue_lightning":{"input": "236K",  "damage": 65, "ce_cost": 30, "startup": 18,"active": 8, "recovery": 16, "hitstun": 20, "kb_x": 6,  "kb_y": -8, "type": "special", "range": 150, "vfx": "nue_lightning"},
            "toad_tongue":  {"input": "214J",  "damage": 20, "ce_cost": 15, "startup": 10,"active": 12,"recovery": 14, "hitstun": 25, "kb_x": -15,"kb_y": 0,  "type": "special", "range": 180, "pull": True, "vfx": "toad"},
            "rabbit_escape":{"input": "214K",  "damage": 0,  "ce_cost": 10, "startup": 4, "active": 15,"recovery": 8,  "hitstun": 0,  "kb_x": 0,  "kb_y": 0,  "type": "special", "range": 0,  "invincible": True, "vfx": "rabbits"},
            "max_elephant": {"input": "22J",   "damage": 90, "ce_cost": 45, "startup": 20,"active": 10,"recovery": 22, "hitstun": 25, "kb_x": 12, "kb_y": -5, "type": "special", "range": 250, "projectile": True, "vfx": "water_cannon"},
            "chimera_pool": {"input": "236236J","damage": 50, "ce_cost": 35, "startup": 14,"active": 60,"recovery": 18, "hitstun": 16, "kb_x": 5,  "kb_y": -3, "type": "super",   "range": 300, "trap": True, "vfx": "chimera_shadow"},
        },
        "supers": {
            "shadow_garden": {"input": "222J", "ce_cost": 100,"damage": 150,"startup": 45,"active": 300,"recovery": 30,"type": "domain","vfx": "shadow_garden","effect": "shikigami_boost"}
        }
    },
    "nobara": {
        "name": "Nobara Kugisaki",
        "title": "The Straw Doll User",
        "archetype": "technical",
        "hp": 900, "ce_max": 100, "speed": 5, "jump_power": -12,
        "color": (255, 100, 150),
        "unlock_cost": 250,
        "description": "Controls space with nails and straw dolls. Resonance damages through any defense.",
        "moves": {
            "hammer":       {"input": "J",     "damage": 30, "ce_cost": 0,  "startup": 6, "active": 4, "recovery": 10, "hitstun": 14, "kb_x": 4,  "kb_y": -2, "type": "light",  "range": 50},
            "nail_shot":    {"input": "236J",  "damage": 25, "ce_cost": 10, "startup": 8, "active": 12,"recovery": 10, "hitstun": 10, "kb_x": 3,  "kb_y": 0,  "type": "special", "range": 200, "projectile": True, "rapid": 3, "vfx": "nail"},
            "straw_doll":   {"input": "236K",  "damage": 0,  "ce_cost": 20, "startup": 12,"active": 180,"recovery": 15,"hitstun": 0,  "kb_x": 0,  "kb_y": 0,  "type": "trap",   "range": 120, "trap": True, "vfx": "straw_doll"},
            "resonance":    {"input": "214J",  "damage": 70, "ce_cost": 25, "startup": 10,"active": 5, "recovery": 18, "hitstun": 22, "kb_x": 8,  "kb_y": -3, "type": "special", "range": 999, "vfx": "resonance", "require_trap": True},
            "hairpin":      {"input": "22J",   "damage": 55, "ce_cost": 30, "startup": 8, "active": 6, "recovery": 16, "hitstun": 18, "kb_x": 10, "kb_y": -5, "type": "special", "range": 150, "vfx": "hairpin", "explode_nails": True},
            "black_flash_n":{"input": "236236J","damage": 100,"ce_cost": 35, "startup": 10,"active": 4, "recovery": 22, "hitstun": 28, "kb_x": 14, "kb_y": -8, "type": "super",   "range": 70, "vfx": "black_flash"},
        },
        "supers": {
            "hairpin_star": {"input": "222J",  "ce_cost": 100,"damage": 160,"startup": 30,"active": 20,"recovery": 25,"type": "domain-lite","vfx": "hairpin_star","effect": "explode_all"}
        }
    },
    "nanami": {
        "name": "Kento Nanami",
        "title": "The Ratio User",
        "archetype": "precision",
        "hp": 1000, "ce_max": 80, "speed": 4.5, "jump_power": -11,
        "color": (200, 180, 100),
        "unlock_cost": 200,
        "description": "Precision striker. Ratio Technique finds weak points for critical damage. Overtime boosts late-game.",
        "moves": {
            "slash":        {"input": "J",     "damage": 28, "ce_cost": 0,  "startup": 5, "active": 3, "recovery": 9,  "hitstun": 12, "kb_x": 3,  "kb_y": 0,  "type": "light",  "range": 55},
            "collapsing":   {"input": "236J",  "damage": 50, "ce_cost": 15, "startup": 8, "active": 4, "recovery": 14, "hitstun": 18, "kb_x": 8,  "kb_y": -3, "type": "special", "range": 70, "vfx": "ratio_line", "crit_boost": True},
            "blade_rush":   {"input": "236K",  "damage": 60, "ce_cost": 25, "startup": 10,"active": 8, "recovery": 16, "hitstun": 20, "kb_x": 10, "kb_y": -4, "type": "special", "range": 90, "multihit": 3, "vfx": "blade_rush"},
            "decisive":     {"input": "22J",   "damage": 95, "ce_cost": 35, "startup": 12,"active": 3, "recovery": 20, "hitstun": 26, "kb_x": 12, "kb_y": -6, "type": "special", "range": 65, "guarantee_crit": True, "vfx": "decisive"},
        },
        "supers": {
            "ratio_collapse":{"input": "236236J","ce_cost": 100,"damage": 170,"startup": 15,"active": 5, "recovery": 28,"type": "super","vfx": "ratio_collapse"}
        },
        "passive": {"name": "Overtime", "effect": "damage_boost_after_60s", "boost": 1.2},
        "passive2": {"name": "Revealing One's Hand", "effect": "announce_technique_damage_boost", "boost": 1.15}
    },
    "inumaki": {
        "name": "Toge Inumaki",
        "title": "The Cursed Speech User",
        "archetype": "gimmick",
        "hp": 850, "ce_max": 130, "speed": 4.5, "jump_power": -11,
        "color": (100, 200, 150),
        "unlock_cost": 350,
        "description": "Cursed Speech commands are powerful but damage the user. High risk, high reward.",
        "moves": {
            "headbutt":     {"input": "J",     "damage": 20, "ce_cost": 0,  "startup": 5, "active": 3, "recovery": 8,  "hitstun": 10, "kb_x": 3,  "kb_y": 0,  "type": "light",  "range": 40},
            "dont_move":    {"input": "236J",  "damage": 0,  "ce_cost": 25, "startup": 8, "active": 120,"recovery": 20,"hitstun": 120,"kb_x": 0,  "kb_y": 0,  "type": "special", "range": 200, "effect": "freeze", "self_damage": 50, "vfx": "speech_freeze"},
            "get_crushed":  {"input": "236K",  "damage": 80, "ce_cost": 35, "startup": 10,"active": 8, "recovery": 22, "hitstun": 24, "kb_x": 5,  "kb_y": 10, "type": "special", "range": 150, "self_damage": 80, "vfx": "speech_crush"},
            "blast_away":   {"input": "214J",  "damage": 60, "ce_cost": 30, "startup": 8, "active": 6, "recovery": 18, "hitstun": 20, "kb_x": 18, "kb_y": -5, "type": "special", "range": 180, "self_damage": 60, "vfx": "speech_blast"},
            "explode":      {"input": "22J",   "damage": 110,"ce_cost": 50, "startup": 12,"active": 8, "recovery": 25, "hitstun": 28, "kb_x": 12, "kb_y": -8, "type": "special", "range": 130, "self_damage": 120,"vfx": "speech_explode"},
            "run":          {"input": "214K",  "damage": 0,  "ce_cost": 20, "startup": 10,"active": 180,"recovery": 10,"hitstun": 0,  "kb_x": 0,  "kb_y": 0,  "type": "buff",   "range": 0,  "buff": "speed_boost", "vfx": "speech_run"},
        },
        "supers": {
            "die":          {"input": "222J",  "ce_cost": 100,"damage": 200,"startup": 15,"active": 10,"recovery": 30,"type": "super","range": 200,"self_damage": 200,"vfx": "speech_die"}
        }
    },
    "todo": {
        "name": "Aoi Todo",
        "title": "The 530,000 IQ Fighter",
        "archetype": "grappler",
        "hp": 1100, "ce_max": 90, "speed": 4, "jump_power": -14,
        "color": (80, 80, 80),
        "unlock_cost": 300,
        "description": "Grappler with Boogie Woogie position swap. Best friend combo summons imaginary Yuji.",
        "moves": {
            "haymaker":     {"input": "J",     "damage": 35, "ce_cost": 0,  "startup": 7, "active": 4, "recovery": 10, "hitstun": 15, "kb_x": 5,  "kb_y": -2, "type": "light",  "range": 55},
            "boogie_woogie":{"input": "214J",  "damage": 0,  "ce_cost": 20, "startup": 6, "active": 0, "recovery": 12, "hitstun": 0,  "kb_x": 0,  "kb_y": 0,  "type": "special", "range": 0,  "effect": "swap_positions", "vfx": "boogie_woogie"},
            "friend_combo": {"input": "236K",  "damage": 70, "ce_cost": 25, "startup": 12,"active": 10,"recovery": 16, "hitstun": 20, "kb_x": 8,  "kb_y": -5, "type": "special", "range": 80, "vfx": "imaginary_yuji"},
            "shoulder_throw":{"input": "214K", "damage": 55, "ce_cost": 15, "startup": 5, "active": 4, "recovery": 18, "hitstun": 25, "kb_x": 10, "kb_y": -10,"type": "command_grab","range": 45},
            "black_flash_t":{"input": "22J",   "damage": 110,"ce_cost": 35, "startup": 8, "active": 3, "recovery": 22, "hitstun": 28, "kb_x": 14, "kb_y": -8, "type": "special", "range": 60, "vfx": "black_flash"},
            "analyze":      {"input": "236J",  "damage": 0,  "ce_cost": 0,  "startup": 30,"active": 0, "recovery": 10, "hitstun": 0,  "kb_x": 0,  "kb_y": 0,  "type": "buff",   "range": 0,  "effect": "reveal_moves"},
        },
        "supers": {
            "solo_stance":  {"input": "236236K","ce_cost": 100,"damage": 180,"startup": 10,"active": 600,"recovery": 20,"type": "super","vfx": "todo_buff","effect": "damage_boost_10s"}
        }
    },
    "mahito": {
        "name": "Mahito",
        "title": "The Curse of Humanity",
        "archetype": "shapeshifter",
        "hp": 950, "ce_max": 130, "speed": 5, "jump_power": -12,
        "color": (150, 150, 200),
        "unlock_cost": 400,
        "description": "Idle Transfiguration reshapes souls. Unique transformation mechanics.",
        "moves": {
            "soul_strike":  {"input": "J",     "damage": 30, "ce_cost": 0,  "startup": 5, "active": 4, "recovery": 9,  "hitstun": 13, "kb_x": 4,  "kb_y": 0,  "type": "light",  "range": 55},
            "transfig":     {"input": "236J",  "damage": 60, "ce_cost": 25, "startup": 12,"active": 5, "recovery": 18, "hitstun": 22, "kb_x": 8,  "kb_y": -3, "type": "special", "range": 65, "vfx": "transfiguration"},
            "body_repel":   {"input": "214J",  "damage": 45, "ce_cost": 20, "startup": 8, "active": 10,"recovery": 14, "hitstun": 16, "kb_x": 10, "kb_y": -4, "type": "special", "range": 80, "armor": True, "vfx": "body_repel"},
            "polymorphic":  {"input": "236K",  "damage": 0,  "ce_cost": 30, "startup": 15,"active": 480,"recovery": 10,"hitstun": 0,  "kb_x": 0,  "kb_y": 0,  "type": "buff",   "range": 0,  "buff": "transform", "vfx": "transform"},
            "triple_arms":  {"input": "22J",   "damage": 85, "ce_cost": 35, "startup": 14,"active": 8, "recovery": 20, "hitstun": 24, "kb_x": 12, "kb_y": -5, "type": "special", "range": 75, "multihit": 3, "vfx": "triple_arm"},
            "instant_spirit":{"input": "214K", "damage": 75, "ce_cost": 40, "startup": 6, "active": 8, "recovery": 18, "hitstun": 20, "kb_x": 8,  "kb_y": -6, "type": "special", "range": 70, "invincible_startup": True, "vfx": "spirit_body"},
        },
        "supers": {
            "true_form":    {"input": "222J",  "ce_cost": 100,"damage": 160,"startup": 40,"active": 300,"recovery": 25,"type": "domain","vfx": "true_form","effect": "transfigure_area"}
        }
    },
    "jogo": {
        "name": "Jogo",
        "title": "The Volcanic Curse",
        "archetype": "zoner",
        "hp": 800, "ce_max": 160, "speed": 5.5, "jump_power": -12,
        "color": (255, 80, 20),
        "unlock_cost": 450,
        "description": "Fire-based zoner. Meteor and ember insects control the screen.",
        "moves": {
            "ember":        {"input": "J",     "damage": 15, "ce_cost": 0,  "startup": 4, "active": 3, "recovery": 7,  "hitstun": 8,  "kb_x": 2,  "kb_y": 0,  "type": "light",  "range": 40},
            "volcano_blast":{"input": "236J",  "damage": 75, "ce_cost": 30, "startup": 14,"active": 8, "recovery": 20, "hitstun": 22, "kb_x": 10, "kb_y": -5, "type": "special", "range": 280, "projectile": True, "vfx": "volcano"},
            "ember_swarm":  {"input": "236K",  "damage": 40, "ce_cost": 25, "startup": 10,"active": 40,"recovery": 14, "hitstun": 12, "kb_x": 3,  "kb_y": -2, "type": "special", "range": 200, "tracking": True, "vfx": "ember_swarm"},
            "meteor":       {"input": "22J",   "damage": 130,"ce_cost": 50, "startup": 25,"active": 10,"recovery": 30, "hitstun": 35, "kb_x": 15, "kb_y": -10,"type": "special", "range": 200, "vfx": "meteor"},
            "heat_aura":    {"input": "214J",  "damage": 25, "ce_cost": 20, "startup": 8, "active": 120,"recovery": 12,"hitstun": 10, "kb_x": 3,  "kb_y": 0,  "type": "special", "range": 80,  "aura": True, "vfx": "heat_aura"},
        },
        "supers": {
            "iron_mountain":{"input": "222J",  "ce_cost": 100,"damage": 190,"startup": 45,"active": 300,"recovery": 30,"type": "domain","vfx": "iron_mountain","effect": "volcanic_hell"}
        }
    },
    "hanami": {
        "name": "Hanami",
        "title": "The Nature Curse",
        "archetype": "tank",
        "hp": 1200, "ce_max": 110, "speed": 3.5, "jump_power": -10,
        "color": (80, 160, 80),
        "unlock_cost": 400,
        "description": "Tanky curse with nature attacks. Thorns armor and root control.",
        "moves": {
            "root_slam":    {"input": "J",     "damage": 35, "ce_cost": 0,  "startup": 8, "active": 5, "recovery": 12, "hitstun": 16, "kb_x": 5,  "kb_y": -2, "type": "light",  "range": 60},
            "cursed_bud":   {"input": "236J",  "damage": 45, "ce_cost": 20, "startup": 14,"active": 30,"recovery": 12, "hitstun": 14, "kb_x": 4,  "kb_y": -1, "type": "special", "range": 250, "homing": True, "vfx": "cursed_bud"},
            "roots":        {"input": "214J",  "damage": 50, "ce_cost": 25, "startup": 10,"active": 8, "recovery": 16, "hitstun": 20, "kb_x": 3,  "kb_y": 0,  "type": "special", "range": 150, "low": True, "vfx": "roots"},
            "flower_beam":  {"input": "236K",  "damage": 80, "ce_cost": 35, "startup": 16,"active": 10,"recovery": 22, "hitstun": 24, "kb_x": 12, "kb_y": -6, "type": "special", "range": 300, "projectile": True, "vfx": "flower_beam"},
            "wooden_wall":  {"input": "214K",  "damage": 0,  "ce_cost": 20, "startup": 8, "active": 60,"recovery": 10, "hitstun": 0,  "kb_x": 0,  "kb_y": 0,  "type": "special", "range": 0,  "wall": True, "vfx": "wood_wall"},
            "thorn_armor":  {"input": "22J",   "damage": 0,  "ce_cost": 30, "startup": 10,"active": 360,"recovery": 10,"hitstun": 0,  "kb_x": 0,  "kb_y": 0,  "type": "buff",   "range": 0,  "buff": "defense_boost", "vfx": "thorns"},
        },
        "supers": {
            "sea_of_trees": {"input": "222J",  "ce_cost": 100,"damage": 150,"startup": 45,"active": 300,"recovery": 30,"type": "domain","vfx": "sea_of_trees","effect": "nature_absorb"}
        }
    },
    "choso": {
        "name": "Choso",
        "title": "Blood Manipulation User",
        "archetype": "technical",
        "hp": 900, "ce_max": 120, "speed": 5.5, "jump_power": -12,
        "color": (180, 30, 30),
        "unlock_cost": 350,
        "description": "Blood manipulation specialist. Convergence builds power for devastating blood attacks.",
        "moves": {
            "blood_cut":    {"input": "J",     "damage": 28, "ce_cost": 0,  "startup": 5, "active": 3, "recovery": 9,  "hitstun": 12, "kb_x": 3,  "kb_y": 0,  "type": "light",  "range": 55},
            "convergence":  {"input": "236J",  "damage": 0,  "ce_cost": 15, "startup": 15,"active": 0, "recovery": 10, "hitstun": 0,  "kb_x": 0,  "kb_y": 0,  "type": "charge",  "range": 0,  "max_charge": 3, "vfx": "convergence"},
            "piercing_blood":{"input": "236K", "damage": 85, "ce_cost": 35, "startup": 10,"active": 8, "recovery": 18, "hitstun": 22, "kb_x": 12, "kb_y": -4, "type": "special", "range": 350, "projectile": True, "require_charge": 1, "vfx": "piercing_blood"},
            "supernova":    {"input": "22K",   "damage": 120,"ce_cost": 55, "startup": 16,"active": 10,"recovery": 25, "hitstun": 30, "kb_x": 15, "kb_y": -8, "type": "special", "range": 150, "require_charge": 2, "vfx": "supernova"},
            "blood_edge":   {"input": "214J",  "damage": 50, "ce_cost": 20, "startup": 8, "active": 15,"recovery": 12, "hitstun": 14, "kb_x": 6,  "kb_y": -2, "type": "special", "range": 200, "projectile": True, "vfx": "blood_disc"},
            "flowing_red":  {"input": "214K",  "damage": 0,  "ce_cost": 25, "startup": 12,"active": 480,"recovery": 10,"hitstun": 0,  "kb_x": 0,  "kb_y": 0,  "type": "buff",   "range": 0,  "buff": "speed_damage", "vfx": "flowing_red"},
        },
        "supers": {
            "blood_meteor": {"input": "222J",  "ce_cost": 100,"damage": 175,"startup": 20,"active": 15,"recovery": 28,"type": "super","range": 300,"require_charge": 3,"vfx": "blood_meteor"}
        }
    },
}

# Story boss variants (extra HP, different behavior)
BOSS_OVERRIDES = {
    "mahito_phase2": {"hp": 1500, "speed_boost": 1.2, "damage_boost": 1.3, "color": (200, 100, 200)},
    "sukuna_15f": {"hp": 2000, "ce_max": 300, "damage_boost": 1.5, "color": (255, 30, 30)},
    "kenjaku": {"hp": 1800, "ce_max": 250, "damage_boost": 1.4, "color": (50, 50, 50)},
    "kashimo": {"hp": 1400, "ce_max": 200, "damage_boost": 1.3, "color": (255, 255, 100)},
}

# AI character preferences
AI_PREFERENCES = {
    "yuji": {"aggression": 0.8, "special_use": 0.3, "block_chance": 0.3, "preferred_range": "close"},
    "gojo": {"aggression": 0.4, "special_use": 0.6, "block_chance": 0.6, "preferred_range": "far"},
    "sukuna": {"aggression": 0.9, "special_use": 0.5, "block_chance": 0.2, "preferred_range": "mid"},
    "megumi": {"aggression": 0.5, "special_use": 0.7, "block_chance": 0.4, "preferred_range": "mid"},
    "nobara": {"aggression": 0.5, "special_use": 0.5, "block_chance": 0.4, "preferred_range": "mid"},
    "nanami": {"aggression": 0.6, "special_use": 0.4, "block_chance": 0.5, "preferred_range": "close"},
    "inumaki": {"aggression": 0.3, "special_use": 0.8, "block_chance": 0.5, "preferred_range": "far"},
    "todo": {"aggression": 0.7, "special_use": 0.4, "block_chance": 0.5, "preferred_range": "close"},
    "mahito": {"aggression": 0.7, "special_use": 0.5, "block_chance": 0.3, "preferred_range": "mid"},
    "jogo": {"aggression": 0.5, "special_use": 0.7, "block_chance": 0.3, "preferred_range": "far"},
    "hanami": {"aggression": 0.3, "special_use": 0.5, "block_chance": 0.7, "preferred_range": "mid"},
    "choso": {"aggression": 0.6, "special_use": 0.6, "block_chance": 0.4, "preferred_range": "mid"},
}

def get_character(char_id):
    return CHARACTERS.get(char_id)

def get_all_character_ids():
    return list(CHARACTERS.keys())

def get_base_characters():
    return ["yuji", "gojo", "sukuna", "megumi"]

def get_unlockable_characters():
    base = get_base_characters()
    return [c for c in CHARACTERS if c not in base]
