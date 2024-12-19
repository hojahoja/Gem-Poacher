from typing import Iterator

import pygame
from pygame import Surface
from pygame.font import Font

from game_engine.game_state import GameState
from ui.text_object import TextObject

GAME_OVER_SCREEN: str = "game_over_screen"
GAME_OVER: str = "game_over"
END_OPTIONS: str = "end_options"

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
        self._create_game_over_text_objects()

    def _create_text_states(self):
        """Creates and initializes the text states dictionary.

        This method sets up the `text_states` attribute with initial values
        for the player's level, lives, and points. The level is set to 0,
        while the lives and points are obtained from the current game state.
        """
        self.text_states: dict[str: int] = {
            LEVEL: self.game_state.level,
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
        font_color: tuple[int, int, int] = (230, 215, 165)

        level_object: TextObject = TextObject(f"Level: {self.game_state.level}", font_color, font,
                                              (self.width - 290, self.height - 30))
        lives_object: TextObject = TextObject(f"Lives: {self.game_state.player.lives}", font_color,
                                              font, (self.width - 390, self.height - 30))
        points_object: TextObject = TextObject(f"Points {self.game_state.points}", font_color, font,
                                               (self.width - 190, self.height - 30))

        self.text_objects[GAMEPLAY] = {
            LEVEL: level_object,
            LIVES: lives_object,
            POINTS: points_object
        }

    def _create_game_over_text_objects(self):
        font: Font = self.fonts[GAME_OVER_SCREEN]

        font_color: tuple[int, int, int] = (200, 0, 0)
        game_over_object: TextObject = TextObject("GAME OVER", font_color, font)
        end_options_object: TextObject = TextObject("F1: NEW GAME  ESC: QUIT GAME", font_color,
                                                    font)

        end_surface: Surface = end_options_object.surface
        game_over_surface: Surface = game_over_object.surface

        end_options_object.location = ((self.width - end_surface.get_width()) // 2,
                                       (self.height - end_surface.get_height()) // 2)

        game_over_object.location = ((self.width - game_over_surface.get_width()) // 2,
                                     (self.height - game_over_surface.get_height()) // 2 + 100)

        self.text_objects[GAME_OVER_SCREEN] = {
            GAME_OVER: game_over_object,
            END_OPTIONS: end_options_object
        }

    def get_text_surface_group(self, group_name: str) -> Iterator[tuple[Surface, tuple[int, int]]]:
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
        for text_object in self.text_objects[group_name].values():
            yield text_object.surface, text_object.location

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
        self.text_objects[group_name][object_name].update(text)

    def _create_font_types(self):
        """Creates and adds font types to the controller."""
        self.fonts[GAMEPLAY] = pygame.font.SysFont("Arial", 24)
        self.fonts[GAME_OVER_SCREEN] = pygame.font.SysFont("Arial", 48)

    def update(self):
        """Callable method to update the text objects in the UI.

        Checks whether relevant game state values have changed and calls a method
        to update the changed text objects.
        """
        current_lives: int = self.game_state.player.lives
        if self.text_states[LIVES] != current_lives:
            self._update_text_object(GAMEPLAY, LIVES, f"Lives: {current_lives}")
            self.text_states[LIVES] = current_lives

        current_points: int = self.game_state.points
        if self.text_states[POINTS] != current_points:
            self._update_text_object(GAMEPLAY, POINTS, f"Points: {current_points}")
            self.text_states[POINTS] = current_points

        current_level: int = self.game_state.level
        if self.text_states[LEVEL] != current_level:
            self._update_text_object(GAMEPLAY, LEVEL, f"Level: {current_level}")
            self.text_states[LEVEL] = current_level
