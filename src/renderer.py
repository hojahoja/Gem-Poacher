import pygame
from pygame import Surface

import ui_text
from game_engine.game_state import GameState


class Renderer:

    def __init__(self, display: Surface, game_state: GameState):
        self._display: Surface = display
        self._game_state: GameState = game_state
        self.text_controller = ui_text.UITextController(game_state)

    def render(self):
        self._display.fill((255, 255, 255))
        self.text_controller.update()
        self.render_text_object_groups(ui_text.GAMEPLAY)
        self._game_state.sprites.draw(self._display)
        pygame.display.update()

    def render_text_object_groups(self, group_name: str):
        for text_object in self.text_controller.get_text_surface_group(group_name):
            self._display.blit(*text_object)
