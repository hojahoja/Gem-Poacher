from typing import TYPE_CHECKING

import pygame
from pygame import Surface

if TYPE_CHECKING:
    from ui.ui_manager import UIManager


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

    def __init__(self, display: Surface, ui_manager: "UIManager"):
        """Initializes the renderer.

        Sets up the display surface and UI manager rendering.
        Keeps a reference to game state and uses it to update the game visuals.

        Args:
            display: The display surface where the game's UI elements will be rendered.
            ui_manager: Gives renderer the objects it needs to render based on games states
        """
        self._display: Surface = display
        self.ui_manager = ui_manager

    def render(self):
        self.ui_manager.update()
        self._display.blits((self.ui_manager.get_renderable_surfaces()))
        self.ui_manager.draw_callbacks(self._display)
        pygame.display.update()

    def distribute_ui_events(self, event: pygame.event.Event):
        self.ui_manager.handle_ui_events(event)
