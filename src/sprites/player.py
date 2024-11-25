import pygame
from pygame import Surface

import image_handler


class Player(pygame.sprite.Sprite):

    def __init__(self, x: int = 0, y: int = 0, lives: int = 9):
        super().__init__()
        self._lives = lives

        self._load_images()
        self.direction: str = "right"
        self.image: Surface = self._images["right"]

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _load_images(self):
        moving_right: Surface = image_handler.load_image("thief_right_facing.png")

        self._images: dict[str, Surface] = {
            "right": moving_right,
            "left": image_handler.reverse_image_horizontally(moving_right),
        }

    def injure(self):
        self._lives -= 1

    @property
    def lives(self) -> int:
        return self._lives

    def update(self):
        if self.direction == "right":
            self.image = self._images["right"]
        elif self.direction == "left":
            self.image = self._images["left"]
