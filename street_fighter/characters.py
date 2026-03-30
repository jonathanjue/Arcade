"""
Street Fighter Style Game - Character Definitions
6 unique characters with distinct movesets, stats, and visual styles.
"""

from typing import Any


def make_move(
    move_type: str = "strike",
    damage: int = 10,
    startup: int = 5,
    active: int = 3,
    recovery: int = 10,
    knockback_x: float = 3.0,
    knockback_y: float = 0.0,
    ce_cost: int = 0,
    hit_range: int = 50,
    input_desc: str = "",
    projectile: bool = False,
    proj_speed: float = 0.0,
    proj_lifetime: int = 0,
    grab_range: int = 0,
    armor: bool = False,
    invuln_startup: int = 0,
    hitstun: int = 0,
    blockstun: int = 0,
) -> dict[str, Any]:
    """Helper to create a move dictionary with consistent structure."""
    return {
        "type": move_type,
        "damage": damage,
        "startup": startup,
        "active": active,
        "recovery": recovery,
        "knockback_x": knockback_x,
        "knockback_y": knockback_y,
        "ce_cost": ce_cost,
        "range": hit_range,
        "input": input_desc,
        "projectile": projectile,
        "proj_speed": proj_speed,
        "proj_lifetime": proj_lifetime,
        "grab_range": grab_range,
        "armor": armor,
        "invuln_startup": invuln_startup,
        "hitstun": hitstun,
        "blockstun": blockstun,
    }


# ---------------------------------------------------------------------------
# Character Definitions
# ---------------------------------------------------------------------------

CHARACTERS: dict[str, dict[str, Any]] = {}


# ===== RYU - Balanced Karate Fighter =====
CHARACTERS["RYU"] = {
    "name": "RYU",
    "title": "The Wandering Warrior",
    "color": (255, 255, 255),        # gi white
    "body_color": (210, 180, 140),   # skin tan
    "hair_color": (139, 69, 19),     # brown hair
    "accent_color": (200, 50, 50),   # headband red
    "outline_color": (40, 40, 40),
    "speed": 5.0,
    "jump_power": -12.0,
    "max_hp": 1000,
    "weight": 1.0,
    "width": 48,
    "height": 88,
    "walk_anim_frames": 4,
    "moves": {
        # -- Normals --
        "light": make_move(
            damage=30, startup=4, active=3, recovery=6,
            knockback_x=2.0, knockback_y=0.0,
            hit_range=55, input_desc="LP",
            hitstun=12, blockstun=8,
        ),
        "heavy": make_move(
            damage=70, startup=8, active=4, recovery=14,
            knockback_x=5.0, knockback_y=-1.5,
            hit_range=65, input_desc="HP",
            hitstun=18, blockstun=12,
        ),
        "crouch_light": make_move(
            damage=25, startup=3, active=3, recovery=7,
            knockback_x=1.5, knockback_y=0.0,
            hit_range=50, input_desc="D+LP",
            hitstun=11, blockstun=7,
        ),
        "crouch_heavy": make_move(
            damage=65, startup=7, active=5, recovery=16,
            knockback_x=4.0, knockback_y=-2.0,
            hit_range=60, input_desc="D+HP",
            hitstun=17, blockstun=12,
        ),
        "jump_light": make_move(
            damage=35, startup=5, active=5, recovery=4,
            knockback_x=2.0, knockback_y=3.0,
            hit_range=55, input_desc="LP (air)",
            hitstun=14, blockstun=9,
        ),
        "jump_heavy": make_move(
            damage=80, startup=7, active=6, recovery=6,
            knockback_x=3.0, knockback_y=5.0,
            hit_range=65, input_desc="HP (air)",
            hitstun=18, blockstun=12,
        ),
        # -- Specials (CE cost 20-30) --
        "special_1": make_move(
            move_type="projectile", damage=60, startup=10, active=30, recovery=16,
            knockback_x=4.0, knockback_y=0.0,
            ce_cost=25, hit_range=0, input_desc="QCF+P (Hadoken)",
            projectile=True, proj_speed=7.0, proj_lifetime=60,
            hitstun=16, blockstun=10,
        ),
        "special_2": make_move(
            move_type="strike", damage=100, startup=5, active=8, recovery=22,
            knockback_x=6.0, knockback_y=-4.0,
            ce_cost=20, hit_range=60, input_desc="DP+P (Shoryuken)",
            invuln_startup=4, hitstun=22, blockstun=14,
        ),
        "special_3": make_move(
            move_type="strike", damage=50, startup=9, active=12, recovery=14,
            knockback_x=3.0, knockback_y=0.0,
            ce_cost=20, hit_range=55, input_desc="QCB+K (Tatsumaki)",
            hitstun=15, blockstun=10,
        ),
        "special_4": make_move(
            move_type="strike", damage=45, startup=12, active=6, recovery=15,
            knockback_x=2.0, knockback_y=-3.0,
            ce_cost=20, hit_range=70, input_desc="QCF+K (Axe Kick)",
            hitstun=16, blockstun=10,
        ),
        # -- Super (CE cost 50-80) --
        "super": make_move(
            move_type="projectile", damage=250, startup=8, active=40, recovery=24,
            knockback_x=10.0, knockback_y=-5.0,
            ce_cost=60, hit_range=0, input_desc="QCF,QCF+P (Shinku Hadoken)",
            projectile=True, proj_speed=9.0, proj_lifetime=80,
            invuln_startup=6, hitstun=28, blockstun=18,
        ),
    },
    "ai_preferences": {
        "aggression": 0.5,
        "zoning": 0.5,
        "grapple_tendency": 0.1,
        "special_usage": 0.4,
        "super_threshold": 0.3,
        "preferred_range": "mid",
        "combo_tendency": 0.5,
    },
}


# ===== BLAZE - Fast Boxer =====
CHARACTERS["BLAZE"] = {
    "name": "BLAZE",
    "title": "The Crimson Fist",
    "color": (220, 30, 30),           # red gloves/shorts
    "body_color": (160, 100, 60),     # darker skin
    "hair_color": (20, 20, 20),       # black hair
    "accent_color": (255, 200, 0),    # gold trim
    "outline_color": (60, 20, 20),
    "speed": 7.0,
    "jump_power": -11.5,
    "max_hp": 850,
    "weight": 0.85,
    "width": 44,
    "height": 84,
    "walk_anim_frames": 4,
    "moves": {
        # -- Normals --
        "light": make_move(
            damage=25, startup=3, active=2, recovery=5,
            knockback_x=1.5, knockback_y=0.0,
            hit_range=50, input_desc="LP",
            hitstun=10, blockstun=7,
        ),
        "heavy": make_move(
            damage=60, startup=6, active=3, recovery=12,
            knockback_x=5.0, knockback_y=-1.0,
            hit_range=58, input_desc="HP",
            hitstun=16, blockstun=11,
        ),
        "crouch_light": make_move(
            damage=20, startup=3, active=2, recovery=6,
            knockback_x=1.0, knockback_y=0.0,
            hit_range=48, input_desc="D+LP",
            hitstun=10, blockstun=6,
        ),
        "crouch_heavy": make_move(
            damage=55, startup=6, active=4, recovery=14,
            knockback_x=4.0, knockback_y=-1.5,
            hit_range=55, input_desc="D+HP",
            hitstun=15, blockstun=11,
        ),
        "jump_light": make_move(
            damage=30, startup=4, active=4, recovery=3,
            knockback_x=2.0, knockback_y=2.5,
            hit_range=50, input_desc="LP (air)",
            hitstun=12, blockstun=8,
        ),
        "jump_heavy": make_move(
            damage=70, startup=6, active=5, recovery=5,
            knockback_x=3.0, knockback_y=4.5,
            hit_range=60, input_desc="HP (air)",
            hitstun=16, blockstun=11,
        ),
        # -- Specials --
        "special_1": make_move(
            move_type="strike", damage=40, startup=4, active=4, recovery=10,
            knockback_x=3.0, knockback_y=0.0,
            ce_cost=20, hit_range=55, input_desc="QCF+P (Flurry Rush)",
            hitstun=12, blockstun=8,
        ),
        "special_2": make_move(
            move_type="strike", damage=90, startup=14, active=3, recovery=18,
            knockback_x=8.0, knockback_y=-2.0,
            ce_cost=25, hit_range=50, input_desc="B,F+P (Thunder Hook)",
            hitstun=20, blockstun=14,
        ),
        "special_3": make_move(
            move_type="strike", damage=35, startup=6, active=6, recovery=10,
            knockback_x=2.0, knockback_y=0.0,
            ce_cost=20, hit_range=52, input_desc="DP+P (Uppercut Blaze)",
            invuln_startup=3, hitstun=14, blockstun=9,
        ),
        "special_4": make_move(
            move_type="strike", damage=50, startup=8, active=8, recovery=12,
            knockback_x=4.0, knockback_y=0.0,
            ce_cost=20, hit_range=48, input_desc="QCB+P (Rapid Jab Combo)",
            hitstun=14, blockstun=9,
        ),
        # -- Super --
        "super": make_move(
            move_type="strike", damage=280, startup=6, active=12, recovery=26,
            knockback_x=12.0, knockback_y=-6.0,
            ce_cost=60, hit_range=65, input_desc="QCF,QCF+P (Blazing Barrage)",
            invuln_startup=5, hitstun=30, blockstun=20,
        ),
    },
    "ai_preferences": {
        "aggression": 0.85,
        "zoning": 0.1,
        "grapple_tendency": 0.05,
        "special_usage": 0.5,
        "super_threshold": 0.4,
        "preferred_range": "close",
        "combo_tendency": 0.7,
    },
}


# ===== TITAN - Slow Heavy Grappler =====
CHARACTERS["TITAN"] = {
    "name": "TITAN",
    "title": "The Unstoppable Mountain",
    "color": (80, 80, 120),           # dark indigo
    "body_color": (230, 200, 170),    # pale skin
    "hair_color": (100, 100, 100),    # grey hair
    "accent_color": (180, 140, 80),   # leather straps
    "outline_color": (30, 30, 60),
    "speed": 3.0,
    "jump_power": -10.0,
    "max_hp": 1300,
    "weight": 1.5,
    "width": 60,
    "height": 96,
    "walk_anim_frames": 4,
    "moves": {
        # -- Normals --
        "light": make_move(
            damage=35, startup=7, active=4, recovery=10,
            knockback_x=3.0, knockback_y=0.0,
            hit_range=55, input_desc="LP",
            hitstun=14, blockstun=10,
        ),
        "heavy": make_move(
            damage=95, startup=14, active=6, recovery=20,
            knockback_x=7.0, knockback_y=-2.0,
            hit_range=70, input_desc="HP",
            hitstun=22, blockstun=16,
        ),
        "crouch_light": make_move(
            damage=30, startup=6, active=4, recovery=10,
            knockback_x=2.0, knockback_y=0.0,
            hit_range=60, input_desc="D+LP",
            hitstun=13, blockstun=9,
        ),
        "crouch_heavy": make_move(
            damage=90, startup=12, active=6, recovery=22,
            knockback_x=6.0, knockback_y=-3.0,
            hit_range=75, input_desc="D+HP",
            hitstun=22, blockstun=16,
        ),
        "jump_light": make_move(
            damage=40, startup=8, active=6, recovery=6,
            knockback_x=3.0, knockback_y=3.0,
            hit_range=60, input_desc="LP (air)",
            hitstun=16, blockstun=11,
        ),
        "jump_heavy": make_move(
            damage=110, startup=12, active=8, recovery=8,
            knockback_x=4.0, knockback_y=6.0,
            hit_range=75, input_desc="HP (air)",
            hitstun=22, blockstun=16,
        ),
        # -- Specials --
        "special_1": make_move(
            move_type="grab", damage=120, startup=5, active=3, recovery=22,
            knockback_x=3.0, knockback_y=-4.0,
            ce_cost=25, hit_range=0, input_desc="HCB+P (Titan Crush)",
            grab_range=60, hitstun=24, blockstun=0,
        ),
        "special_2": make_move(
            move_type="strike", damage=130, startup=18, active=4, recovery=24,
            knockback_x=10.0, knockback_y=-3.0,
            ce_cost=25, hit_range=70, input_desc="F,D,DF+P (Earthquake Slam)",
            armor=True, hitstun=26, blockstun=18,
        ),
        "special_3": make_move(
            move_type="grab", damage=100, startup=8, active=4, recovery=20,
            knockback_x=0.0, knockback_y=-6.0,
            ce_cost=20, hit_range=0, input_desc="360+P (Mountain Buster)",
            grab_range=55, hitstun=22, blockstun=0,
        ),
        "special_4": make_move(
            move_type="strike", damage=80, startup=20, active=8, recovery=18,
            knockback_x=5.0, knockback_y=-1.0,
            ce_cost=20, hit_range=80, input_desc="QCB+P (Avalanche Rush)",
            armor=True, hitstun=20, blockstun=14,
        ),
        # -- Super --
        "super": make_move(
            move_type="grab", damage=350, startup=6, active=4, recovery=30,
            knockback_x=8.0, knockback_y=-10.0,
            ce_cost=80, hit_range=0, input_desc="720+P (Titan's Wrath)",
            grab_range=70, invuln_startup=4, hitstun=36, blockstun=0,
        ),
    },
    "ai_preferences": {
        "aggression": 0.6,
        "zoning": 0.05,
        "grapple_tendency": 0.8,
        "special_usage": 0.5,
        "super_threshold": 0.5,
        "preferred_range": "close",
        "combo_tendency": 0.2,
    },
}


# ===== VIPER - Tricky Rushdown =====
CHARACTERS["VIPER"] = {
    "name": "VIPER",
    "title": "The Serpent Dancer",
    "color": (50, 180, 50),           # green bodysuit
    "body_color": (220, 190, 160),    # light skin
    "hair_color": (0, 0, 0),          # black hair
    "accent_color": (200, 50, 200),   # purple accents
    "outline_color": (20, 60, 20),
    "speed": 6.5,
    "jump_power": -13.0,
    "max_hp": 900,
    "weight": 0.9,
    "width": 42,
    "height": 82,
    "walk_anim_frames": 4,
    "moves": {
        # -- Normals --
        "light": make_move(
            damage=25, startup=3, active=3, recovery=5,
            knockback_x=1.5, knockback_y=0.0,
            hit_range=50, input_desc="LP",
            hitstun=11, blockstun=7,
        ),
        "heavy": make_move(
            damage=55, startup=7, active=4, recovery=13,
            knockback_x=4.0, knockback_y=-1.0,
            hit_range=58, input_desc="HP",
            hitstun=15, blockstun=10,
        ),
        "crouch_light": make_move(
            damage=20, startup=3, active=3, recovery=6,
            knockback_x=1.0, knockback_y=0.0,
            hit_range=52, input_desc="D+LP",
            hitstun=10, blockstun=6,
        ),
        "crouch_heavy": make_move(
            damage=50, startup=6, active=5, recovery=14,
            knockback_x=3.0, knockback_y=-2.5,
            hit_range=60, input_desc="D+HP",
            hitstun=14, blockstun=10,
        ),
        "jump_light": make_move(
            damage=30, startup=4, active=5, recovery=3,
            knockback_x=2.0, knockback_y=2.5,
            hit_range=50, input_desc="LP (air)",
            hitstun=12, blockstun=8,
        ),
        "jump_heavy": make_move(
            damage=65, startup=6, active=6, recovery=5,
            knockback_x=3.0, knockback_y=4.0,
            hit_range=60, input_desc="HP (air)",
            hitstun=16, blockstun=11,
        ),
        # -- Specials --
        "special_1": make_move(
            move_type="strike", damage=45, startup=5, active=6, recovery=10,
            knockback_x=3.0, knockback_y=0.0,
            ce_cost=20, hit_range=55, input_desc="QCF+P (Fang Strike)",
            hitstun=13, blockstun=8,
        ),
        "special_2": make_move(
            move_type="strike", damage=35, startup=7, active=4, recovery=8,
            knockback_x=2.0, knockback_y=-3.0,
            ce_cost=20, hit_range=50, input_desc="DP+K (Viper Bite)",
            invuln_startup=5, hitstun=14, blockstun=9,
        ),
        "special_3": make_move(
            move_type="strike", damage=55, startup=10, active=8, recovery=12,
            knockback_x=5.0, knockback_y=0.0,
            ce_cost=25, hit_range=65, input_desc="QCB+K (Coiling Rush)",
            hitstun=16, blockstun=10,
        ),
        "special_4": make_move(
            move_type="strike", damage=40, startup=8, active=6, recovery=10,
            knockback_x=1.5, knockback_y=-2.0,
            ce_cost=20, hit_range=55, input_desc="B,F+P (Poison Whip)",
            hitstun=14, blockstun=9,
        ),
        # -- Super --
        "super": make_move(
            move_type="strike", damage=260, startup=5, active=14, recovery=24,
            knockback_x=8.0, knockback_y=-7.0,
            ce_cost=55, hit_range=60, input_desc="QCF,QCF+P (Deadly Venom)",
            invuln_startup=4, hitstun=28, blockstun=18,
        ),
    },
    "ai_preferences": {
        "aggression": 0.8,
        "zoning": 0.15,
        "grapple_tendency": 0.05,
        "special_usage": 0.6,
        "super_threshold": 0.35,
        "preferred_range": "close",
        "combo_tendency": 0.8,
    },
}


# ===== STORM - Zoner with Projectiles =====
CHARACTERS["STORM"] = {
    "name": "STORM",
    "title": "Eye of the Tempest",
    "color": (60, 120, 220),          # blue gi
    "body_color": (200, 175, 140),    # tan skin
    "hair_color": (200, 200, 220),    # silver hair
    "accent_color": (100, 200, 255),  # electric cyan
    "outline_color": (20, 40, 80),
    "speed": 4.5,
    "jump_power": -11.0,
    "max_hp": 950,
    "weight": 0.95,
    "width": 46,
    "height": 86,
    "walk_anim_frames": 4,
    "moves": {
        # -- Normals --
        "light": make_move(
            damage=25, startup=5, active=3, recovery=7,
            knockback_x=2.0, knockback_y=0.0,
            hit_range=52, input_desc="LP",
            hitstun=11, blockstun=7,
        ),
        "heavy": make_move(
            damage=55, startup=9, active=4, recovery=14,
            knockback_x=4.0, knockback_y=-1.0,
            hit_range=60, input_desc="HP",
            hitstun=15, blockstun=11,
        ),
        "crouch_light": make_move(
            damage=20, startup=4, active=3, recovery=7,
            knockback_x=1.5, knockback_y=0.0,
            hit_range=50, input_desc="D+LP",
            hitstun=10, blockstun=7,
        ),
        "crouch_heavy": make_move(
            damage=50, startup=8, active=5, recovery=16,
            knockback_x=3.0, knockback_y=-2.0,
            hit_range=58, input_desc="D+HP",
            hitstun=14, blockstun=11,
        ),
        "jump_light": make_move(
            damage=30, startup=5, active=5, recovery=4,
            knockback_x=2.0, knockback_y=2.5,
            hit_range=52, input_desc="LP (air)",
            hitstun=12, blockstun=8,
        ),
        "jump_heavy": make_move(
            damage=65, startup=8, active=6, recovery=6,
            knockback_x=3.0, knockback_y=4.0,
            hit_range=62, input_desc="HP (air)",
            hitstun=16, blockstun=11,
        ),
        # -- Specials --
        "special_1": make_move(
            move_type="projectile", damage=50, startup=12, active=40, recovery=18,
            knockback_x=3.0, knockback_y=0.0,
            ce_cost=20, hit_range=0, input_desc="QCF+P (Gale Shot)",
            projectile=True, proj_speed=6.0, proj_lifetime=55,
            hitstun=14, blockstun=9,
        ),
        "special_2": make_move(
            move_type="projectile", damage=40, startup=16, active=50, recovery=20,
            knockback_x=2.0, knockback_y=0.0,
            ce_cost=25, hit_range=0, input_desc="QCB+P (Storm Cloud)",
            projectile=True, proj_speed=3.5, proj_lifetime=70,
            hitstun=14, blockstun=10,
        ),
        "special_3": make_move(
            move_type="strike", damage=30, startup=10, active=4, recovery=14,
            knockback_x=6.0, knockback_y=-2.0,
            ce_cost=20, hit_range=60, input_desc="DP+K (Thunder Kick)",
            invuln_startup=6, hitstun=14, blockstun=10,
        ),
        "special_4": make_move(
            move_type="strike", damage=55, startup=14, active=10, recovery=16,
            knockback_x=4.0, knockback_y=0.0,
            ce_cost=25, hit_range=70, input_desc="QCF+K (Cyclone Sweep)",
            hitstun=16, blockstun=12,
        ),
        # -- Super --
        "super": make_move(
            move_type="projectile", damage=220, startup=10, active=50, recovery=28,
            knockback_x=10.0, knockback_y=-4.0,
            ce_cost=70, hit_range=0, input_desc="QCF,QCF+P (Tempest Annihilation)",
            projectile=True, proj_speed=10.0, proj_lifetime=90,
            invuln_startup=8, hitstun=26, blockstun=18,
        ),
    },
    "ai_preferences": {
        "aggression": 0.2,
        "zoning": 0.9,
        "grapple_tendency": 0.0,
        "special_usage": 0.7,
        "super_threshold": 0.25,
        "preferred_range": "far",
        "combo_tendency": 0.3,
    },
}


# ===== CRUSHER - Power Hitter =====
CHARACTERS["CRUSHER"] = {
    "name": "CRUSHER",
    "title": "The Iron Hammer",
    "color": (200, 160, 40),          # gold armor
    "body_color": (180, 140, 100),    # bronze skin
    "hair_color": (50, 30, 10),       # dark brown
    "accent_color": (220, 50, 50),    # red crest
    "outline_color": (60, 40, 10),
    "speed": 4.0,
    "jump_power": -10.5,
    "max_hp": 1100,
    "weight": 1.3,
    "width": 56,
    "height": 92,
    "walk_anim_frames": 4,
    "moves": {
        # -- Normals --
        "light": make_move(
            damage=35, startup=6, active=4, recovery=8,
            knockback_x=3.0, knockback_y=0.0,
            hit_range=58, input_desc="LP",
            hitstun=13, blockstun=9,
        ),
        "heavy": make_move(
            damage=90, startup=12, active=5, recovery=18,
            knockback_x=7.0, knockback_y=-2.0,
            hit_range=70, input_desc="HP",
            hitstun=20, blockstun=15,
        ),
        "crouch_light": make_move(
            damage=30, startup=5, active=4, recovery=9,
            knockback_x=2.5, knockback_y=0.0,
            hit_range=55, input_desc="D+LP",
            hitstun=12, blockstun=8,
        ),
        "crouch_heavy": make_move(
            damage=85, startup=10, active=6, recovery=20,
            knockback_x=6.0, knockback_y=-3.0,
            hit_range=72, input_desc="D+HP",
            hitstun=20, blockstun=15,
        ),
        "jump_light": make_move(
            damage=40, startup=7, active=6, recovery=5,
            knockback_x=3.0, knockback_y=3.5,
            hit_range=58, input_desc="LP (air)",
            hitstun=15, blockstun=10,
        ),
        "jump_heavy": make_move(
            damage=100, startup=10, active=7, recovery=7,
            knockback_x=4.0, knockback_y=6.0,
            hit_range=72, input_desc="HP (air)",
            hitstun=20, blockstun=15,
        ),
        # -- Specials --
        "special_1": make_move(
            move_type="strike", damage=120, startup=16, active=4, recovery=22,
            knockback_x=10.0, knockback_y=-3.0,
            ce_cost=25, hit_range=70, input_desc="QCF+P (Hammer Down)",
            armor=True, hitstun=24, blockstun=18,
        ),
        "special_2": make_move(
            move_type="strike", damage=80, startup=20, active=10, recovery=16,
            knockback_x=6.0, knockback_y=-1.0,
            ce_cost=25, hit_range=80, input_desc="QCB+P (Crushing Blow)",
            armor=True, hitstun=20, blockstun=14,
        ),
        "special_3": make_move(
            move_type="strike", damage=70, startup=12, active=6, recovery=18,
            knockback_x=5.0, knockback_y=-4.0,
            ce_cost=20, hit_range=60, input_desc="DP+P (Meteor Uppercut)",
            invuln_startup=6, hitstun=20, blockstun=14,
        ),
        "special_4": make_move(
            move_type="grab", damage=90, startup=10, active=3, recovery=20,
            knockback_x=4.0, knockback_y=-5.0,
            ce_cost=20, hit_range=0, input_desc="HCF+P (Iron Vise)",
            grab_range=55, hitstun=22, blockstun=0,
        ),
        # -- Super --
        "super": make_move(
            move_type="strike", damage=320, startup=12, active=8, recovery=30,
            knockback_x=14.0, knockback_y=-8.0,
            ce_cost=70, hit_range=75, input_desc="QCF,QCF+P (Apocalypse Crush)",
            armor=True, invuln_startup=8, hitstun=32, blockstun=22,
        ),
    },
    "ai_preferences": {
        "aggression": 0.45,
        "zoning": 0.15,
        "grapple_tendency": 0.35,
        "special_usage": 0.4,
        "super_threshold": 0.4,
        "preferred_range": "mid",
        "combo_tendency": 0.25,
    },
}


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def get_character(name: str) -> dict[str, Any] | None:
    """Retrieve a character definition by name (case-insensitive)."""
    return CHARACTERS.get(name.upper())


def list_characters() -> list[str]:
    """Return a list of all available character names."""
    return list(CHARACTERS.keys())


def get_move(char_name: str, move_name: str) -> dict[str, Any] | None:
    """Retrieve a specific move for a character."""
    char = get_character(char_name)
    if char is None:
        return None
    return char["moves"].get(move_name)


def get_character_names() -> list[str]:
    """Return display names for all characters."""
    return [CHARACTERS[c]["name"] for c in CHARACTERS]


def get_all_move_names(char_name: str) -> list[str]:
    """Return all move names for a given character."""
    char = get_character(char_name)
    if char is None:
        return []
    return list(char["moves"].keys())


# ---------------------------------------------------------------------------
# Domain / Super Effects
# ---------------------------------------------------------------------------

DOMAIN_EFFECTS: dict[str, dict[str, Any]] = {
    "RYU":     {"type": "zone_damage", "dps": 5, "color": (255, 255, 255)},
    "BLAZE":   {"type": "self_buff",   "damage_boost": 1.5, "color": (255, 50, 50)},
    "TITAN":   {"type": "zone_damage", "dps": 8, "color": (100, 100, 160)},
    "VIPER":   {"type": "combo",       "dmg_per_hit": 20, "color": (50, 200, 50)},
    "STORM":   {"type": "zone_damage", "dps": 4, "color": (60, 120, 220)},
    "CRUSHER": {"type": "stun",        "stun_duration": 60, "color": (200, 160, 40)},
}


if __name__ == "__main__":
    # Print summary of all characters when run directly
    print("=" * 60)
    print("STREET FIGHTER - CHARACTER ROSTER")
    print("=" * 60)
    for char_key, char_data in CHARACTERS.items():
        print(f"\n--- {char_data['name']}: {char_data['title']} ---")
        print(f"  HP: {char_data['max_hp']}  Speed: {char_data['speed']}  "
              f"Jump: {char_data['jump_power']}  Weight: {char_data['weight']}")
        print(f"  Moves:")
        for move_name, move_data in char_data["moves"].items():
            ce = move_data['ce_cost']
            ce_str = f" [{ce} CE]" if ce > 0 else ""
            print(f"    {move_name:15s} DMG:{move_data['damage']:4d}  "
                  f"F:{move_data['startup']+move_data['active']+move_data['recovery']:3d}  "
                  f"{move_data['input']}{ce_str}")
    print("\n" + "=" * 60)
