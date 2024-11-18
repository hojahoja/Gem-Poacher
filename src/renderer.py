import pygame

from level import Level


class Renderer:

    def __init__(self, display: pygame.display, level: Level):
        self._display = display
        self._level = level

    def render(self):
        self._display.fill((255, 255, 255))
        self._level.sprites.draw(self._display)
        pygame.display.update()
