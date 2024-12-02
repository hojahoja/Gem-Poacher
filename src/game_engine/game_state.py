from random import randint

from pygame.sprite import Group

from sprites import Player, Gem

type Character = Player


class GameState:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.player: Player = Player()
        self.gems: Group = Group()
        self.sprites: Group = Group()

        self.sprites.add(self.player)

    def _generate_random_spawn_point(self, game_object: Gem) -> tuple[int, int]:
        end_x: int = game_object.rect.width
        end_y: int = game_object.rect.height
        x: int = randint(1, self.width - end_x)
        y: int = randint(1, self.height - end_y)

        return x, y

    def populate_level_with_gems(self, amount: int = 1):
        for _ in range(amount):
            gem: Gem = Gem()
            coord: tuple[int, int] = self._generate_random_spawn_point(gem)
            gem.place(*coord)
            self.gems.add(gem)

        self.sprites.add(self.gems)
