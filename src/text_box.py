import os

import pygame.font
from pygame import Surface
from pygame.font import Font

import image_handler
from text_object import TextObject

from utilities.constants import Folder

FONTS_DIR = Folder.FONTS_DIR
type Blit = tuple[Surface, tuple[int, int]]


class TextInputBox:
    def __init__(self, position: tuple[int, int], title: str, scale: float = 0):
        super().__init__()

        self.position = position
        self._text: str = ""
        self._active: bool = False

        self._init_image(scale)

        scale = scale if scale else 1
        self.scale = scale
        self._init_title_text(title)
        self._init_input_text_object()

    def _init_image(self, scale: float):
        self._image: Surface = image_handler.load_image("text_box_narrow_titled.png")

        if scale:
            self._image = image_handler.scale_image(self._image, scale)

    def _init_title_text(self, title: str):
        title_font: Font = pygame.font.Font(os.path.join(FONTS_DIR, "Cinzel-Medium.ttf"),
                                            int(64 * self.scale))

        self._title_text_object = TextObject(title, (0, 0, 0), title_font)
        self._align_text_object(self._title_text_object, height=30)

    def _init_input_text_object(self):
        input_font: Font = pygame.font.Font(os.path.join(FONTS_DIR, "Cinzel-Medium.ttf"),
                                            int(80 * self.scale))

        self._input_text_object = TextObject(self._text, (0, 0, 0), input_font)

        self._align_text_object(self._input_text_object, height=130)

    @property
    def text(self):
        return self._text

    @property
    def active(self):
        return self._active

    def activate(self):
        pygame.key.set_repeat(500, 50)
        self._text = ""
        self._active = True

    def deactivate(self):
        pygame.key.set_repeat(0, 0)
        self._active = False

    def _align_text_object(self, text_object: TextObject, height: int):
        x: int = self.position[0]
        y: int = self.position[1]
        x += self._image.get_width() // 2 - text_object.surface.get_width() // 2
        y += int(height * self.scale) - text_object.surface.get_height() // 2
        text_object.location = (x, y)

    def blits(self) -> tuple[Blit, Blit, Blit]:
        return ((self._image, self.position),
                (self._title_text_object.surface, self._title_text_object.location),
                (self._input_text_object.surface, self._input_text_object.location))

    def update(self):
        self._input_text_object.update(self._text)
        self._align_text_object(self._input_text_object, height=130)

    def input_text(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self._text = self._text[:-1]
            elif self._input_text_object.surface.get_width() // self.scale <= 1000:
                self._text += event.unicode
