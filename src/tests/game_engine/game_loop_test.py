import unittest
from unittest.mock import Mock

import pygame

from game_engine import GameLoop


class GameLoopTest(unittest.TestCase):

    def setUp(self):
        self.game_logic = Mock()
        self.renderer = Mock()
        self.clock = Mock()

        self.event_queue = Mock()
        self.events = [pygame.event.Event(pygame.QUIT)]
        self.event_queue.get.return_value = self.events

        self.game_loop = GameLoop(self.game_logic, self.renderer, self.clock, self.event_queue)

    def test_game_loop_stops_on_event_quit(self):
        self.game_loop.run()

    def test_mouse_motion_causes_game_logic_to_the_move_player(self):
        mouse_event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (300, 300)})
        self.events.insert(0, mouse_event)

        self.game_loop.run()
        self.game_logic.move_player.assert_called_once_with(300, 300)

    def test_run_calls_renderer_render(self):
        self.game_loop.run()
        self.renderer.render.assert_called_once()

    def test_run_calls_clock_tick(self):
        self.game_loop.run()
        self.clock.tick.assert_called_once_with(120)

    def test_run_calls_game_logic_update(self):
        self.game_loop.run()
        self.game_logic.update.assert_called_once()
