import itertools
from itertools import chain
from typing import TYPE_CHECKING

import pygame
from pygame import Surface

from ui import ui_text
from ui.text_box import TextInputBox
from ui.ui_text import UITextController
from utilities import constants
from utilities import image_handler
from utilities.score_manager import ScoreManager

if TYPE_CHECKING:
    from game_engine import GameState


class UIManager:

    def __init__(self, game_state: "GameState", score_manager: "ScoreManager"):
        self.text_controller: UITextController = UITextController(game_state, score_manager)
        self.game_state = game_state
        self.loop_state = 0
        self.score_page = 0
        self.score_manager: ScoreManager = score_manager
        self._init_backgrounds()

        self.text_box = TextInputBox((240, 271), "Enter Your Name", constants.SCALE_720P)

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
            self.text_controller.get_text_surface_group(ui_text.Group.GAMEPLAY))

    def _end_game_screen(self) -> chain[tuple[Surface, tuple[int, int]]]:

        first = self.score_page * 10
        last = first + 10

        return itertools.chain(
            [(self.backgrounds["end"], (0, 0))],
            self.text_controller.get_text_surface_group(ui_text.Group.HIGH_SCORES, first, last),
            self.text_controller.get_text_surface_group(ui_text.Group.GAME_OVER_SCREEN),
            self.text_box.blits() if self.text_box.active else []

        )

    def update(self):

        if not self.game_state.game_over:
            self.text_controller.update()
            if self.loop_state == 1:
                pygame.mouse.set_visible(False)
                self.text_box.deactivate()
                self.score_page = 0
                self.loop_state = 0
        else:
            self.text_controller.update()
            if self.loop_state == 0:
                self.text_box.activate()
                pygame.mouse.set_visible(True)
                self.loop_state = 1
            self.text_box.update()

    def handle_ui_events(self, event: pygame.event.Event):
        if self.text_box.active:
            self._text_box_events(event)
        elif self.game_state.game_over:
            self._score_board_events(event)

    def _score_board_events(self, event: pygame.event.Event):
        pages: int = (len(self.score_manager.get_scores()) + 9) // 10
        if event.key in (pygame.K_F1, pygame.K_LEFT) and pages > 1:
            self.score_page = (self.score_page - 1) % pages
            if self.score_page < 0:
                self.score_page = pages - 1

        elif event.key in (pygame.K_F2, pygame.K_RIGHT) and pages > 1:
            self.score_page = (self.score_page + 1) % pages

    def _text_box_events(self, event: pygame.event.Event):
        if event.key != pygame.K_RETURN:
            self.text_box.input_text(event)
        else:
            if self.text_box.text:
                self.score_manager.add_score(self.text_box.text, self.game_state.level,
                                             self.game_state.points)
            self.text_box.deactivate()
