import sys

import pygame

from game_engine import Clock, EventQueue, GameLogic, GameLoop, GameState
from renderer import Renderer


# Docstrings in this module were written with the help of AI generation.
def init() -> GameLoop:
    """
    Initializes the game application. Sets up display properties, game state,
    logic, and control flow components required for running the game.


    Returns:
        A GameLoop instance that manages the core game loop operations.
    """
    width: int = 1280
    height: int = 720
    display: pygame.Surface = pygame.display.set_mode((width, height))

    pygame.display.set_caption("Gem Poacher")
    pygame.mouse.set_visible(False)

    game_state: GameState = GameState(width, height)
    game_logic: GameLogic = GameLogic(game_state)
    clock: Clock = Clock()
    event_queue = EventQueue()

    pygame.font.init()
    renderer: Renderer = Renderer(display, game_state)
    game_loop: GameLoop = GameLoop(game_logic, renderer, clock, event_queue)

    pygame.init()
    return game_loop


def stop():
    """Exits the game application cleanly."""
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    loop: GameLoop = init()
    loop.run()
    stop()
