import pygame
from pygame import Surface

import image_handler


# Docstrings in this class were written with the help of AI generation.
class Player(pygame.sprite.Sprite):
    """Player pygame sprite.

    Attributes:
        _lives: Number of lives the player has.
        _images: Dictionary holding all player images.
        direction: The direction the player is facing. Options are "right" and "left".
        image: Pygame image surface that is currently used to render the sprite.
        rect: Pygame rect object gets it's position and size from image.
        _vulnerable: Boolean value indicating whether the player is currently vulnerable.
    """

    def __init__(self, x: int = 0, y: int = 0, player_lives: int = 9):
        """Initializes the player sprite.

        The player's initial position and number of lives can be configured upon creation.
        This class relies on images to represent the player in different
        directions, and initializes the player's direction to "right". The
        player's positional rectangle is also initialized, allowing for collision
        detection and boundary setting. The vulnerability attribute determines
        whether the player can currently take damage.

        Args:
            x: Initial x-coordinate of the player. Defaults to 0.
            y: Initial y-coordinate of the player. Defaults to 0.
            player_lives: Number of lives assigned to the player upon
                initialization. Defaults to 9.
        """
        super().__init__()
        self._lives = player_lives

        self._load_images()
        self.direction: str = "right"
        self.image: Surface = self._images["right"]
        self._vulnerable: bool = True

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _load_images(self):
        """Uses the image handler helper module to load and create images of the player.

        This method prepares the images required for rendering the character in various
        states such as moving to the right, moving to the left, and their corresponding
        damaged versions. The images are processed and stored in a dictionary for easy
        access within the application.
        """
        moving_right: Surface = image_handler.load_image("thief_right_facing.png")
        damaged_moving_right: Surface = image_handler.create_opaque_image("thief_right_facing.png")
        self._images: dict[str, Surface] = {
            "right": moving_right,
            "left": image_handler.reverse_image_horizontally(moving_right),
            "damaged_right": damaged_moving_right,
            "damaged_left": image_handler.reverse_image_horizontally(damaged_moving_right),
        }

    def injure(self):
        """Decreases the player's life count by one."""
        if self.lives > 0:
            self._lives -= 1

    def update(self):
        """Updates the image of an object based on its direction and vulnerability status.

        The method checks the current direction and vulnerability of the object to select
        the appropriate image. The object changes its image to represent its state,
        displaying either a normal or damaged appearance, depending on whether it is
        vulnerable or not.
        """
        if self.direction == "right" and self.vulnerable:
            self.image = self._images["right"]
        elif self.direction == "left" and self.vulnerable:
            self.image = self._images["left"]
        elif self.direction == "right" and not self.vulnerable:
            self.image = self._images["damaged_right"]
        elif self.direction == "left" and not self.vulnerable:
            self.image = self._images["damaged_left"]

    @property
    def lives(self) -> int:
        """Property method for the player's lives attribute."""
        return self._lives

    @property
    def vulnerable(self) -> bool:
        """Property method for the player's vulnerability attribute.'"""
        return self._vulnerable

    @vulnerable.setter
    def vulnerable(self, value: bool):
        """Sets the player's vulnerability status to either True or False.

        Args:
            value: The vulnerability status to be set. Must be a boolean
            indicating the object's vulnerability state.

        Raises:
            ValueError: If the provided value is not a boolean.
        """
        if not isinstance(value, bool):
            raise ValueError("Vulnerability must be a boolean")
        self._vulnerable = value
