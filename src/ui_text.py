from typing import Iterator

import pygame
from pygame import Surface
from pygame.font import Font

from game_engine.game_state import GameState

type TextObject = tuple[Surface, tuple[int, int]]

GAMEPLAY: str = "gameplay"
"""Constant for the name of the gameplay text group and font."""
LIVES: str = "lives"
"""Constant for the name of the lives text object."""
POINTS: str = "points"
"""Constant for the name of the points text object."""
LEVEL: str = "level"
"""Constant for the name of the level text object."""


# Docstrings in this class were written with the help of AI generation.
class UITextController:
    """Manages the text representation for the user interface in the game

    Provides facilities for creating and updating text components in the game UI by
    leveraging various fonts and maintaining states for different text types. Allows
    retrieval of text objects to be rendered as part of the game display. Text objects
    are created and stored so that the game doesn't have to recreate every text Surface
    on every iteration of the game loop and instead updates them only when necessary.

    Attributes:
        game_state: Instance of the GameState class.
        width: The width of the game screen.
        height: The height of the game screen.
        text_states: A dictionary tracking the text values for different game aspects.
        fonts: A dictionary associating font names with their respective Font objects.
        text_objects: A dictionary to manage and organize text objects related to
            game states such as gameplay.
    """

    def __init__(self, game_state: GameState):
        """Initializes the UI text controller.

        Keeps reference to game state so it knows what information to render on dynamic
        text objects. Creates the dictionaries which are used to keep track of various
        Fonts text objects and their values.

        Args:
            game_state: The current game state from which text parameters and configurations
                are derived.
        """
        self.game_state: GameState = game_state
        self.width: int = self.game_state.width
        self.height: int = self.game_state.height
        self.text_states: dict[str, str | int] = {}

        self.fonts: dict[str, Font] = {}
        self.text_objects: dict[str, dict[str, TextObject]] = {}

        self._create_text_states()
        self._create_font_types()
        self._create_level_text_objects()

    def _create_text_states(self):
        """Creates and initializes the text states dictionary.

        This method sets up the `text_states` attribute with initial values
        for the player's level, lives, and points. The level is set to 0,
        while the lives and points are obtained from the current game state.
        """
        self.text_states = {
            LEVEL: 0,
            LIVES: self.game_state.player.lives,
            POINTS: self.game_state.points,
        }

    def _create_level_text_objects(self):
        """Create level text objects for the game display.

        This function initializes and sets up the surfaces for displaying
        gameplay information, such as level, lives, and points, on the game
        screen. text objects are tuples that contain the rendered text Surface as the
        first value and x, y coordinates as the second value. The text objects for
        gameplay are stored in the `self.text_objects` dictionary with predefined keys
        for easy reference during the game loop.
        """
        font: Font = self.fonts[GAMEPLAY]

        # TODO level functionality
        level_text: Surface = font.render("Level 1", True, (255, 0, 0))
        lives_text: Surface = font.render(f"Lives: {self.game_state.player.lives}", True,
                                          (255, 0, 0))
        points_text: Surface = font.render(f"Points {self.game_state.points}", True,
                                           (255, 0, 0))

        self.text_objects[GAMEPLAY] = {
            LEVEL: (level_text, (self.width - 200, 10)),
            LIVES: (lives_text, (self.width - 320, 10)),
            POINTS: (points_text, (self.width - 200, self.height - 30))
        }

    def get_text_surface_group(self, group_name: str) -> Iterator[TextObject]:
        """Returns an iterator over text `Surface` instances in the specified group.

        This method retrieves all TextObject tuples associated with the
        provided group name. It returns an iterator to traverse through these
        objects.

        Args:
            group_name: The name of the group for which TextObject
                instances are to be retrieved.

        Returns:
            Iterator: An iterator over the TextObject tuples in the specified group.
        """
        return iter(self.text_objects[group_name].values())

    def _update_text_object(self, group_name: str, object_name: str, text: str):
        """Updates a text object within a specified group

        This method creates a new text Surface with the specified `Font` object
        and replace the existing one with the new Surface


        Args:
            group_name: The name of the group where the text object is located.
            object_name: The name of the text object to be updated within the group.
            text: The new text to render and update within the specified text
                object.
        """
        font: Font = self.fonts[group_name]
        surface: Surface = font.render(text, True, (255, 0, 0))
        location: tuple[int, int] = self.text_objects[group_name][object_name][1]
        self.text_objects[group_name][object_name] = (surface, location)

    def _create_font_types(self):
        """Creates and adds font types to the controller."""
        self.fonts[GAMEPLAY] = pygame.font.SysFont("Arial", 24)

    def update(self):
        """Callable method to update the text objects in the UI.

        Checks whether relevant game state values have changed and calls a method
        to update the changed text objects.
        """
        current_lives: int = self.game_state.player.lives
        if self.text_states[LIVES] != current_lives:
            self._update_text_object(GAMEPLAY, LIVES, f"Lives: {current_lives}")

        current_points: int = self.game_state.points
        if self.text_states[POINTS] != current_points:
            self._update_text_object(GAMEPLAY, POINTS, f"Points: {current_points}")
