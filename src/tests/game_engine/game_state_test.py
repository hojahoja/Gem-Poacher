import unittest
from unittest.mock import patch

import pygame

from game_engine import GameState


class GameStateTest(unittest.TestCase):

    def setUp(self):
        self.player_patch = patch("sprites.player.image_handler").start()
        self.game_state = GameState(1280, 720)

    def tearDown(self):
        self.player_patch.stop()

    def test_game_state_initializes_properly(self):
        self.assertEqual(1280, self.game_state.width)
        self.assertEqual(720, self.game_state.height)

    def test_game_state_starts_with_no_gems(self):
        self.assertEqual(0, len(self.game_state.gems))

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

    @patch("sprites.enemy.image_handler.load_image")
    def test_spawn_enemy_creates_an_enemy(self, mock_surface):
        mock_surface.return_value = pygame.Surface((32, 40))

        for i in range(2):
            with self.subTest(enemy_count=i + 1):
                self.game_state.spawn_enemy()
                self.assertEqual(i + 1, len(self.game_state.enemies))

    @patch("sprites.enemy.image_handler.load_image")
    def test_spawn_enemy_creates_an_enemy_with_correct_speed_value(self, mock_surface):
        mock_surface.return_value = pygame.Surface((32, 40))

        self.game_state.spawn_enemy(50)
        enemy = self.game_state.enemies.sprites()[0]
        self.assertEqual(50, enemy.speed)
