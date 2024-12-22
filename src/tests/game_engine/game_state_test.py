import unittest
from unittest.mock import patch

import pygame

from game_engine import GameState, game_state


class GameStateTest(unittest.TestCase):

    def setUp(self):
        self.player_patch = patch("sprites.player.image_handler")
        self.player_patch.start()

        self.enemy_patch = patch("sprites.enemy.image_handler.load_image")
        self.enemy_patch.start().return_value = pygame.Surface((32, 40))

        self.game_state = GameState(1280, 720, difficulty=0)

    def tearDown(self):
        self.player_patch.stop()
        self.enemy_patch.stop()

    def test_game_state_initializes_properly(self):
        self.assertEqual(1280, self.game_state.width)
        self.assertEqual(720, self.game_state.height)

    def test_game_state_starts_with_no_gems(self):
        self.assertEqual(0, len(self.game_state.gems))

    def test_correct_amount_of_lives_for_each_difficulty(self):

        test_cases = ((0, 12), (1, 6), (2, 4), (3, 3), (-1, 12))

        for difficulty, expected_lives in test_cases:
            with self.subTest(difficulty=difficulty, expected_lives=expected_lives):
                self.game_state = GameState(1280, 720, difficulty=difficulty, lives=12)
                self.assertEqual(expected_lives, self.game_state.player.lives)

    def test_manually_setting_difficulty_gives_correct_value(self):
        self.game_state.difficulty = 1
        self.assertEqual(1, self.game_state.difficulty)

    def test_level_gives_the_correct_level(self):
        self.assertEqual(1, self.game_state.level)

    def test_increase_level_increments_level_by_one(self):
        self.game_state.increase_level()
        self.game_state.increase_level()

        self.assertEqual(3, self.game_state.level)

    def test_player_losing_all_lives_leads_to_game_over(self):
        self.game_state = GameState(1280, 720, difficulty=-1, lives=1)
        self.game_state.player.injure()
        self.assertTrue(self.game_state.game_over)

    def test_game_is_not_over_when_player_still_has_lives(self):
        self.assertFalse(self.game_state.game_over)

    @patch("sprites.gem.Gem")
    def test_random_spawn_stays_within_bounds(self, mock_gem):
        mock_gem.rect.width = 30
        mock_gem.rect.height = 40
        self.game_state.width = 32
        self.game_state.height = 42

        expected = ((1, 1), (1, 2), (2, 1), (2, 2))
        spawns = (self.game_state._generate_random_spawn_point(mock_gem) for _ in range(10))

        for spawn in spawns:
            self.assertIn(spawn, expected)

    @patch("sprites.gem.image_handler.load_image")
    def test_populate_level_with_gems_increases_gem_count(self, mock_loader):
        mock_loader.return_value = pygame.Surface((32, 40))
        self.game_state.populate_level_with_gems(4)
        self.assertEqual(4, len(self.game_state.gems))

    def test_add_points_increases_game_logic_points(self):
        self.game_state.add_points(100)
        self.assertEqual(100, self.game_state.points)

    def test_add_points_cant_decrease_points(self):
        self.game_state.add_points(300)
        self.game_state.add_points(-100)
        self.assertEqual(300, self.game_state.points)

    def test_game_state_starts_with_no_enemies(self):
        self.assertEqual(0, len(self.game_state.enemies))

    def test_spawn_enemy_creates_an_enemy(self):

        for i in range(2):
            with self.subTest(enemy_count=i + 1):
                self.game_state.spawn_enemy()
                self.assertEqual(i + 1, len(self.game_state.enemies))

    def test_spawn_enemy_creates_an_enemy_with_correct_speed_value(self):

        self.game_state.spawn_enemy(50)
        enemy = self.game_state.enemies.sprites()[0]
        self.assertEqual(50, enemy.speed)

    def test_spawn_multiple_enemies_spawns_correct_amount_of_enemies(self):

        self.game_state.spawn_multiple_enemies(enemy_count=5, enemy_speed=1)
        self.assertEqual(5, len(self.game_state.enemies))

    def test_spawn_multiple_enemies_spawns_enemies_with_correct_speed(self):

        self.game_state.spawn_multiple_enemies(enemy_count=5, enemy_speed=4)
        for enemy in self.game_state.enemies:
            self.assertEqual(4, enemy.speed)

    def test_reset_game_state_creates_new_sprites(self):

        original_player = self.game_state.player
        original_enemies = self.game_state.enemies
        original_gems = self.game_state.gems
        original_sprite = self.game_state.sprites

        self.game_state.reset_game_state()

        with self.subTest(sprite="player"):
            self.assertNotEqual(original_player, self.game_state.player)

        with self.subTest(sprite="enemies"):
            self.assertNotEqual(original_enemies, self.game_state.enemies)

        with self.subTest(sprite="gems"):
            self.assertNotEqual(original_gems, self.game_state.gems)

        with self.subTest(sprite="sprites"):
            self.assertNotEqual(original_sprite, self.game_state.sprites)

    def test_reset_game_states_resset_game_variables(self):
        self.game_state.increase_level()
        self.game_state.increase_level()

        self.game_state.add_points(1000)

        self.game_state.reset_game_state()

        with self.subTest(game_state="level"):
            self.assertEqual(1, self.game_state.level)

        with self.subTest(game_state="points"):
            self.assertEqual(0, self.game_state.points)
