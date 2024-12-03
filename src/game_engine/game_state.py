from random import randint, choice

from pygame.sprite import Group

from sprites import Player, Gem
from sprites.enemy import Enemy

type SpawnableObject = Gem | Enemy


class GameState:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.player: Player = Player()
        self.gems: Group = Group()
        self.enemies: Group = Group()
        self.sprites: Group = Group()
        self._points: int = 0

        self.sprites.add(self.player)

    @property
    def points(self):
        return self._points

    def _generate_random_spawn_point(self, game_object: SpawnableObject) -> tuple[int, int]:
        end_x: int = game_object.rect.width
        end_y: int = game_object.rect.height
        x: int = randint(1, self.width - end_x)
        y: int = randint(1, self.height - end_y)

        return x, y

    def add_points(self, points: int):
        if points >= 0:
            self._points += points

    def spawn_enemy(self, speed: int = 1):
        direction: tuple[int, int] = choice(((1, 1), (-1, 1), (1, -1), (-1, -1)))

        enemy: Enemy = Enemy(direction=direction, speed=speed)
        self._add_game_object_to_group(enemy, self.enemies)

        self.sprites.add(enemy)

    def _add_game_object_to_group(self, game_object: SpawnableObject, group: Group):
        coord: tuple[int, int] = self._generate_random_spawn_point(game_object)
        game_object.place(*coord)
        group.add(game_object)

    def populate_level_with_gems(self, amount: int = 1):
        for _ in range(amount):
            gem: Gem = Gem()
            self._add_game_object_to_group(gem, self.gems)

        self.sprites.add(self.gems)
