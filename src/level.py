from random import randint

import pygame.sprite
from pygame.sprite import Group

from sprites import Gem, Player

type Character = Player


class Level:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.player: Player = Player()
        self.gems: Group = Group()
        self.sprites: Group = Group()

        self.sprites.add(self.player)

    def detect_border_collision(self, entity: Character) -> bool:
        if (entity.rect.left < 0 or
                entity.rect.right > self.width or
                entity.rect.top < 0 or
                entity.rect.bottom > self.height):
            return True
        return False

    def _generate_random_spawn_point(self, game_object: Gem) -> tuple[int, int]:
        end_x: int = game_object.rect.width
        end_y: int = game_object.rect.height
        x: int = randint(1, self.width - end_x)
        y: int = randint(1, self.height - end_y)

        return x, y

    def move_player(self, x: int = 0, y: int = 0):
        if x > self.player.rect.centerx:
            self.player.direction = "right"
        elif x < self.player.rect.centerx:
            self.player.direction = "left"

        self.player.rect.center = (x, y)

    def populate_level_with_gems(self, amount: int = 1):
        for _ in range(amount):
            gem: Gem = Gem()
            coord: tuple[int, int] = self._generate_random_spawn_point(gem)
            gem.place(*coord)
            self.gems.add(gem)

        self.sprites.add(self.gems)

    def _run_collision_checks(self):
        self._player_gem_collision()
        self._player_wall_collision()

    # TODO get points
    def _player_gem_collision(self):
        if pygame.sprite.spritecollide(self.player, self.gems, True):
            print("To be continued!")

    def _player_wall_collision(self):
        if self.detect_border_collision(self.player):
            self.player.injure()

    def update(self):
        self._run_collision_checks()
        if not self.gems:
            self.populate_level_with_gems(5)

        self.sprites.update()
