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
- Text rendering with a controller class and updating text based on game state.
    - Lives are rendered on screen and updated in real time.
    - Same for points when gems are collected.
    - Level text is rendered, but the feature is not yet implemented.
- Player becomes invulnerable to damage for a set period of time after taking damage.
    - Player image becomes transparent during the invulnerability period.
- Enemy character:
    - Random spawn point.
    - Move diagonally around the game area.
    - Can be initiated with different movement speeds.
    - Changes movement direction when they hit a border.
    - Damages the player when touched.
    - Minor movement animation swapping between 3 frames.

## Week 6

- Every class has a Docstring.
- Majority of engine and sprite tests covered.
- All features under gameplay section of req specification implemented.
- Difficulty settings:
    - Only accessible through code variables (for now).
    - Affects gem and enemy spawn rates and initial player lives
- Level progression:
    - Spawn new enemies and gems upon completing a level.
    - Level progression varies with different difficulty settings.
    - UI tracking for current level
- New Game (reset game state) feature.
    - GameLogic and GameState classes have now features for initializing a new game on demand.
- Game Over:
    - Game ends after all player lives are lost.
    - Currently just a black screen with new game and quit game options.

## Week 7

- Level background.
- UITextController separated into UITextController and TextObject Classes.
- Configuration file in src/config folder.
    - Pre-set difficulty settings
    - Custom difficulty options
    - Player lives
- Different look for endgame screen
- TextInputBox UI-component in endgame screen
- Renderer and split into render and Ui manager.