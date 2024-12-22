import unittest
from unittest.mock import patch

import game_engine


class ClockTest(unittest.TestCase):
    def setUp(self):
        self.pygame_clock_patcher = patch("pygame.time.Clock")
        self.mock_clock = self.pygame_clock_patcher.start()
        self.clock = game_engine.Clock()

    def tearDown(self):
        self.pygame_clock_patcher.stop()

    def test_clock_gets_initialized_with_correct_fps(self):
        self.clock = game_engine.Clock(fps=10)
        self.assertEqual(self.clock.fps, 10)

    def test_clock_defaults_to_120_fps(self):
        self.assertEqual(self.clock.fps, 120)

    def test_clock_can_set_fps_manually(self):
        self.clock.set_framerate(20)
        self.clock.tick()
        self.mock_clock.return_value.tick.assert_called_with(20)

    def test_clock_initialized_properly(self):
        self.mock_clock.assert_called()

    def test_clock_tick(self):
        self.clock.tick()
        self.mock_clock.return_value.tick.assert_called_with(120)
