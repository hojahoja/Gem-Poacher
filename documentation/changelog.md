# Changelog

## Week 3

- Created basic structure for the game
    - GameLoop takes care of running the main game.
    - Level class has the basic information and logic of the game
    - Level, Clock, EventQueue and Render are added to GameLoop as parameters
- Added Player sprite
    - Can be moved with the mouse, has lives and can take damage.
- Added some tests for player
- Added some tests for level

## Week 4

- Added Gem sprite
- Collision detection:
    - Collision between player and gems removes gems from the game
    - Collision between player and borders damages player.
- image_handler module for loading and manipulating images.