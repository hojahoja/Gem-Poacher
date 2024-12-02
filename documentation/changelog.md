# Changelog

## Week 3

- Created basic structure for the game.
    - GameLoop takes care of running the main game.
    - Level class has the basic information and logic of the game.
    - Level, Clock, EventQueue and Render are added to GameLoop as parameters.
- Added Player sprite.
    - Can be moved with the mouse, has lives and can take damage.
- Added some tests for player.
- Added some tests for level.

## Week 4

- Added Gem sprite.
    - Basic tests.
- Collision detection:
    - Collision between player and gems removes gems from the game.
    - Collision between player and borders damages player.
- image_handler module for loading and manipulating images.
- Refactored Level Class into GameState and GameLogic.
    - Added appropriate tests for these classes.

## Week 5

- Files responsible for gameplay mechanics are moved into game_engine package.
- Tests for all classes currently in game_engine.
- Points collected are now recorded.
- Text rendering with and updating text based on game state.
    - Lives are rendered on screen and updated in real time.
    - Same for points when games are collected.
    - Level text is rendered, but the feature is not yet implemented.