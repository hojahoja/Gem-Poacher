import os
import sys

import pygame

from game_engine import Clock, EventQueue, GameLogic, GameLoop, GameState
from renderer import Renderer
from ui_manager import UIManager
from utilities.config_manager import ConfigManager

base_path: str = os.path.dirname(__file__)
type ProgressionLogic = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]


# Docstrings in this module were written with the help of AI generation.
def init(cfg: ConfigManager) -> GameLoop:
    """
    Initializes the game application. Sets up display properties, game state,
    logic, and control flow components required for running the game.


    Returns:
        A GameLoop instance that manages the core game loop operations.
    """

    pygame.display.set_caption("Gem Poacher")
    pygame.font.init()

    components: tuple = _initialize_loop_components(cfg)
    pygame.mouse.set_visible(False)

    game_loop: GameLoop = GameLoop(*components)

    pygame.init()
    return game_loop


def _initialize_loop_components(config: ConfigManager) -> tuple:
    width: int = 1280
    height: int = 720
    display: pygame.Surface = pygame.display.set_mode((width, height))

    difficulty: int = config.get_difficulty()
    custom_settings: ProgressionLogic | None = None
    player_lives: int = 18

    if difficulty == -1:
        custom_settings = config.get_custom_difficulty_settings()
        player_lives = config.get_player_lives()

    game_state: GameState = GameState(width, height, difficulty, player_lives)
    game_logic: GameLogic = GameLogic(game_state, custom_settings)

    event_queue = EventQueue()

    ui_manager: UIManager = UIManager(game_state)

    renderer: Renderer = Renderer(display, ui_manager)

    clock: Clock = Clock()

    return game_logic, renderer, clock, event_queue


def stop():
    """Exits the game application cleanly."""
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    config_manager: ConfigManager = ConfigManager()
    config_manager.create_config()
    loop: GameLoop = init(config_manager)
    loop.run()
    stop()
