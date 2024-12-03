import pygame
from pygame import Surface, Rect

import image_handler

FRAME_SWAP_RATE: int = 167


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x: int = 0, y: int = 0, direction: tuple[int, int] = (1, 1), speed: int = 0):
        super().__init__()

        self.direction_x: int = direction[0]
        self.direction_y: int = direction[1]
        self.speed: int = speed

        self._load_images()
        self.image: Surface = self._frames[0]
        self.rect: Rect = self.image.get_rect()
        self.place(x, y)

        self.previous_frame_swap: int = 0
        self.current_frame: int = 0

    def _load_images(self):
        self._frames: list[Surface] = []
        for i in range(1, 4):
            self._frames.append(image_handler.load_image(f"ghost_frame_{i}.png"))

    def move(self):
        new_x: int = self.rect.centerx + self.direction_x * self.speed
        new_y: int = self.rect.centery + self.direction_y * self.speed
        self.rect.center = (new_x, new_y)

    def place(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        elapsed_time: int = pygame.time.get_ticks() - self.previous_frame_swap
        if elapsed_time > FRAME_SWAP_RATE:
            self.current_frame = (self.current_frame + 1) % 3
            self.image = self._frames[self.current_frame]
            self.previous_frame_swap = pygame.time.get_ticks()
