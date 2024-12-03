import unittest
from unittest.mock import patch

from sprites.player import Player


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.image_handler_patcher = patch("sprites.player.image_handler")
        self.image_handler_patcher.start()
        self.player = Player(player_lives=2)

    def tearDown(self):
        self.image_handler_patcher.stop()

    def test_player_initializes_correctly(self):
        self.assertEqual(2, self.player.lives)

    def test_player_loses_a_life_from_injury(self):
        self.player.injure()
        self.assertEqual(1, self.player.lives)

    def test_player_lives_dont_drop_below_zero(self):
        self.player.vulnerable = False
        for _ in range(4):
            self.player.injure()

        self.assertEqual(0, self.player.lives)

    def test_update_returns_correct_value(self):
        with patch.dict(self.player._images, {
            "right": "right_substitute",
            "left": "left_substitute",
            "damaged_right": "damaged_right_substitute",
            "damaged_left": "damaged_left_substitute",
        }):
            test_cases = [
                ("right", True, "right_substitute"),
                ("left", True, "left_substitute"),
                ("right", False, "damaged_right_substitute"),
                ("left", False, "damaged_left_substitute"),
            ]
            for direction, vulnerability, expected_substitute_image in test_cases:
                with self.subTest(direction=direction, vulnerability=vulnerability):
                    self.player.direction = direction
                    self.player.vulnerable = vulnerability
                    self.player.update()
                    self.assertEqual(expected_substitute_image, self.player.image)

    def test_setting_incorrect_value_in_vulnerable_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.player.vulnerable = "LMAO"
