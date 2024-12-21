from pathlib import Path

import pygame.font
from pygame import Surface
from pygame.font import Font

from ui.text_object import TextObject
from utilities import image_handler
from utilities.constants import Folder

CINZEL_MEDIUM: Path = Path(Folder.FONTS_DIR) / "Cinzel-Medium.ttf"
type Blit = tuple[Surface, tuple[int, int]]


class TextInputBox:
    def __init__(self, position: tuple[int, int], title: str, scale: float = 0):
        super().__init__()

        self._text: str = ""
        self._init_image(scale)

        self._variables: dict[str, int | float | bool | tuple[int, int]] = {
            "position": position,
            "scale": scale or 1,
            "active": False,
            "cursor_visible": True,
            "previous_cursor_change": 0
        }

        self._init_title_text(title)
        self._init_input_text_object()
        self._cursor: tuple[Surface, tuple[int, int]] | None = None
        self._init_cursor()

    def _init_image(self, scale: float):
        self._image: Surface = image_handler.load_image("text_box_narrow_titled.png")

        if scale:
            self._image = image_handler.scale_image(self._image, scale)

    def _init_title_text(self, title: str):

        title_font: Font = pygame.font.Font(CINZEL_MEDIUM, int(64 * self.scale))

        self._title_text_object = TextObject(title, (0, 0, 0), title_font)
        self._align_text_object(self._title_text_object, height=30)

    def _init_input_text_object(self):
        input_font: Font = pygame.font.Font(CINZEL_MEDIUM, int(80 * self.scale))

        self._input_text_object = TextObject(self._text, (0, 0, 0), input_font)

        self._align_text_object(self._input_text_object, height=130)

    def _init_cursor(self):
        cursor_surface: Surface = Surface((int(7 * self.scale), int(80 * self.scale)))
        cursor_surface.fill((0, 0, 0))

        self._cursor: tuple[Surface, tuple[int, int]] = (cursor_surface, (0, 0))
        self._align_cursor_()

    def _align_cursor_(self):
        text_position: tuple[int, int] = self._input_text_object.location
        cursor_position: tuple[int, int] = (
            text_position[0] + self._input_text_object.surface.get_width(),
            text_position[1] + int(10 * self.scale))
        self._cursor = (self._cursor[0], cursor_position)

    @property
    def text(self) -> str:
        return self._text

    @property
    def position(self) -> tuple[int, int]:
        return self._variables["position"]

    @property
    def scale(self) -> float:
        return self._variables["scale"]

    @scale.setter
    def scale(self, value: float):
        self._variables["scale"] = value

    @property
    def active(self) -> bool:
        return self._variables["active"]

    def activate(self):
        pygame.key.set_repeat(500, 50)
        self._text = ""
        self._variables["active"] = True

    def deactivate(self):
        pygame.key.set_repeat(0, 0)
        self._variables["active"] = False

    def _align_text_object(self, text_object: TextObject, height: int):
        x: int = self.position[0]
        y: int = self.position[1]
        x += self._image.get_width() // 2 - text_object.surface.get_width() // 2
        y += int(height * self.scale) - text_object.surface.get_height() // 2
        text_object.location = (x, y)

    def _cursor_blink(self):
        if self._input_text_object.surface.get_width() // self.scale >= 1000:
            self._variables["cursor_visible"] = False
        elif pygame.time.get_ticks() - self._variables["previous_cursor_change"] > 550:
            self._variables["previous_cursor_change"] = pygame.time.get_ticks()
            self._variables["cursor_visible"] = not self._variables["cursor_visible"]

    def update(self):
        if self._input_text_object.text != self._text:
            self._input_text_object.update(self._text)
            self._align_text_object(self._input_text_object, height=130)
            self._align_cursor_()
        self._cursor_blink()

    def blits(self) -> list[Blit]:
        blit_list: list[Blit] = [
            (self._image, self.position),
            (self._title_text_object.surface, self._title_text_object.location),
            (self._input_text_object.surface, self._input_text_object.location),
        ]

        if self._variables["cursor_visible"]:
            blit_list.append((self._cursor[0], self._cursor[1]))

        return blit_list

    def input_text(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self._text = self._text[:-1]
            elif self._input_text_object.surface.get_width() // self.scale <= 1000:
                self._text += event.unicode
