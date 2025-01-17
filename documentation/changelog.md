# Changelog

## Week 3

- Created a basic structure for the game.
    - GameLoop takes care of running the main game.
    - Level class has the basic information and logic of the game.
    - Level, Clock, EventQueue, and Render are added to GameLoop as parameters.
- Added Player sprite.
    - Can be moved with the mouse, has lived, and can take damage.
- Added some tests for player class.
- Added some tests for level class.

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

- Files responsible for gameplay mechanics are moved into the game_engine package.
- Tests for all classes currently in game_engine.
- Points collected are now recorded.
- Text rendering with a controller class and updating text based on the game state.
    - Lives are rendered on screen and updated in real-time.
    - Same for points when gems are collected.
    - Level text is rendered, but the feature is not yet implemented.
- The player becomes invulnerable to damage for a set time after taking damage.
    - The player image becomes transparent during the invulnerability period.
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
- All features under the gameplay section of the req specification implemented.
- Difficulty settings:
    - Only accessible through code variables (for now).
    - Affects gem and enemy spawn rates and initial player lives
- Level progression:
    - Spawn new enemies and gems upon completing a level.
    - Level progression varies with different difficulty settings.
    - UI tracking for the current level
- New Game (reset game state) feature.
    - GameLogic and GameState classes have now features for initializing a new game on demand.
- Game Over:
  -The game ends after all player lives are lost.
    - Currently just a black screen with a new game and quit game option.

## Week 7

- Level background.
- UITextController separated into UITextController and TextObject Classes.
- Configuration file in src/config folder.
    - Pre-set difficulty settings.
    - Custom difficulty options.
    - Player lives.
- Different look for endgame screen.
- TextInputBox UI component in the endgame screen.
- Renderer and split into render and Ui manager.
- Database for storing scores.
    - Get and add players and scores.
    - The user can choose the database filename in the config file.
- Game Over screen.
    - Fully functional textbox for inputting player names.
    - Stores names and score information in the database.
    - Pagination for score pages (shows 10 at a time).
- Invoke task for creating a configuration file and score database.
- Finally refactored everything into logical packages.
    - UI files are all under ui package (except sprites).
    - Database and database management files under the database package.
    - Src will only directly contain .py files that are intended for running from the outside.
- Made Clock class keep FPS information to support changing FPS in configuration file down the line.
- Added tests to most new features in game_engine.
- Added tests to some features of configuration manager (uses .ini file) and score manager (uses a database).
