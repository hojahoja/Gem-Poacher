import os
from typing import AnyStr

import pygame
from pygame import Surface

base_path: AnyStr = os.path.dirname(__file__)


def load_image(filename: str) -> Surface:
    image: Surface = pygame.image.load(
        os.path.join(base_path, "assets", filename))

    return image


def reverse_image_horizontally(image: Surface) -> Surface:
    return pygame.transform.flip(image, True, False)


# TODO for "animating" player damage
def create_opaque_image() -> Surface:
    pass
