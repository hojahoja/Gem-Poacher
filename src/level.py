from pygame.sprite import Group

from sprites.player import Player


class Level:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.player: Player = Player(200, 200)

        self.sprites: Group = Group()

        self._init_sprites()

    def move_player(self, x: int = 0, y: int = 0):
        if x > self.player.rect.centerx:
            self.player.direction = "right"
        elif x < self.player.rect.centerx:
            self.player.direction = "left"

        self.player.rect.center = (x, y)

        self.player.update()

    def _init_sprites(self):
        self.sprites.add(self.player)
