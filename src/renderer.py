import pygame

from game_engine.game_state import GameState


class Renderer:

    def __init__(self, display: pygame.display, game_state: GameState):
        self._display = display
        self._game_state = game_state

    def render(self):
        self._display.fill((255, 255, 255))
        self._game_state.sprites.draw(self._display)
        pygame.display.update()
