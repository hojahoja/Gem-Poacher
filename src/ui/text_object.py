from pygame import Surface
from pygame.font import Font


class TextObject:

    def __init__(self, text: str, color: tuple[int, int, int], font: Font,
                 location: tuple[int, int] = (0, 0), ):
        self._text = text
        self._color = color
        self._font = font
        self._location = location
        self._create_surface()

    def update(self, text: str):
        self._text = text
        self._create_surface()

    def _create_surface(self):
        self._surface: Surface = self._font.render(self._text, True, self._color)

    @property
    def location(self) -> tuple[int, int]:
        return self._location

    @location.setter
    def location(self, value: tuple[int, int]):
        if isinstance(value, tuple):
            if isinstance(value[0], int) and isinstance(value[1], int):
                self._location = value

    @property
    def surface(self) -> Surface:
        return self._surface

    @property
    def text(self) -> str:
        return self._text
