import pygame
from pygame import Surface, Rect

from utilities import image_handler

FRAME_SWAP_RATE: int = 167
"""Constant rate value used for animating the Enemy sprite."""


class Enemy(pygame.sprite.Sprite):
    """Enemy pygame sprite.

    Attributes:
        direction_x: Horizontal movement direction. either a positive or a negative value.
        direction_y: Vertical movement direction. either a positive or a negative value.
        speed: Movement speed of the Enemy sprite.
        _frames: List holding all image surfaces that are used to render and animate the class
        image: Pygame image surface that is currently used to render the sprite.
        rect: Pygame rect object gets it's position and size from image.
        _previous_frame_swap: Timestamp for when the previous frame was swapped.
        _current_frame: The numerical index of currently rendered image frame.
    """

    def __init__(self, x: int = 0, y: int = 0, direction: tuple[int, int] = (1, 1), speed: int = 1):
        """Initializes the enemy sprite.

        Sets sprites initial coordinates and movement speed. The direction tuple represents
        movement directions of the sprite. sprite moves toward the right if the first value
        is positive and left if it's negative. Sprites moves down if the second value is
        positive and up if it's negative. Speed represents how many pixels per game loop
        iterations the sprites moves towards it's given directions.

        Args:
            x: x coordinate value for the sprite's starting position.
            y: y coordinate value for the sprite's starting position.
            direction: The direction the sprite moves to horizontally and vertically.
            speed: Movement speed of the Enemy sprite.
        """
        super().__init__()

        self.direction_x: int = direction[0]
        self.direction_y: int = direction[1]
        self.speed: int = speed

        self._load_images()
        self.image: Surface = self._frames[0]
        self.rect: Rect = self.image.get_rect()
        self.place(x, y)

        self._previous_frame_swap: int = 0
        self._current_frame: int = 0

    def _load_images(self):
        """Uses the image handler helper module to load images from the asset folder.

        Currently, loads 3 slightly different ghost images used for creating simple
        sprite animation. Images are kept inside the frames list.
        """
        self._frames: list[Surface] = []
        for i in range(1, 4):
            self._frames.append(image_handler.load_image(f"ghost_frame_{i}.png"))

    def move(self):
        """Updates the enemy sprite coordinates based on its direction and speed attributes."""
        new_x: int = self.rect.centerx + self.direction_x * self.speed
        new_y: int = self.rect.centery + self.direction_y * self.speed
        self.rect.center = (new_x, new_y)

    def place(self, x: int, y: int):
        """Directly places the sprite at the given coordinates.

        Args:
            x: x coordinate value for placing the sprite manually.
            y: y coordinate value for placing the sprite manually.
        """
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """Method for updating sprite animation.

        Meant to be called during every game iteration so the sprite's images can be
        updated over time. Checks whether enough time has passed between previous time
        the frame was swapped and swaps the frame when elapsed time is greater than the
        value determined by FRAME_SWAP_RATE module constant.
        """
        elapsed_time: int = pygame.time.get_ticks() - self._previous_frame_swap
        if elapsed_time > FRAME_SWAP_RATE:
            self._current_frame = (self._current_frame + 1) % 3
            self.image = self._frames[self._current_frame]
            self._previous_frame_swap = pygame.time.get_ticks()
