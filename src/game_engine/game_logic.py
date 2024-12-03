import pygame
from pygame.sprite import Group

from sprites import Player, Gem
from sprites.enemy import Enemy
from .game_state import GameState

type Character = Player | Enemy


class GameLogic:

    def __init__(self, game_state: GameState):
        self._game_state: GameState = game_state
        self.player: Player = game_state.player
        self.enemies: Group = game_state.enemies
        self._invulnerability_period: int = 1000
        self._invulnerability_period_start: int = 0

    def move_player(self, x: int = 0, y: int = 0):
        if x > self.player.rect.centerx:
            self.player.direction = "right"
        elif x < self.player.rect.centerx:
            self.player.direction = "left"

        self.player.rect.center = (x, y)

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()

    def _run_collision_checks(self):
        self._player_gem_collision(self._game_state.gems)
        self._player_wall_collision()
        self._player_enemy_collision()
        self._enemy_wall_collision()

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

    def _player_enemy_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self._player_damage_event_handler()

    def _enemy_wall_collision(self):
        for enemy in self.enemies:
            if self.detect_border_collision(enemy):
                if enemy.rect.left < 0:
                    enemy.direction_x = 1
                elif enemy.rect.right > self._game_state.width:
                    enemy.direction_x = -1

                if enemy.rect.top < 0:
                    enemy.direction_y = 1
                elif enemy.rect.bottom > self._game_state.height:
                    enemy.direction_y = -1

    def _player_damage_event_handler(self):
        if self.player.vulnerable:
            self.player.injure()
            self.activate_player_invulnerability()

    def activate_player_invulnerability(self):
        self.player.vulnerable = False
        self._invulnerability_period_start = pygame.time.get_ticks()

    def update(self):
        self.move_enemies()
        self._run_collision_checks()

        if not self._game_state.gems:
            self._game_state.populate_level_with_gems(5)

        elapsed_time: int = pygame.time.get_ticks() - self._invulnerability_period_start
        if elapsed_time > self._invulnerability_period:
            self.player.vulnerable = True

        self._game_state.sprites.update()
