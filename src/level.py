from pygame.rect import Rect
from pygame.sprite import Group

from sprites.player import Player

type character = Player


class Level:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.player: Player = Player()

        self.sprites: Group = Group()

        self._init_sprites()

    def detect_border_collision(self, entity: character) -> bool:
        if (entity.rect.left < 0 or
                entity.rect.right > self.width or
                entity.rect.top < 0 or
                entity.rect.bottom > self.height):
            return True
        return False

    def move_player(self, x: int = 0, y: int = 0):
        if x > self.player.rect.centerx:
            self.player.direction = "right"
        elif x < self.player.rect.centerx:
            self.player.direction = "left"

        self.player.rect.center = (x, y)

        self.player.update()

    def _init_sprites(self):
        self.sprites.add(self.player)
