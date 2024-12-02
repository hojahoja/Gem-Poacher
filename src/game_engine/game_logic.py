import pygame

from sprites import Player
from .game_state import GameState

type Character = Player


class GameLogic:

    def __init__(self, game_state: GameState):
        self._game_state = game_state
        self.player: Player = game_state.player

    def move_player(self, x: int = 0, y: int = 0):
        if x > self.player.rect.centerx:
            self.player.direction = "right"
        elif x < self.player.rect.centerx:
            self.player.direction = "left"

        self.player.rect.center = (x, y)

    def _run_collision_checks(self):
        self._player_gem_collision(self._game_state.gems)
        self._player_wall_collision()

    def detect_border_collision(self, entity: Character) -> bool:
        if (entity.rect.left < 0 or
                entity.rect.right > self._game_state.width or
                entity.rect.top < 0 or
                entity.rect.bottom > self._game_state.height):
            return True
        return False

    # TODO get points
    def _player_gem_collision(self, gems):
        if pygame.sprite.spritecollide(self.player, gems, True):
            print("To be continued!")

    def _player_wall_collision(self):
        if self.detect_border_collision(self.player):
            self.player.injure()

    def update(self):
        self._run_collision_checks()

        if not self._game_state.gems:
            self._game_state.populate_level_with_gems(5)

        self._game_state.sprites.update()
