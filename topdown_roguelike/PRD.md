# PRD: TOPDOWN ROGUELIKE — "VOID RUNNER"

## Overview
A fast-paced top-down roguelike where the player kills enemies, collects points/souls, and buys upgrades between waves. Runs are short (10-15 min), death is permanent, and every run feels different via procedural generation and randomized upgrade paths.

**Engine:** Pygame | **Resolution:** 1080x720 | **Target FPS:** 60

---

## CORE LOOP
1. Enter arena → enemies spawn in waves
2. Kill enemies → they drop **Souls** (currency) + **XP orbs**
3. Collect souls/xp → fill CE meter, gain levels
4. Between waves → shop opens, spend souls on upgrades
5. Every 5 waves → boss fight
6. Death → run ends, score tallied, meta-progression saved

---

## PLAYER

### Movement
- WASD movement, smooth acceleration/deceleration
- Shift = dash (i-frame, cooldown-based, leaves afterimage trail)
- Space = dodge roll (longer i-frames, fixed direction, stamina cost)
- Base speed: 4 px/frame, upgradable

### Combat
- **Primary attack:** Melee swing in facing direction (mouse aims)
  - 3-hit combo: light → light → heavy (timing-based chain)
  - Startup/active/recovery frames (6/4/8 default)
- **Secondary attack:** Ranged projectile (limited ammo, regenerates)
- **CE Meter** (Cursed Energy): starts at 50, regens 0.3/frame
  - Powers special abilities
  - Drops on taking damage

### Stats
| Stat | Base | Description |
|------|------|-------------|
| HP | 100 | Health points |
| ATK | 10 | Base damage |
| DEF | 5 | Damage reduction |
| SPD | 4.0 | Movement speed |
| CE | 50/50 | Cursed energy pool |
| CRIT% | 5% | Crit chance |
| LUCK | 0 | Affects drop rates |

---

## ENEMIES

### Tiers
- **Tier 1 (Waves 1-5):** Crawlers, Shooters, Dashers
- **Tier 2 (Waves 6-10):** Shielders, Teleporters, Swarmers
- **Tier 3 (Waves 11-15):** Summoners, Exploders, Phantoms
- **Elite variants:** 1.5x HP, 2x damage, guaranteed rare drop, glow aura

### Enemy Types
| Type | Behavior | Drop |
|------|----------|------|
| Crawler | Chases player slowly | 5 souls |
| Shooter | Fires projectiles at range | 8 souls |
| Dasher | Charges at player, pauses | 10 souls |
| Shielder | Frontal shield, must flank | 12 souls |
| Teleporter | Blinks around, hard to track | 15 souls |
| Swarmer | Spawns in packs of 5-8, low HP | 3 souls each |
| Summoner | Spawns Tier 1 enemies | 20 souls |
| Exploder | Runs at player, detonates | 18 souls |
| Phantom | Phases through walls, ignores terrain | 22 souls |

### Bosses (every 5 waves)
- **Wave 5 — The Warden:** Slow, massive HP, ground pound AoE
- **Wave 10 — The Swarm Queen:** Summons swarmer waves, poison clouds
- **Wave 15 — The Void Knight:** Teleports, sword combos, phase 2 enrages
- Each boss has 3 attack patterns, telegraphed tells, and a unique drop

---

## UPGRADES & SHOP

### Upgrade Categories
1. **Combat** — damage, crit, attack speed, combo extensions
2. **Survival** — HP, DEF, regen, lifesteal, i-frame duration
3. **Movement** — speed, dash distance, dodge cooldown
4. **CE Mastery** — pool size, regen rate, ability damage
5. **Utility** — magnet range, luck, soul multiplier

### Upgrade Mechanics
- Shop opens between waves (3 random upgrades offered)
- Reroll option (costs souls, limited rerolls per shop)
- Upgrades stack with diminishing returns (e.g., +10% → +7% → +5%)
- **Synergy combos:** Certain upgrade pairs unlock bonus effects
  - Lifesteal + Crit = "Blood Pact" (crits heal double)
  - Speed + Dash = "Phantom Step" (dash leaves damaging trail)
  - CE Regen + ATK = "Overflow" (max CE boosts damage 20%)

### Legendary Upgrades (rare, 5% shop chance)
- **Soul Eater:** Kills restore 5% HP
- **Time Dilation:** Slow nearby enemies 30%
- **Chain Lightning:** Attacks bounce to 3 nearby enemies
- **Phoenix Feather:** Survive lethal damage once per run
- **Void Walker:** Dash through walls

---

## PROGRESSION

### In-Run
- XP orbs → level up → stat boost (+2 to random stat each level)
- Soul count → shop purchases
- Wave counter → difficulty scaling (enemy HP +8% per wave)

### Meta-Progression (persistent between runs)
- **Soul Vault:** Unspent souls carry over (partial, 20%)
- **Unlock Characters:** Beat bosses to unlock new playable characters
- **Challenge Modifiers:** "Glass Cannon" (2x damage, 0.5x HP), "Pacifist" (no melee, 3x ranged)
- **Bestiary:** Kill counts, lore entries, weak points revealed
- **Achievement Milestones:** Unlock starting bonuses (extra HP, bonus souls, etc.)

---

## ARENA & PROCEDURAL GENERATION

### Arena Types (rotates every 5 waves)
- **Arena:** Open square, minimal cover
- **Maze:** Tight corridors, ambush points
- **Swamp:** Mud patches (slow zones), poison pools
- **Void:** Floating platforms, falling = damage
- **Temple:** Pillars for cover, destructible environment

### Generation Rules
- Arena size: 3000x3000 px (camera follows player)
- Tile-based: 32x32 tiles
- Wall placement uses cellular automata for organic layouts
- Enemy spawn points: minimum 400px from player
- Pickup spawn: random, weighted toward open areas

---

## CAMERA & RENDERING

### Camera
- Smooth follow with lerp (0.08 factor)
- Slight lead toward mouse cursor (predictive offset)
- Screen shake on hits (3px, 4 frames)
- Zoom-out on boss fights (0.85x)

### Rendering Layers (back to front)
1. Background tiles
2. Floor decals (blood pools, cracks)
3. Pickups (souls, XP orbs, health packs)
4. Enemies
5. Player + projectiles
6. Particles
7. UI overlay

---

## VISUAL EFFECTS

### Particles
- Hit spark (white/yellow burst, 6-10 particles)
- Blood splatter (red, physics-based, stains floor)
- Dash trail (semi-transparent afterimage, fades in 300ms)
- Soul pickup (spiraling upward glow)
- Death burst (radial explosion, 20+ particles)

### Screen Effects
- Low HP vignette (red edges, pulsing)
- Kill flash (brief white flash on kill)
- Level-up burst (golden radial)
- Boss intro: slow zoom + text overlay

### Animations
- Player: idle bob, run cycle (4 frames), attack swing (3 frames), dash, death
- Enemies: idle, chase, attack, hit stun, death
- All use sprite sheets, 64x64 or 128x128 cells

---

## AUDIO

### Music
- Adaptive soundtrack: intensity scales with enemy count
- 3 layers: ambient (exploration), combat (enemies present), boss (boss fight)
- Procedural layering if numpy available, fallback to looping .ogg files

### SFX
- Melee swing, hit, crit
- Dash whoosh, dodge roll
- Pickup collect (souls, XP)
- Enemy death gurgle
- Boss phase transition
- UI: shop open, upgrade select, reroll
- Ambient: arena-specific background hum

---

## UI/HUD

### In-Run HUD
- **Top-left:** HP bar (red), CE bar (blue), Level + XP bar
- **Top-right:** Wave counter, Soul count, Timer
- **Bottom-left:** Current upgrades (icon row)
- **Bottom-center:** Ability cooldowns
- **Bottom-right:** Minimap (200x200 px, shows enemies as red dots)

### Menus
- **Title screen:** Start Run, Bestiary, Achievements, Settings, Quit
- **Shop screen:** 3 upgrade cards, reroll button, skip button
- **Death screen:** Run stats, score, soul earnings, "Retry" / "Main Menu"
- **Pause:** Resume, Settings, Quit to Menu

### Settings
- Volume sliders (music, SFX)
- Screen shake toggle
- Damage numbers toggle
- Difficulty: Normal / Hard / Nightmare

---

## SCORING

### Score Formula
```
score = (enemies_killed × 10) + (bosses_killed × 500) + (souls_collected × 2) + (waves_survived × 50) + (no_hit_bonus × 200) - (deaths × 1000)
```

### Multipliers
- Combo multiplier: kills within 2s chain → +0.1x per chain (max 3.0x)
- Difficulty multiplier: Hard = 1.5x, Nightmare = 2.0x
- Speed bonus: finish wave under 30s → +25% score

### Leaderboard (local)
- Top 10 runs stored in `scores.json`
- Tracks: score, character, waves survived, time, difficulty

---

## DATA STRUCTURES

### Save Data (`save.json`)
```json
{
  "meta_progression": {
    "total_souls_earned": 0,
    "characters_unlocked": ["default"],
    "achievements": [],
    "modifiers_unlocked": []
  },
  "leaderboard": []
}
```

### Run Data (in-memory)
```python
player = {
    "x": 540, "y": 360,
    "hp": 100, "max_hp": 100,
    "atk": 10, "def": 5, "spd": 4.0,
    "ce": 50, "max_ce": 50,
    "crit": 0.05, "luck": 0,
    "level": 1, "xp": 0, "xp_next": 100,
    "souls": 0,
    "upgrades": [],
    "facing": 0.0  # radians
}
```

---

## FILE STRUCTURE (planned)
```
topdown_roguelike/
├── main.py              # Game loop, scene manager
├── player.py            # Player class, input, combat
├── enemies.py           # Enemy base + all types
├── bosses.py            # Boss classes
├── arena.py             # Procedural generation
├── shop.py              # Upgrade system, shop UI
├── particles.py         # Particle system
├── camera.py            # Camera follow + effects
├── audio.py             # Sound manager (numpy fallback)
├── ui.py                # HUD, menus, overlays
├── scoring.py           # Score calculation, leaderboard
├── save_system.py       # Meta-progression persistence
├── settings.py          # Constants, config
├── assets/
│   ├── sprites/         # Sprite sheets
│   ├── audio/           # .ogg music, .wav SFX
│   └── fonts/           # .ttf fonts
└── PRD.md               # This file
```

---

## PHASE PLAN

### Phase 1: Core Mechanics
- Player movement (WASD), mouse aiming, basic attack
- Camera follow, simple arena (single room)
- 1 enemy type (Crawler), basic AI chase
- Soul drops, pickup collection
- HP system, death → restart

### Phase 2: Combat & Enemies
- 3-hit combo system, attack frame data
- All Tier 1 enemies (Crawler, Shooter, Dasher)
- Projectile system (player ranged + enemy bullets)
- Hit stun, knockback, i-frames on dash
- CE meter, regen

### Phase 3: Progression & Shop
- XP orbs, leveling, stat boosts
- Shop screen (3 upgrades, reroll)
- 15+ upgrades across 5 categories
- Synergy combo detection
- Wave system, difficulty scaling

### Phase 4: Content Expansion
- Tier 2 + Tier 3 enemies
- Boss fights (Warden, Swarm Queen, Void Knight)
- Procedural arena generation (5 arena types)
- Legendary upgrades

### Phase 5: Polish & Meta
- Particle system, screen effects
- Adaptive music, full SFX
- Complete UI (menus, HUD, settings)
- Meta-progression, save/load, leaderboard
- Achievements, bestiary, challenge modifiers

### Phase 6: Testing & Balance
- Playtest each phase independently
- Balance enemy HP/damage curves
- Tune upgrade costs vs reward
- Performance profiling (target: 60 FPS with 50+ enemies)
- Edge case handling (alt-tab, rapid input, memory)

---

## TECHNICAL CONSTRAINTS
- Pygame 2.6.1, Python 3.12.10
- No external dependencies beyond pygame (numpy optional for audio)
- All sprites are procedural (colored rects/circles) until real art is added
- Graceful fallback for missing audio (silent Sound objects)
- Use `pygame.key.get_pressed()` directly — never convert to dict
- Color values must be clamped 0-255 (avoid overflow on set_at)
