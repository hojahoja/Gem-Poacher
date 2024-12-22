import os

import pygame
from pygame import Surface

import utilities.constants

# Docstrings in this module were written with the help of AI generation.
IMAGES_DIR: str = utilities.constants.Folder.IMAGES_DIR
"""Constant for the Base path of the assets directory."""


def load_image(filename: str, alpha: bool = True, size: tuple[int, int] | None = None) -> Surface:
    """
    Loads an image from the specified filename and converts it to have an
    alpha channel. This ensures that the image can support transparency. It
    utilizes the `pygame` library for loading and processing the image data.

    Args:
        filename: The name of the file to be loaded, including its extension.
        alpha: A boolean flag indicating whether you want to preserve the alpha channel.
        size: Optional size parameter for resizing the image to specific dimensions.

    Returns:
        A `Surface` object containing the loaded image with alpha transparency
        enabled.
    """
    image: Surface = pygame.image.load(os.path.join(IMAGES_DIR, filename))
    if alpha:
        image.convert_alpha()
    else:
        image.convert()

    if size:
        image = pygame.transform.scale(image, size)

    return image


def scale_image(image: Surface, scale: float) -> Surface:
    """Scales an image to a new size based on the given scale factor.

    This function calculates the new dimensions of the image by multiplying the
    current width and height of the image by the specified scale factor. The scaled
    image is then returned.

    Args:
        image: The original image to be scaled.
        scale: The scale factor to resize the image by.

    Returns:
        Surface: The scaled image with adjusted dimensions.
    """
    new_width: int = int(image.get_width() * scale)
    new_height: int = int(image.get_height() * scale)
    return pygame.transform.scale(image, (new_width, new_height))


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
