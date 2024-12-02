import unittest
from unittest.mock import patch

import pygame

from game_engine import EventQueue


class EventQueueTest(unittest.TestCase):

    @patch.object(pygame.event, "get")
    def test_event_queue_calls_pygame_event(self, mock_get):
        mock_get.return_value = pygame.KEYDOWN
        eq = EventQueue()
        event = eq.get()

        mock_get.assert_called_once()
        self.assertEqual(event, pygame.KEYDOWN)
