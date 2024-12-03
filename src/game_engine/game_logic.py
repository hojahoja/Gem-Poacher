import pygame

from sprites import Player, Gem
from .game_state import GameState

type Character = Player


class GameLogic:

    def __init__(self, game_state: GameState):
        self._game_state: GameState = game_state
        self.player: Player = game_state.player
        self._invulnerability_period: int = 1000
        self._invulnerability_period_start: int = 0

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

    def _player_gem_collision(self, gems):
        collided_gems: list[Gem] = pygame.sprite.spritecollide(self.player, gems, True)

        if collided_gems:
            for gem in collided_gems:
                self._game_state.add_points(gem.value)

    def _player_wall_collision(self):
        if self.detect_border_collision(self.player):
            self._player_damage_event_handler()

    def _player_damage_event_handler(self):
        if self.player.vulnerable:
            self.player.injure()
            self.activate_player_invulnerability()

    def activate_player_invulnerability(self):
        self.player.vulnerable = False
        self._invulnerability_period_start = pygame.time.get_ticks()

    def update(self):
        self._run_collision_checks()

        if not self._game_state.gems:
            self._game_state.populate_level_with_gems(5)

        elapsed_time: int = pygame.time.get_ticks() - self._invulnerability_period_start
        if elapsed_time > self._invulnerability_period:
            self.player.vulnerable = True

        self._game_state.sprites.update()
