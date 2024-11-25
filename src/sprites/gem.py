import pygame

import image_handler


class Gem(pygame.sprite.Sprite):

    def __init__(self, x: int = 0, y: int = 0, value: int = 100):
        super().__init__()
        self._value = value
        self.image: pygame.Surface = image_handler.load_image("sapphire.png")

        self.rect: pygame.Rect = self.image.get_rect()
        self.place(x, y)

    def place(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y
