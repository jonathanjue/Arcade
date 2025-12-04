# Pacman Game Architecture Diagram

## Class Diagram

```mermaid
classDiagram
    %% Main Game Classes
    class GameManager {
        +screen: pygame.Surface
        +clock: pygame.time.Clock
        +running: bool
        +current_state: GameState
        +score_manager: ScoreManager
        +powerup_manager: PowerupManager
        +maze: Maze
        +pacman: Pacman
        +ghosts: List[Ghost]
        +run()
        +handle_events()
        +update(dt: float)
        +render()
        +change_state(new_state: GameState)
    }

    class GameState {
        <<abstract>>
        +enter()
        +exit()
        +handle_event(event: pygame.Event)
        +update(dt: float)
        +render(screen: pygame.Surface)
    }

    class MenuState {
        +selected_option: int
        +options: List[str]
        +handle_event(event: pygame.Event)
        +render(screen: pygame.Surface)
    }

    class PlayState {
        +paused: bool
        +handle_event(event: pygame.Event)
        +update(dt: float)
        +render(screen: pygame.Surface)
    }

    class GameOverState {
        +final_score: int
        +handle_event(event: pygame.Event)
        +render(screen: pygame.Surface)
    }

    %% Game Entities
    class Pacman {
        +position: Vector2
        +direction: Vector2
        +speed: float
        +lives: int
        +sprite: pygame.Surface
        +move()
        +collect_dot()
        +use_powerup()
        +get_position()
        +set_direction(new_direction: Vector2)
    }

    class Ghost {
        <<abstract>>
        +position: Vector2
        +speed: float
        +state: str
        +target: Vector2
        +sprite: pygame.Surface
        +chase(pacman_position: Vector2)
        +scatter()
        +frightened()
        +update(dt: float)
        +change_state(new_state: str)
    }

    class Blinky {
        +aggressive_chase(pacman_position: Vector2)
        +find_shortest_path(target: Vector2)
    }

    class Pinky {
        +ambush_chase(pacman_position: Vector2, pacman_direction: Vector2)
        +predict_position(current: Vector2, direction: Vector2)
    }

    class Inky {
        +random_chase()
        +random_direction()
    }

    %% Game Systems
    class Maze {
        +layout: List[List[str]]
        +dot_positions: List[Vector2]
        +powerup_positions: List[Vector2]
        +cell_size: int
        +load_layout(file_path: str)
        +get_valid_moves(position: Vector2)
        +check_collision(position: Vector2)
        +consume_dot(position: Vector2)
        +spawn_powerup()
    }

    class ScoreManager {
        +current_score: int
        +high_score: int
        +dot_points: int
        +ghost_points: int
        +powerup_points: int
        +add_points(amount: int)
        +update_high_score()
        +reset_score()
        +get_score()
    }

    class PowerupManager {
        +active_powerups: List[str]
        +powerup_timers: Dict[str, float]
        +spawn_powerup(position: Vector2)
        +activate_powerup(powerup_type: str)
        +deactivate_powerup(powerup_type: str)
        +is_powerup_active(powerup_type: str)
        +update()
    }

    class CollisionManager {
        +check_entity_collision(entity1: GameObject, entity2: GameObject)
        +check_wall_collision(entity: GameObject, maze: Maze)
        +check_dot_collision(pacman: Pacman, maze: Maze)
    }

    class InputManager {
        +handle_keyboard_input(event: pygame.Event)
        +handle_joystick_input(event: pygame.Event)
        +get_pacman_direction()
    }

    %% Relationships
    GameManager --> GameState
    GameManager --> Pacman
    GameManager --> Ghost
    GameManager --> Maze
    GameManager --> ScoreManager
    GameManager --> PowerupManager
    GameManager --> CollisionManager
    GameManager --> InputManager

    GameState <|-- MenuState
    GameState <|-- PlayState
    GameState <|-- GameOverState

    Ghost <|-- Blinky
    Ghost <|-- Pinky
    Ghost <|-- Inky

    CollisionManager --> Pacman
    CollisionManager --> Ghost
    CollisionManager --> Maze

    InputManager --> Pacman
```

## System Workflow

### Game Initialization Flow

```mermaid
flowchart TD
    A[Start] --> B[Initialize Pygame]
    B --> C[Load Configuration]
    C --> D[Create Game Manager]
    D --> E[Initialize Managers]
    E --> F[Load Assets]
    F --> G[Setup Game States]
    G --> H[Enter Menu State]
    H --> I[Main Game Loop]
```

### Main Game Loop

```mermaid
flowchart TD
    A[Game Loop Start] --> B[Handle Events]
    B --> C[Update Game State]
    C --> D[Update Entities]
    D --> E[Check Collisions]
    E --> F[Update Managers]
    F --> G[Render Frame]
    G --> H[Check State Changes]
    H -->|State Changed| I[Transition State]
    H -->|No Change| A
    I --> A
```

### Ghost AI Decision Flow

```mermaid
flowchart TD
    A[Ghost Update Start] --> B{Current State?}
    B -->|Chase| C[Target Pacman]
    B -->|Scatter| D[Move to Corner]
    B -->|Frightened| E[Random Movement]
    C --> F[Blinky: Direct Path]
    C --> G[Pinky: Predict Path]
    C --> H[Inky: Random Target]
    F --> I[Calculate Path]
    G --> I[Calculate Path]
    H --> I[Calculate Path]
    I --> J[Move Ghost]
    D --> J[Move Ghost]
    E --> J[Move Ghost]
    J --> K[Check Collisions]
    K --> L[Update Position]
```

### Powerup System Flow

```mermaid
flowchart TD
    A[Powerup Spawned] --> B[Pacman Collects]
    B --> C[Activate Powerup]
    C --> D[Ghosts Enter Frightened State]
    D --> E[Start Timer]
    E --> F{Timer Expired?}
    F -->|No| G[Continue Frightened State]
    F -->|Yes| H[Deactivate Powerup]
    H --> I[Ghosts Return to Normal]
    G --> J[Check Pacman-Ghost Collision]
    J -->|Collision| K[Pacman Eats Ghost]
    K --> L[Add Bonus Points]
    L --> M[Respawn Ghost]
    M --> G
```

## Component Interaction Diagram

```mermaid
sequenceDiagram
    participant GM as GameManager
    participant PS as PlayState
    participant P as Pacman
    participant G as Ghost
    participant M as Maze
    participant CM as CollisionManager
    participant IM as InputManager
    participant SM as ScoreManager
    participant PM as PowerupManager

    GM->>PS: update()
    PS->>IM: get_pacman_direction()
    IM-->>PS: direction
    PS->>P: set_direction(direction)
    P->>M: get_valid_moves()
    M-->>P: valid_moves
    P->>P: move()
    P->>CM: check_dot_collision()
    CM->>M: consume_dot()
    M-->>CM: dot_consumed
    CM-->>P: collision_result
    P->>SM: add_points(dot_points)

    GM->>G: update()
    G->>G: determine_target()
    G->>M: get_valid_moves()
    M-->>G: valid_moves
    G->>G: move()

    GM->>CM: check_entity_collision(P, G)
    CM->>PM: is_powerup_active()
    PM-->>CM: is_active
    alt Powerup Active
        CM->>SM: add_points(ghost_points)
        CM->>G: change_state(frightened)
    else Normal State
        CM->>PS: game_over()
    end

    GM->>PM: update()
    PM->>PM: check_timers()
    PM->>G: change_state(normal)
```

## Implementation Priority

1. **Core Game Loop**: GameManager, GameState system
2. **Player System**: Pacman movement and controls
3. **Maze System**: Layout loading and collision detection
4. **Basic Ghost AI**: Simple movement patterns
5. **Scoring System**: Points tracking
6. **Advanced Ghost AI**: Unique behaviors for each ghost
7. **Powerup System**: Collection and activation logic
8. **Visual Polish**: Sprites, animations, UI

## Technical Considerations

### Performance Optimization
- **Pathfinding**: Use A* algorithm for ghost pathfinding
- **Collision Detection**: Spatial partitioning for efficient checks
- **Rendering**: Sprite batching and layer management

### Memory Management
- **Object Pooling**: Reuse ghost and powerup objects
- **Asset Caching**: Load and cache all sprites at startup
- **State Cleanup**: Properly clean up game objects on state change

This architecture diagram provides a comprehensive visual representation of the Pacman game system, showing class relationships, system workflows, and component interactions.