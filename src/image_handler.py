import os
from typing import AnyStr

import pygame
from pygame import Surface

base_path: AnyStr = os.path.dirname(__file__)


def load_image(filename: str) -> Surface:
    image: Surface = pygame.image.load(
        os.path.join(base_path, "assets", filename))
    image.convert_alpha()

    return image


def reverse_image_horizontally(image: Surface) -> Surface:
    return pygame.transform.flip(image, True, False)


def create_opaque_image(filename: str) -> Surface:
    image: Surface = load_image(filename).convert_alpha()
    image.set_alpha(128)
    return image
