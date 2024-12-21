from pathlib import Path
from typing import Iterator

import pygame
from pygame import Surface
from pygame.font import Font

from game_engine.game_state import GameState
from ui.text_object import TextObject
from utilities.constants import Folder, TextObjects as Text, FontStyle as Style, TextGroup as Group
from utilities.score import Score
from utilities.score_manager import ScoreManager


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

    def __init__(self, game_state: GameState, score_manager: ScoreManager):
        """Initializes the UI text controller.

        Keeps reference to game state so it knows what information to render on dynamic
        text objects. Creates the dictionaries which are used to keep track of various
        Fonts text objects and their values.

        Args:
            game_state: The current game state from which text parameters and configurations
                are derived.
        """
        self.game_state: GameState = game_state
        self.score_manager: ScoreManager = score_manager
        self.width: int = self.game_state.width
        self.height: int = self.game_state.height
        self.text_states: dict[str, str | int] = {}

        self.fonts: dict[str, Font] = {}
        self.text_objects: dict[str, dict[str, TextObject]] = {}

        self._create_text_states()
        self._create_font_types()
        self._create_level_text_objects()
        self._create_game_over_text_objects()
        self._create_all_high_score_text_objects()

    def _create_text_states(self):
        """Creates and initializes the text states dictionary.

        This method sets up the `text_states` attribute with initial values
        for the player's level, lives, and points. The level is set to 0,
        while the lives and points are obtained from the current game state.
        """
        self.text_states: dict[str: int] = {
            Text.LEVEL: self.game_state.level,
            Text.LIVES: self.game_state.player.lives,
            Text.POINTS: self.game_state.points,
        }

    def _create_font_types(self):
        """Creates and adds font types to the controller."""
        cinzel_semi_bold: Path = Path(Folder.FONTS_DIR) / "Cinzel-SemiBold.ttf"
        cinzel_bold: Path = Path(Folder.FONTS_DIR) / "Cinzel-Bold.ttf"

        self.fonts[Style.GAMEPLAY] = pygame.font.SysFont("Arial", 24)
        self.fonts[Style.GAME_OVER_SCREEN] = pygame.font.Font(cinzel_bold, 14)
        self.fonts[Style.SCORE_TITLE] = pygame.font.Font(cinzel_semi_bold, 24)
        self.fonts[Style.SCORE] = pygame.font.SysFont("Courier New", 24)

    def _create_level_text_objects(self):
        """Create level text objects for the game display.

        This function initializes and sets up the surfaces for displaying
        gameplay information, such as level, lives, and points, on the game
        screen. text objects are tuples that contain the rendered text Surface as the
        first value and x, y coordinates as the second value. The text objects for
        gameplay are stored in the `self.text_objects` dictionary with predefined keys
        for easy reference during the game loop.
        """
        font: Font = self.fonts[Style.GAMEPLAY]
        font_color: tuple[int, int, int] = (230, 215, 165)

        level_object: TextObject = TextObject(f"Level: {self.game_state.level}", font_color, font,
                                              (self.width - 290, self.height - 30))
        lives_object: TextObject = TextObject(f"Lives: {self.game_state.player.lives}", font_color,
                                              font, (self.width - 390, self.height - 30))
        points_object: TextObject = TextObject(f"Points: {self.game_state.points}", font_color,
                                               font,
                                               (self.width - 190, self.height - 30))

        self.text_objects[Group.GAMEPLAY] = {
            Text.LEVEL: level_object,
            Text.LIVES: lives_object,
            Text.POINTS: points_object
        }

    def _create_game_over_text_objects(self):
        font: Font = self.fonts[Style.GAME_OVER_SCREEN]

        arrows: str = f"< F1: PREVIOUS {' ' * 98} F2: NEXT >"
        restart_exit: str = f"F4: NEW GAME {' ' * 13} ESC: QUIT GAME"
        font_color: tuple[int, int, int] = (0, 0, 0)
        game_over_object: TextObject = TextObject(arrows, font_color, font, (350, 555))
        end_options_object: TextObject = TextObject(restart_exit, font_color, font, (510, 555))

        self.text_objects[Group.GAME_OVER_SCREEN] = {
            Text.GAME_OVER: game_over_object,
            Text.END_OPTIONS: end_options_object
        }

    def _create_all_high_score_text_objects(self):
        font: Font = self.fonts[Style.SCORE_TITLE]
        font_color: tuple[int, int, int] = (0, 0, 0)
        title_text: str = f"{'#':<{9}}|{'Name':^{40}}|{'Level':^{9}}|   Points"
        title_object: TextObject = TextObject(title_text, font_color, font, (350, 160))

        self.text_objects[Group.HIGH_SCORES] = {
            Text.TITLE: title_object
        }

        self._create_score_text_objects()

    def _create_score_text_objects(self):
        scores: list[Score] = self.score_manager.get_scores()
        font = self.fonts[Style.SCORE]
        font_color = (0, 0, 0)

        for i, score in enumerate(scores, start=1):
            text: str = f"{i:<{4}}|{score.name[:20]:^{20}}|{score.level:<{6}}|{score.points:<}".upper()
            location: tuple[int, int] = (350, 200 + ((i - 1) % 10) * 34)
            text_object: TextObject = TextObject(text, font_color, font, location)
            self.text_objects[Group.HIGH_SCORES][f"position_{i}"] = text_object

    def _get_score_surface_group(self, first: int = 0, last: int = 10) -> Iterator[
        tuple[Surface, tuple[int, int]]]:

        last = min(last + 1, len(self.text_objects[Group.HIGH_SCORES]))
        first = first if first <= last else last - last % 10
        scores: dict[str, TextObject] = self.text_objects[Group.HIGH_SCORES]
        yield scores[Text.TITLE].surface, scores[Text.TITLE].location

        for i in range(first + 1, last):
            text_object: TextObject = scores[f"position_{i}"]
            yield text_object.surface, text_object.location

    def get_text_surface_group(self, group_name: str, first: int = 0, last: int = 10) -> Iterator[
        tuple[Surface, tuple[int, int]]]:
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

        if group_name == Group.HIGH_SCORES:
            yield from self._get_score_surface_group(first, last)

        else:
            for text_object in self.text_objects[group_name].values():
                yield text_object.surface, text_object.location

    def _update_score_board(self):
        if len(self.score_manager.get_scores()) == len(self.text_objects[Group.HIGH_SCORES]):
            self._create_score_text_objects()

    def _update_text_object(self, group_name: str, object_name: str, text: str, state: int):
        """Updates a text object within a specified group

        This method creates a new text Surface with the specified `Font` object
        and replace the existing one with the new Surface


        Args:
            group_name: The name of the group where the text object is located.
            object_name: The name of the text object to be updated within the group.
            text: The new text to render and update within the specified text
                object.
        """
        if self.text_states[object_name] != state:
            self.text_objects[group_name][object_name].update(text)
            self.text_states[object_name] = state

    def update(self):
        """Callable method to update the text objects in the UI.

        Checks whether relevant game state values have changed and calls a method
        to update the changed text objects.
        """
        if not self.game_state.game_over:
            lives: int = self.game_state.player.lives
            self._update_text_object(Group.GAMEPLAY, Text.LIVES, f"Lives: {lives}", lives)

            points: int = self.game_state.points
            self._update_text_object(Group.GAMEPLAY, Text.POINTS, f"Points: {points}", points)

            level: int = self.game_state.level
            self._update_text_object(Group.GAMEPLAY, Text.LEVEL, f"Level: {level}", level)
        else:
            self._update_score_board()
