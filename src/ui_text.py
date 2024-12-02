from typing import Iterator

import pygame
from pygame import Surface
from pygame.font import Font

from game_engine.game_state import GameState

type TextObject = tuple[Surface, tuple[int, int]]
GAMEPLAY: str = "gameplay"
LIVES: str = "lives"
POINTS: str = "points"
LEVEL: str = "level"


class UITextController:

    def __init__(self, game_state: GameState):
        self.game_state: GameState = game_state
        self.width: int = self.game_state.width
        self.height: int = self.game_state.height
        self.text_states: dict[str, str | int] = {}

        self.fonts: dict[str, Font] = {}
        self.text_objects: dict[str, dict[str, TextObject]] = {}

        self._create_text_states()
        self._create_font_types()
        self._create_level_text_objects()

    def _create_text_states(self):
        self.text_states = {
            LEVEL: 0,
            LIVES: self.game_state.player.lives,
            POINTS: self.game_state.points,
        }

    def _create_level_text_objects(self):
        font: Font = self.fonts[GAMEPLAY]

        # TODO level functionality
        level_text: Surface = font.render("Level 1", True, (255, 0, 0))
        lives_text: Surface = font.render(f"Lives: {self.game_state.player.lives}", True,
                                          (255, 0, 0))
        points_text: Surface = font.render(f"Points {self.game_state.points}", True,
                                           (255, 0, 0))

        self.text_objects[GAMEPLAY] = {
            LEVEL: (level_text, (self.width - 200, 10)),
            LIVES: (lives_text, (self.width - 320, 10)),
            POINTS: (points_text, (self.width - 200, self.height - 30))
        }

    def get_text_surface_group(self, group_name: str) -> Iterator[TextObject]:
        return iter(self.text_objects[group_name].values())

    def _update_text_object(self, group_name: str, object_name: str, text: str):
        font: Font = self.fonts[group_name]
        surface: Surface = font.render(text, True, (255, 0, 0))
        location: tuple[int, int] = self.text_objects[group_name][object_name][1]
        self.text_objects[group_name][object_name] = (surface, location)

    def _create_font_types(self):
        self.fonts[GAMEPLAY] = pygame.font.SysFont("Arial", 24)

    def update(self):
        current_lives: int = self.game_state.player.lives
        if self.text_states[LIVES] != current_lives:
            self._update_text_object(GAMEPLAY, LIVES, f"Lives: {current_lives}")

        current_points: int = self.game_state.points
        if self.text_states[POINTS] != current_points:
            self._update_text_object(GAMEPLAY, POINTS, f"Points: {current_points}")
