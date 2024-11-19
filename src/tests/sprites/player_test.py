import unittest
from sprites.player import Player


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.player = Player(lives=2)

    def test_player_initializes_correctly(self):

        self.assertEqual(self.player.lives, 2)

    def test_player_loses_a_life_from_injury(self):
        self.player.injure()
        self.assertEqual(self.player.lives, 1)
