import time
import unittest
from unittest.mock import Mock, call

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

    # This is here for manually making sure that the main loop runs infinitely
    # without having to write a multithreaded test.
    # def test_game_loop_doesnt_stop_if_theres_no_quit_event(self):
    #     self.events.pop()
    #     self.game_loop.run()

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
        self.clock.tick.assert_called_once()

    def test_run_calls_game_logic_update(self):
        self.game_logic.game_over = False
        self.game_loop.run()
        self.game_logic.update.assert_called_once()

    def test_run_doesnt_call_game_logic_update_when_game_is_over(self):
        self.game_logic.game_over = True
        self.game_loop.run()
        self.game_logic.update.assert_not_called()

    def test_reset_game_calls_correct_methods_on_f4_press(self):
        self.events.insert(0, pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_F4}))
        self.game_logic.start_new_game.reset_mock()
        self.game_loop.run()

        with self.subTest("game_logic.reset_game() is called once"):
            self.game_logic.reset_game.assert_called_once()

        with self.subTest("game_logic.start_new_game() is called twice"):
            self.game_logic.start_new_game.assert_has_calls([call(), call()])

    def test_loop_stops_when_esc_is_pressed(self):
        self.events.pop()
        self.events.insert(0, pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
        self.game_loop.run()

    def test_send_renderer_keys_that_are_not_f4_or_esc(self):
        press_space = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        self.events.insert(0, press_space)
        self.game_loop.run()
        self.renderer.adistribute_ui_events.ssert_called_once_with(press_space)
