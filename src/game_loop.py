import pygame

from clock import Clock
from level import Level
from renderer import Renderer


class GameLoop:

    def __init__(self, level: Level, renderer: Renderer, clock: Clock):
        self._level = level
        self._renderer = renderer
        self._clock = clock

    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    self._level.move_player(event.pos[0], event.pos[1])

                if event.type == pygame.QUIT:
                    exit()

            self._renderer.render()
            self._clock.tick(120)
