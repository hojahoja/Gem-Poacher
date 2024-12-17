import os

import pygame.font
from pygame import Surface
from pygame.font import Font

import image_handler
from text_object import TextObject

from utilities.constants import Folder

FONTS_DIR = Folder.FONTS_DIR


class TextInputBox:
    def __init__(self, position: tuple[int, int], title: str, scale: float = 0):
        super().__init__()

        self.input_text: str = ""
        self.position = position

        self._init_image(scale)

        scale = scale if scale else 1
        self._init_title_text(title, scale)
        self._init_input_text_object(scale)

    def _init_image(self, scale: float):
        self._image: Surface = image_handler.load_image("text_box_narrow_titled.png")

        if scale:
            self._image = image_handler.scale_image(self._image, scale)

    def _init_title_text(self, title: str, scale: float):
        title_font: Font = pygame.font.Font(os.path.join(FONTS_DIR, "Cinzel-Medium.ttf"),
                                            int(64 * scale))

        self._title_text_object = TextObject(title, (0, 0, 0), title_font)
        self._align_text_object(self._title_text_object, scale, height=30)

    def _init_input_text_object(self, scale: float):
        input_font: Font = pygame.font.Font(os.path.join(FONTS_DIR, "Cinzel-Medium.ttf"),
                                            int(88 * scale))

        # FIXME Temporary test variable
        self.input_text = "QWERTYUU ASDFLKJG"
        self._input_text_object = TextObject(self.input_text, (0, 0, 0), input_font)

        self._align_text_object(self._input_text_object, scale, height=130)

    def _align_text_object(self, text_object: TextObject, scale: float, height: int):
        x: int = self.position[0]
        y: int = self.position[1]
        x: int = x + self._image.get_width() // 2 - text_object.surface.get_width() // 2
        y: int = y + int(height * scale) - text_object.surface.get_height() // 2
        text_object.location = (x, y)

    def draw(self, surface: Surface):
        surface.blit(self._image, self.position)
        surface.blit(self._title_text_object.surface, self._title_text_object.location)
        surface.blit(self._input_text_object.surface, self._input_text_object.location)

    # def update(self):
    #     for event in pygame.event.get():
