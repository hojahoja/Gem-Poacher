from enum import IntEnum, StrEnum
from pathlib import Path

SCALE_720P: float = 720 / 1008
"""Scale factor for 720p resolution using castle dungeon background as the baseline value."""


class TextObjects(StrEnum):
    """Defines enumeration for text objects used UITextController.

    Attributes:
        LIVES: Represents the text object for player lives.
        POINTS: Represents the text object for player score or points.
        LEVEL: Represents the text object for the game level information.
        TITLE: Represents the text object for the initial title or position.
        GAME_OVER: Represents the text object for the game over screen.
        END_OPTIONS: Represents the text object for end game options.
    """
    LIVES: str = "lives"
    POINTS: str = "points"
    LEVEL: str = "level"
    TITLE: str = "position_0"
    GAME_OVER: str = "game_over"
    END_OPTIONS: str = "end_options"


class TextGroup(StrEnum):
    """Represents groups of text types used accessible through the UITextController.

    The string values can be used to access the available groups inside
    UITextController by using its .get_text_surface_group() method.

    Attributes:
        GAMEPLAY: Represents the gameplay group.
        GAME_OVER_SCREEN: Represents the game over screen group.
        HIGH_SCORES: Represents the high scores group.
    """
    GAMEPLAY: str = "gameplay_group"
    GAME_OVER_SCREEN: str = "game_over_screen_group"
    HIGH_SCORES: str = "high_scores_group"


class FontStyle(StrEnum):
    """Represents different font styles that are setup in the UITextController.

    Attributes:
        GAMEPLAY: Font style used during gameplay.
        GAME_OVER_SCREEN: Font style used in the game over screen.
        SCORE_TITLE: Font style used for the high score title.
        SCORE: Font style used for the high score value.
    """
    GAMEPLAY: str = "gameplay_style"
    GAME_OVER_SCREEN: str = "game_over_screen_style"
    SCORE_TITLE: str = "high_score_title_style"
    SCORE: str = "high_score_style"


class Folder(StrEnum):
    """Enumeration for predefined folder paths relevant to the application.

    Attributes:
        SRC_DIR: Absolute path to the source parent directory of the application.
        ASSETS_DIR: Absolute path to the assets directory containing
            general application assets.
        IMAGES_DIR: Absolute path to the images directory where image
            resources are stored.
        FONTS_DIR: Absolute path to the fonts directory where font
            resources are contained.
        CONFIG_DIR: Absolute path to the configuration directory that
            holds application configuration files.
        DATABASE_DIR: Absolute path to the database directory for storing
            database files.
    """
    SRC_DIR = str(Path(__file__).parent.parent.resolve())
    ASSETS_DIR = str(Path(SRC_DIR) / "assets")
    IMAGES_DIR = str(Path(ASSETS_DIR) / "images")
    FONTS_DIR = str(Path(ASSETS_DIR) / "fonts")
    CONFIG_DIR = str(Path(SRC_DIR) / "config")
    DATABASE_DIR = str(Path(SRC_DIR) / "database")


class Difficulty(IntEnum):
    """Enumeration for game difficulty levels.

    Game difficulties are represented as integers. This provides a way to use them based
    on difficulty names.

    Attributes:
        EASY: Represents the easiest difficulty level.
        MEDIUM: Represents a medium difficulty level.
        HARD: Represents a hard difficulty level.
        LUDICROUS: Represents the most challenging difficulty level.
        CUSTOM: Represents a customizable difficulty level.
    """
    EASY = 0
    MEDIUM = 1
    HARD = 2
    LUDICROUS = 3
    CUSTOM = -1
