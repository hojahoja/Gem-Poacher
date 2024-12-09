import pygame


class Clock:
    """Class that encapsulates the functionality of pygame.time.Clock.

    Attributes:
        _clock: Instance of pygame.time.Clock.
    """

    def __init__(self):
        """Initialize the clock."""
        self._clock = pygame.time.Clock()

    def tick(self, fps: int):
        """Gives access to pygame.time.clock.tick method.

        Args:
            fps: Set how many ticks per second.
        """
        self._clock.tick(fps)
