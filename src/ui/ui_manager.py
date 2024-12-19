import itertools
from itertools import chain
from typing import TYPE_CHECKING

import pygame
from pygame import Surface

from utilities import image_handler
from ui import ui_text
from ui.text_box import TextInputBox
from ui.ui_text import UITextController

if TYPE_CHECKING:
    from game_engine import GameState


class UIManager:

    def __init__(self, game_state: "GameState"):
        self.text_controller: UITextController = UITextController(game_state)
        self.game_state = game_state
        self.loop_state = 0
        self._init_backgrounds()

        self.text_box = TextInputBox((240, 271), "Enter Your Name", scale=720 / 1008)

    def _init_backgrounds(self):
        game_bg: Surface = image_handler.load_image("castle_dungeon_background.png", False,
                                                    (1280, 720))
        end_bg: Surface = image_handler.load_image("end_game.png", False, (1280, 720))

        self.backgrounds: dict[str, Surface] = {
            "game": game_bg,
            "end": end_bg
        }

    def draw_callbacks(self, surface):
        if not self.game_state.game_over:
            self.game_state.sprites.draw(surface)

    def get_renderable_surfaces(self):
        if not self.game_state.game_over:
            return self._gameplay_screen_()

        return self._end_game_screen()

    def _gameplay_screen_(self) -> chain[tuple[Surface, tuple[int, int]]]:
        return itertools.chain(
            [(self.backgrounds["game"], (0, 0))],
            self.text_controller.get_text_surface_group(ui_text.GAMEPLAY))

    def _end_game_screen(self) -> chain[tuple[Surface, tuple[int, int]]]:

        return itertools.chain(
            [(self.backgrounds["end"], (0, 0))],
            self.text_box.blits() if self.text_box.active else []
        )

    def update(self):

        if not self.game_state.game_over:
            self.text_controller.update()
            if self.loop_state == 1:
                pygame.mouse.set_visible(False)
                self.text_box.deactivate()
                self.loop_state = 0
        else:
            if self.loop_state == 0:
                self.text_box.activate()
                pygame.mouse.set_visible(True)
                self.loop_state = 1
            self.text_box.update()

    def handle_ui_events(self, event: pygame.event.Event):
        if self.text_box.active:
            if event.key != pygame.K_RETURN:
                self.text_box.input_text(event)
            else:
                if self.text_box.text:
                    # TODO save name into records.
                    print(self.text_box.text)
                self.text_box.deactivate()
