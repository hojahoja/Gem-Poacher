import unittest
from unittest.mock import patch

import pygame
from pygame.sprite import Group

from game_engine import GameLogic


class StubGem(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, value=100):
        super().__init__()
        self.value = value
        self.image = pygame.Surface((40, 40))

        self.rect = self.image.get_rect()
        self.place(x, y)

    def place(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y


class StubPlayer(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, lives=2):
        super().__init__()
        self.vulnerable = True
        self.lives = lives
        self.image = pygame.Surface((50, 50))
        self.direction = "right"
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def injure(self):
        self.lives -= 1


class StubGameState:
    def __init__(self):
        self.height = 720
        self.width = 1280
        self.player = StubPlayer(lives=2)
        self.gems = Group()
        self.enemies = Group()
        self.sprites = Group()
        self.points = 0

        self.gems.add(StubGem(800, 800, ))
        self.sprites.add(self.player)
        self.sprites.add(self.gems)

        self.populate_called = 0

    def populate_level_with_gems(self, amount: int = 1):
        self.populate_called += 1

    def add_points(self, value):
        self.points += value


class GameLogicTest(unittest.TestCase):

    def setUp(self):
        self.game_state = StubGameState()
        self.player = self.game_state.player

        self.player.rect.center = (420, 420)

        self.game_logic = GameLogic(self.game_state)

    def test_moves_player_position_correctly(self):
        self.assertEqual((420, 420), self.player.rect.center)

        self.game_logic.move_player(520, 680)
        self.assertEqual((520, 680), self.player.rect.center)

    def test_move_player_changes_direction_right(self):
        self.assertEqual("right", self.player.direction)
        self.game_logic.move_player(410, 420)
        self.assertEqual("left", self.player.direction)

    def test_move_player_changes_direction_left(self):
        self.player.direction = "left"
        self.game_logic.move_player(430, 420)
        self.assertEqual("right", self.player.direction)

    def test_right_direction_doesnt_change_when_moving_toward_right(self):
        self.game_logic.move_player(430, 420)
        self.assertEqual("right", self.player.direction)

    def test_left_direction_doesnt_change_when_moving_toward_left(self):
        self.game_logic.move_player(400, 420)
        self.assertEqual("left", self.player.direction)

    def test_moving_vertically_doesnt_change_direction(self):
        self.game_logic.move_player(420, 300)
        self.assertEqual("right", self.player.direction)

        self.game_logic.move_player(420, 500)
        self.assertEqual("right", self.player.direction)

    def test_border_collision_works_for_left_side(self):
        self.game_logic.move_player(0, 100)
        collides = self.game_logic.detect_border_collision(self.player)
        self.assertTrue(collides)

    def test_border_collision_works_for_right_side(self):
        self.game_logic.move_player(1280, 200)
        collides = self.game_logic.detect_border_collision(self.player)
        self.assertTrue(collides)

    def test_border_collision_works_for_top_side(self):
        self.game_logic.move_player(100, 0)
        collides = self.game_logic.detect_border_collision(self.player)
        self.assertTrue(collides)

    def test_border_collision_works_for_bottom(self):
        self.game_logic.move_player(100, 720)
        collides = self.game_logic.detect_border_collision(self.player)
        self.assertTrue(collides)

    def test_no_collision_detect_when_player_is_not_at_the_border(self):
        collides = self.game_logic.detect_border_collision(self.player)
        self.assertFalse(collides)

    def test_player_wall_collison_triggers_player_damage(self):
        self.game_logic.move_player(0, 100)
        self.game_logic.update()
        self.assertEqual(1, self.player.lives)

    def test_moving_player_without_hitting_walls_doesnt_damage_player(self):
        self.game_logic.move_player(200, 200)
        self.game_logic.update()
        self.assertEqual(2, self.player.lives)

    def test_player_gem_collison_triggers_gem_removal(self):
        gems = self.game_state.gems
        self.assertEqual(1, len(gems))
        self.game_logic.move_player(800, 800)
        self.game_logic.update()
        self.assertEqual(0, len(gems))

    def test_player_gem_collision_adds_points_to_game_state(self):
        self.game_logic.move_player(800, 800)
        self.game_logic.update()
        points = self.game_state.points
        self.assertEqual(100, points)

    def test_empty_gem_group_triggers_populate_gems(self):
        self.assertEqual(0, self.game_state.populate_called)
        self.game_logic.move_player(800, 800)
        self.game_logic.update()
        self.assertEqual(1, self.game_state.populate_called)

    def test_player_taking_damage_activates_invulnerability(self):
        self.game_logic.move_player(0, 300)
        self.game_logic.update()
        self.assertFalse(self.player.vulnerable)

    def test_player_becomes_vulnerable_after_enough_time_has_passed(self):
        self.game_logic.activate_player_invulnerability()
        self.game_logic.update()
        self.assertFalse(self.player.vulnerable)
        with patch.object(pygame.time, "get_ticks") as mock_tick:
            mock_tick.return_value = 1001
            self.game_logic.update()

        self.assertTrue(self.player.vulnerable)

    def test_player_doesnt_take_damage_when_invulnerable(self):
        self.game_logic.activate_player_invulnerability()
        self.game_logic.move_player(0, 200)
        self.game_logic.update()
        self.assertEqual(2, self.player.lives)
