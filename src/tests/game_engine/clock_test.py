import unittest
from unittest.mock import patch

import game_engine


class ClockTest(unittest.TestCase):

    @patch("pygame.time.Clock")
    def test_clock_initialized_properly(self, mock_clock):
        clock = game_engine.Clock()
        mock_clock.assert_called()

    @patch("pygame.time.Clock")
    def test_clock_tick(self, mock_clock):
        mock_instance = mock_clock.return_value
        clock = game_engine.Clock()
        clock.tick(120)

        mock_instance.tick.assert_called_with(120)
