import sys

import pygame

from clock import Clock
from event_queue import EventQueue
from game_logic import GameLogic
from renderer import Renderer


class GameLoop:

    def __init__(self, game_logic: GameLogic, renderer: Renderer, clock: Clock,
                 event_queue: EventQueue):
        self._game_logic = game_logic
        self._renderer = renderer
        self._clock = clock
        self._event_queue = event_queue

    def run(self):
        while True:

            for event in self._event_queue.get():
                if event.type == pygame.MOUSEMOTION:
                    self._game_logic.move_player(event.pos[0], event.pos[1])

                if event.type == pygame.QUIT:
                    sys.exit()

            self._renderer.render()
            self._clock.tick(120)
            self._game_logic.update()
