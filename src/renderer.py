import pygame
from pygame import Surface

import image_handler
import ui_text
from game_engine.game_state import GameState
from text_box import TextInputBox


# Docstrings in this class were written with the help of AI generation.
class Renderer:
    """Handles the rendering process for the game.

    The Renderer class is responsible for managing the visual presentation of the
    game state. It updates and displays text elements and game sprites on the screen.

    Attributes:
        _display: The display surface where the game graphics are rendered.
        _game_state: Represents the current game state, including all
            game elements and related data.
        text_controller: Manages the text elements on the screen, updating them
            according to the game state.
    """

    def __init__(self, display: Surface, game_state: GameState):
        """Initializes the renderer.

        Sets up the display surface and text controller for rendering.
        Keeps a reference to game state and uses it to update the game visuals.

        Args:
            display: The display surface where the game's UI elements will be rendered.
            game_state: The current state of the game that the UI will interact with.
        """
        self._display: Surface = display
        self._game_state: GameState = game_state
        self.text_controller: ui_text.UITextController = ui_text.UITextController(game_state)
        self._initialize_background_()

    def _initialize_background_(self):
        self.background = image_handler.load_image("castle_dungeon_background.png", False,
                                                   (1280, 720))
        # temp
        self.end_background = image_handler.load_image("end_game.png", False, (1280, 720))

        # self.text_box = TextInputBox((240, 271), "Enter Your Name", scale=720 / 1008)
        self.text_box = TextInputBox((100, 200), "Enter Your Name")

    def render(self):

        if not self._game_state.game_over:
            self._gameplay_screen()
        else:
            self._game_over_screen()

    def _gameplay_screen(self):
        """Handles rendering of the display during gameplay.

        This method updates the display elements including filling the background,
        updating the text controller, rendering text objects for the gameplay UI,
        drawing game state sprites, and finally updating the entire display to
        reflect these changes.
        """

        self._display.blit(self.background, (0, 0))
        self.text_controller.update()
        self.render_text_object_groups(ui_text.GAMEPLAY)
        self._game_state.sprites.draw(self._display)
        pygame.display.update()

    def _game_over_screen(self):
        self._display.blit(self.end_background, (0, 0))

        # self._display.blit(self.text_box, (240, 274))
        self.text_box.draw(self._display)
        # self.render_text_object_groups(ui_text.GAME_OVER_SCREEN)

        pygame.display.update()

    def redraw_game_play_text(self):
        self.text_controller.update(force_update=True)

    def render_text_object_groups(self, group_name: str):
        """Renders text objects from a specified group.

        Renders all text objects associated with a specified group name onto the display
        surface. It retrieves text surfaces from a text controller and blits them onto
        the main display screen.

        Args:
            group_name: The name of the group whose text surfaces are to be rendered.
        """
        for text_object in self.text_controller.get_text_surface_group(group_name):
            self._display.blit(*text_object)
