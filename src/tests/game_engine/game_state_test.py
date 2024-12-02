import unittest
from unittest.mock import patch

from game_engine import GameState


class GameStateTest(unittest.TestCase):

    def setUp(self):
        self.game_state = GameState(1280, 720)

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

    def test_populate_level_with_gems_increases_gem_count(self):
        self.game_state.populate_level_with_gems(4)
        self.assertEqual(4, len(self.game_state.gems))
