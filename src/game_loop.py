import pygame

from clock import Clock
from event_queue import EventQueue
from level import Level
from renderer import Renderer


class GameLoop:

    def __init__(self, level: Level, renderer: Renderer, clock: Clock, event_queue: EventQueue):
        self._level = level
        self._renderer = renderer
        self._clock = clock
        self._event_queue = event_queue

    def run(self):
        while True:

            for event in self._event_queue.get():
                if event.type == pygame.MOUSEMOTION:
                    self._level.move_player(event.pos[0], event.pos[1])

                if event.type == pygame.QUIT:
                    exit()

            self._renderer.render()
            self._clock.tick(120)
