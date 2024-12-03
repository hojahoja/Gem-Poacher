# Architecture Description

## Structure

![Package diagram](images/package_diagram.png)

The "game_engine package" is basically just the src folder for now,
but might get seperated into its own folder later on as the project
gets developed further. Utilities package doesn't exit as of now either,
but will likely be added in some form later on when I start working on DB
functionalities. The diagram still describes the basic idea behind the
the structure as of now.

## Functionality examples

### Player takes damage from touching a game border

```mermaid
sequenceDiagram
    participant GameLoop
    participant GameLogic
    participant Player(class)
    participant pygame
    GameLoop ->> GameLogic: update()
    GameLogic ->> GameLogic: run_collision_checks()
    GameLogic ->> GameLogic: player_wall_collision()
    GameLogic ->> GameLogic: detect_border_collision()
    GameLogic ->> Player(class): rect.left
    Player(class) -->> GameLogic: "some integer"
    GameLogic ->> Player(class): rect.right
    Player(class) -->> GameLogic: "another integer"
    GameLogic ->> Player(class): rect.top
    Player(class) -->> GameLogic: "another integer"
    GameLogic ->> Player(class): rect.bottom
    Player(class) -->> GameLogic: "another integer"
    GameLogic -->> GameLogic: True
    GameLogic ->> GameLogic: player_damage_event_handler()
    GameLogic ->> Player(class): vulnerable
    Player(class) -->> GameLogic: True
    GameLogic ->> Player(class): injure()
    Player(class) ->> Player(class): lives = lives - 1
    GameLogic ->> GameLogic: activate_player_invulnerability()
    GameLogic ->> Player(class): vulnerable(False)
    Player(class) ->> Player(class): vulnerable = False
    GameLogic ->> pygame: time.get_ticks()
    pygame -->> GameLogic: "int(nanoseconds)"
    GameLogic ->> GameLogic: "invulnerability_period_start = "int(nanoseconds)
```