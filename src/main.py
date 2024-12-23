import os
import sys
from sqlite3 import Connection

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
os.environ["SDL_AUDIODRIVER"] = "dsp"

# The given linter file makes it so that pylint keeps whining about wrong import order.
# However, the os.environ calls need to happen before pygame is imported for them to work.
# SDL AUDIODRIVER in particular fixes annoying error caused by pygame
# trying to use the ALSA driver on linux.

# pylint: disable=wrong-import-position
import pygame

from database.database_connection import get_database_connection
from database.score_service import ScoreService
from game_engine import Clock, EventQueue, GameLogic, GameLoop, GameState
from ui.renderer import Renderer
from ui.ui_manager import UIManager
from utilities.config_manager import ConfigManager
from utilities.score_manager import ScoreManager

# pylint: enable=wrong-import-position

type ProgressionLogic = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
type Components = tuple[GameLogic, Renderer, Clock, EventQueue]


# Docstrings in this module were written with the help of AI generation.
def init(config: ConfigManager, connection: Connection) -> GameLoop:
    """ Basic setup for pygame. GameLoop components are initialized in the
    _initialize_loop_components function.

    Args:
        config: Configuration manager instance passed to _initialize_loop_components.
        connection: Connection instance for database operations.

    Returns:
        GameLoop: A fully initialized game loop ready to be executed.
    """

    pygame.display.set_caption("Gem Poacher")
    pygame.font.init()

    components: tuple = _initialize_loop_components(config, connection)
    pygame.mouse.set_visible(False)

    game_loop: GameLoop = GameLoop(*components)

    pygame.init()
    return game_loop


def _initialize_loop_components(config: ConfigManager, connection: Connection) -> Components:
    """ Initializes and returns essential components required for the game loop.

    This function prepares and configures the game state, game logic, score manager, UI manager,
    renderer, clock, and event queue based on the provided configuration and connection. If the
    difficulty setting is custom, additional properties such as custom difficulty settings and
    player lives are retrieved and used.

    Args:
        config: The configuration manager instance that provides game settings such as difficulty,
            custom difficulty settings, and player lives.
        connection: Connection instance for database operations.

    Returns:
        tuple: A tuple containing initialized instances of the game logic, renderer, clock,
            and event queue for the game.
    """
    width: int = 1280
    height: int = 720
    display: pygame.Surface = pygame.display.set_mode((width, height))

    difficulty: int = config.get_difficulty()

    if difficulty == -1:
        custom_settings = config.get_custom_difficulty_settings()
        player_lives = config.get_player_lives()
        game_state: GameState = GameState(width, height, difficulty, player_lives)
        game_logic: GameLogic = GameLogic(game_state, custom_settings)
    else:
        game_state: GameState = GameState(width, height, difficulty)
        game_logic: GameLogic = GameLogic(game_state)

    scores: ScoreManager = ScoreManager(ScoreService(connection))
    ui_manager: UIManager = UIManager(game_state, scores)

    renderer: Renderer = Renderer(display, ui_manager)

    clock: Clock = Clock()
    event_queue = EventQueue()

    return game_logic, renderer, clock, event_queue


def stop(connection: Connection):
    """Exits the game application cleanly."""
    connection.close()
    pygame.quit()
    sys.exit()


def run():
    """Main entry point for the game application."""
    config: ConfigManager = ConfigManager()
    config.create_config()
    connection: Connection = get_database_connection()
    loop: GameLoop = init(config, connection)
    loop.run()
    stop(connection)


if __name__ == "__main__":
    run()
