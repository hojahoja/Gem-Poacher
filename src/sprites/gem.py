import pygame

from utilities import image_handler


# Docstrings in this class were written with the help of AI generation.
class Gem(pygame.sprite.Sprite):
    """Enemy pygame sprite.

    The Gem class manages the graphical representation of a gem object in the
    game environment. It initializes the gem's image and sets its initial
    position on the screen. The class also provides access to the gem's
    value, allowing other game components to interact with it accordingly.

    Attributes:
        _value: The point value of the gem.
        image: Pygame image surface that is currently used to render the sprite.
        rect: Pygame rect object gets it's position and size from image.
    """

    def __init__(self, x: int = 0, y: int = 0, value: int = 100):
        """Initializes the enemy sprite.

        Represents a gem, initialized with a position and value attribute.
        Handles image loading and positioning the object on the screen.

        Args:
            x: x coordinate value for the sprite's starting position.
            y: y coordinate value for the sprite's starting position.
            value: The value associated with the gem, defaults to 100.
        """
        super().__init__()
        self._value = value
        self.image: pygame.Surface = image_handler.load_image("sapphire.png")

        self.rect: pygame.Rect = self.image.get_rect()
        self.place(x, y)

    @property
    def value(self):
        """Property method for the gem's value attribute."""
        return self._value

    def place(self, x: int, y: int):
        """Directly places the sprite at the given coordinates."

        Args:
            x: x coordinate value for placing the sprite manually.
            y: y coordinate value for placing the sprite manually.
        """
        self.rect.x = x
        self.rect.y = y
