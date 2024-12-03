import pygame
from pygame import Surface

import image_handler


class Player(pygame.sprite.Sprite):

    def __init__(self, x: int = 0, y: int = 0, player_lives: int = 9):
        super().__init__()
        self._lives = player_lives

        self._load_images()
        self.direction: str = "right"
        self.image: Surface = self._images["right"]
        self._vulnerable: bool = True

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _load_images(self):
        moving_right: Surface = image_handler.load_image("thief_right_facing.png")
        damaged_moving_right: Surface = image_handler.create_opaque_image("thief_right_facing.png")
        self._images: dict[str, Surface] = {
            "right": moving_right,
            "left": image_handler.reverse_image_horizontally(moving_right),
            "damaged_right": damaged_moving_right,
            "damaged_left": image_handler.reverse_image_horizontally(damaged_moving_right),
        }

    def injure(self):
        if self.lives > 0:
            self._lives -= 1

    def update(self):
        if self.direction == "right" and self.vulnerable:
            self.image = self._images["right"]
        elif self.direction == "left" and self.vulnerable:
            self.image = self._images["left"]
        elif self.direction == "right" and not self.vulnerable:
            self.image = self._images["damaged_right"]
        elif self.direction == "left" and not self.vulnerable:
            self.image = self._images["damaged_left"]

    @property
    def lives(self) -> int:
        return self._lives

    @property
    def vulnerable(self) -> bool:
        return self._vulnerable

    @vulnerable.setter
    def vulnerable(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Vulnerability must be a boolean")
        self._vulnerable = value
