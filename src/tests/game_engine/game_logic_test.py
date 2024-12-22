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


class StubEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.times_moved = 0
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.direction_x = 1
        self.direction_y = 1

    def move(self):
        self.times_moved += 1


class StubGameState:
    def __init__(self):
        self.height = 720
        self.width = 1280
        self.player = StubPlayer(lives=2)
        self.gems = Group()
        self.enemies = Group()
        self.sprites = Group()
        self.points = 0
        self.level = 0
        self.difficulty = 0

        self.gems.add(StubGem(800, 800, ))
        self.enemies.add(StubEnemy())
        self.enemies.add(StubEnemy())
        self.sprites.add(self.player)
        self.sprites.add(self.gems)
        self.sprites.add(self.enemies)

        self.game_over = False
        self.populate_called = 0
        self.populate_amount = 0
        self.spawn_enemy_called = []
        self.reset_game_state_called = 0

    def populate_level_with_gems(self, amount: int = 1):
        self.populate_called += 1
        self.populate_amount = amount

    def add_points(self, value):
        self.points += value

    def increase_level(self):
        self.level += 1

    def spawn_enemy(self, speed=0):
        self.spawn_enemy_called.append(speed)

    def spawn_multiple_enemies(self, enemy_count, enemy_speed):
        for _ in range(enemy_count):
            self.spawn_enemy(enemy_speed)

    def reset_game_state(self):
        self.reset_game_state_called += 1
        self.player = StubPlayer(lives=2)
        self.enemies = Group()

        self.enemies.add(StubEnemy())
        self.enemies.add(StubEnemy())
        self.sprites.add(self.player)
        self.sprites.add(self.gems)
        self.sprites.add(self.enemies)


class GameLogicTest(unittest.TestCase):

    def setUp(self):
        self.game_state = StubGameState()
        self.player = self.game_state.player

        self.player.rect.center = (420, 420)

        self.game_logic = GameLogic(self.game_state, ((3, 6), (2, 3), (2, 3)))

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

    def test_player_collecting_the_last_gem_increases_level(self):
        self.game_state.level = 2
        self.game_logic.move_player(800, 800)
        self.game_logic.update()
        self.assertEqual(3, self.game_state.level)

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

    def test_game_logic_update_moves_the_enemies(self):
        self.game_logic.update()
        self.game_logic.update()

        for enemy in self.game_state.enemies.sprites():
            self.assertEqual(enemy.times_moved, 2)

    def test_game_enemy_wall_collision_moves_enemy_direction(self):
        enemy = self.game_logic.enemies.sprites()[0]
        enemy.rect.center = (100, 100)

        test_cases = [
            ((100, 0), (1, -1), (1, 1)),  # top collision
            ((0, 100), (-1, 1), (1, 1)),  # left
            ((100, self.game_state.height), (1, 1), (1, -1)),  # bottom
            ((self.game_state.width, 100), (1, 1), (-1, 1)),  # right
        ]

        for coordinates, initial_direction, expected_direction in test_cases:
            with self.subTest(coordinates=coordinates):
                enemy.rect.center = coordinates
                enemy.direction_x = initial_direction[0]
                enemy.direction_y = initial_direction[1]
                self.game_logic.update()
                enemy_direction = (enemy.direction_x, enemy.direction_y)

                self.assertEqual(expected_direction, enemy_direction)

    def test_enemy_doesnt_change_direction_if_it_doesnt_collide_with_a_wall(self):
        enemy = self.game_logic.enemies.sprites()[0]
        enemy.rect.center = (100, 100)
        enemy.direction_x = 1
        enemy.direction_y = 1

        self.game_logic.update()
        enemy_direction = (enemy.direction_x, enemy.direction_y)

        self.assertEqual((1, 1), enemy_direction)

    def test_enemy_player_collision_damages_player(self):
        self.player.lives = 5
        self.player.rect.center = (100, 100)
        self.game_logic.enemies.sprites()[0].rect.center = (100, 100)
        self.game_logic.update()

        self.assertEqual(4, self.player.lives)

    def test_initializes_correctly_without_custom_difficulty_setting(self):
        initial_length = len(self.game_logic._progression_options)

        self.game_state = StubGameState()
        self.player = self.game_state.player
        self.player.rect.center = (420, 420)
        self.game_logic = GameLogic(self.game_state)

        self.assertEqual(initial_length - 1, len(self.game_logic._progression_options))

    def test_initializes_correctly_with_custom_difficulty_setting(self):
        initial_length = len(self.game_logic._progression_options)

        self.game_state = StubGameState()
        self.player = self.game_state.player
        self.player.rect.center = (420, 420)
        self.game_logic = GameLogic(self.game_state, ((0, 0), (0, 0), (0, 0)))

        self.assertEqual(initial_length, len(self.game_logic._progression_options))

    def test_game_over_returns_correct_value(self):
        with self.subTest(game_over=False):
            self.assertFalse(self.game_logic.game_over)

        with self.subTest(game_over=True):
            self.game_state.game_over = True
            self.assertTrue(self.game_logic.game_over)

    def test_difficulty_progression_spawns_enemy_with_correct_speed(self):

        self.game_state.difficulty = -1
        test_cases = (
            (1, 1), (2, 2), (3, 2), (4, 2), (5, 3), (6, 3), (7, 3)
        )

        for level, expected_speed in test_cases:
            with self.subTest(level=level, expected_speed=expected_speed):
                self.game_state.gems.add(StubGem(800, 800, ))
                self.game_state.level = level
                self.game_logic.move_player(800, 800)
                self.game_logic.update()

                self.assertEqual(expected_speed, self.game_state.spawn_enemy_called.pop())

    def test_difficulty_progression_spawns_correct_amount_of_gems(self):

        self.game_state.difficulty = -1

        # ((3, 6), (2, 3), (2, 3)))
        test_cases = (
            (1, 5), (2, 5), (3, 6), (4, 7), (5, 9), (6, 10), (7, 11)
        )

        for level, expected_gem_count in test_cases:
            with self.subTest(level=level, expected_gem_count=expected_gem_count):
                self.game_state.gems.add(StubGem(800, 800, ))
                self.game_state.level = level
                self.game_logic.move_player(800, 800)
                self.game_logic.update()

                self.assertEqual(expected_gem_count, self.game_state.populate_amount)

    def test_start_new_game_starts_the_game_with_correct_conditions(self):
        self.game_logic.start_new_game()

        with self.subTest(expected_gem_count=5):
            self.assertEqual(5, self.game_state.populate_amount)

        with self.subTest(expected_enemy_count=3):
            self.assertEqual(3, len(self.game_state.spawn_enemy_called))

        with self.subTest(player_vulnerable=False):
            self.assertFalse(self.player.vulnerable)

    def test_reset_game_calls_reset_game_state_method(self):
        self.game_logic.reset_game()
        self.assertEqual(1, self.game_state.reset_game_state_called)

    def test_reset_game_resets_invulnerability_period(self):
        self.game_logic._invulnerability_period_start = 100
        self.game_logic.reset_game()
        self.assertEqual(0, self.game_logic._invulnerability_period_start)

    def test_reset_game_creates_new_player_character(self):
        player = self.game_state.player
        self.game_logic.reset_game()

        self.assertNotEqual(player, self.game_state.player)

    def test_reset_game_creates_new_enemy_group(self):
        enemies = self.game_state.enemies
        self.game_logic.reset_game()

        self.assertNotEqual(enemies, self.game_state.enemies)
