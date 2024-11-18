import pygame

from clock import Clock
from game_loop import GameLoop
from level import Level
from renderer import Renderer


def main():
    width: int = 1280
    height: int = 720
    display: pygame.display = pygame.display.set_mode((width, height))

    pygame.display.set_caption("Gem Poacher")
    pygame.mouse.set_visible(False)

    level: Level = Level(height, height)
    renderer: Renderer = Renderer(display, level)
    clock: Clock = Clock()
    game_loop: GameLoop = GameLoop(level, renderer, clock)

    pygame.init()
    game_loop.run()


if __name__ == "__main__":
    main()
