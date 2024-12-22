import sys
from sqlite3 import Connection

import pygame

from database.database_connection import get_database_connection
from database.score_service import ScoreService
from game_engine import Clock, EventQueue, GameLogic, GameLoop, GameState
from ui.renderer import Renderer
from ui.ui_manager import UIManager
from utilities.config_manager import ConfigManager
from utilities.score_manager import ScoreManager

type ProgressionLogic = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
type Components = tuple[GameLogic, Renderer, Clock, EventQueue]


# Docstrings in this module were written with the help of AI generation.
def init(config: ConfigManager, connection: Connection) -> GameLoop:
    """
    Initializes the game application. Sets up display properties, game state,
    logic, and control flow components required for running the game.


    Returns:
        A GameLoop instance that manages the core game loop operations.
    """

    pygame.display.set_caption("Gem Poacher")
    pygame.font.init()

    components: tuple = _initialize_loop_components(config, connection)
    pygame.mouse.set_visible(False)

    game_loop: GameLoop = GameLoop(*components)

    pygame.init()
    return game_loop


def _initialize_loop_components(config: ConfigManager, connection: Connection) -> Components:
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
    config: ConfigManager = ConfigManager()
    config.create_config()
    connection: Connection = get_database_connection()
    loop: GameLoop = init(config, connection)
    loop.run()
    stop(connection)


if __name__ == "__main__":
    run()
