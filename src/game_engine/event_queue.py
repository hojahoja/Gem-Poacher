import pygame


class EventQueue:
    """Encapsulates the pygame method for getting pygame events."""

    def get(self):
        """Method for getting pygame events.

        Returns: pygame event.

        """
        return pygame.event.get()
