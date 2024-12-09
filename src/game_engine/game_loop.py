import pygame

from renderer import Renderer
from .clock import Clock
from .event_queue import EventQueue
from .game_logic import GameLogic


class GameLoop:
    """A class responsible for running the game loop.

    Attributes:
        self._game_logic: Instance of the GameLogic class.
        self._renderer: Instance of the Renderer class.
        self._clock: Instance of the Clock class.
        self._event_queue: Instance of the EventQueue class.
    """

    def __init__(self, game_logic: GameLogic, renderer: Renderer, clock: Clock,
                 event_queue: EventQueue):
        """Initialize the game loop"""
        self._game_logic = game_logic
        self._renderer = renderer
        self._clock = clock
        self._event_queue = event_queue

    def run(self):
        """Start the game loop and call update the game on every iteration.

        Checks the pygame event_queue to see if the mouse has been moved and calls game
        logic to move the player when mouse movement is detected. Responsible for
        calling clock ticks and updating the game logic and renderer. breaks the loop
        on quit event.
        """
        running = True
        self._game_logic.activate_player_invulnerability()
        # TODO remove test spawns
        for i in range(1, 3 + 1):
            self._game_logic._game_state.spawn_enemy(i)
        while running:

            for event in self._event_queue.get():
                if event.type == pygame.MOUSEMOTION:
                    self._game_logic.move_player(event.pos[0], event.pos[1])

                if event.type == pygame.QUIT:
                    running = False
                    break

            self._renderer.render()
            self._clock.tick(120)
            self._game_logic.update()
