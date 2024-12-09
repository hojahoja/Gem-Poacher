import os
from typing import AnyStr

import pygame
from pygame import Surface

# Docstrings in this module were written with the help of AI generation.
base_path: AnyStr = os.path.dirname(__file__)
"""Constant for the Base path of the project."""


def load_image(filename: str) -> Surface:
    """
    Loads an image from the specified filename and converts it to have an
    alpha channel. This ensures that the image can support transparency. It
    utilizes the `pygame` library for loading and processing the image data.

    Args:
        filename: The name of the file to be loaded, including its extension.

    Returns:
        A `Surface` object containing the loaded image with alpha transparency
        enabled.
    """
    image: Surface = pygame.image.load(
        os.path.join(base_path, "assets", filename))
    image.convert_alpha()

    return image


def reverse_image_horizontally(image: Surface) -> Surface:
    """Reverse an image horizontally using the pygame library.

    Args:
        image: A pygame Surface object representing the image to be
        reversed horizontally.

    Returns:
        Surface: A new pygame Surface object that is a horizontally flipped
        version of the input image.
    """
    return pygame.transform.flip(image, True, False)


def create_opaque_image(filename: str) -> Surface:
    """Creates an opaque image from the given filename.

    The function loads an image file, converts it to include alpha
    transparency, and sets its opacity level to 128 to make the image appear
    semi-transparent.

    Args:
        filename: The path to the image file to be processed.

    Returns:
        Surface: The processed image with adjusted opacity.
    """
    image: Surface = load_image(filename).convert_alpha()
    image.set_alpha(128)
    return image
