import os
from typing import AnyStr

import pygame
from pygame import Rect

type PygameSurface = pygame.Surface | pygame.SurfaceType


class Player(pygame.sprite.Sprite):

    def __init__(self, x: int = 0, y: int = 0, lives: int = 9):
        super().__init__()
        self._lives = lives

        self._load_images()
        self.direction: str = "right"
        self.image: PygameSurface = self._images["right"]

        self.rect: Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _load_images(self):
        base_path: AnyStr = os.path.dirname(__file__)
        moving_right: PygameSurface = pygame.image.load(
            os.path.join(base_path, "..", "assets", "thief_right_facing.png"))
        self._images: dict[str, PygameSurface] = {
            "right": moving_right,
            "left": pygame.transform.flip(moving_right, True, False)
        }

    def injure(self):
        self._lives -= 1

    @property
    def lives(self):
        return self._lives

    def update(self):
        if self.direction == "right":
            self.image = self._images["right"]
        elif self.direction == "left":
            self.image = self._images["left"]
