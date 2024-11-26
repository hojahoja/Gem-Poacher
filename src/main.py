import pygame

from clock import Clock
from event_queue import EventQueue
from game_logic import GameLogic
from game_loop import GameLoop
from game_state import GameState
from renderer import Renderer


def main():
    width: int = 1280
    height: int = 720
    display: pygame.display = pygame.display.set_mode((width, height))

    pygame.display.set_caption("Gem Poacher")
    pygame.mouse.set_visible(False)

    game_state: GameState = GameState(width, height)
    game_logic: GameLogic = GameLogic(game_state)
    renderer: Renderer = Renderer(display, game_state)
    clock: Clock = Clock()
    event_queue = EventQueue()
    game_loop: GameLoop = GameLoop(game_logic, renderer, clock, event_queue)

    pygame.init()
    game_loop.run()


if __name__ == "__main__":
    main()
