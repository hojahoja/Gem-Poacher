import pygame


class Clock:
    """Class that encapsulates the functionality of pygame.time.Clock.

    Attributes:
        _clock: Instance of pygame.time.Clock.
    """

    def __init__(self, fps: int = 120):
        """Initialize the clock."""
        self._fps = fps
        self._clock: pygame.time.Clock = pygame.time.Clock()

    @property
    def fps(self):
        return self._fps

    def set_framerate(self, fps: int):
        self._fps = fps

    def tick(self):
        """Gives access to pygame.time.clock.tick method.

        Args:
            fps: Set how many ticks per second.
        """
        self._clock.tick(self._fps)
