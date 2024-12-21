from enum import IntEnum, StrEnum
from pathlib import Path

SCALE_720P: float = 720 / 1008


class TextObjects(StrEnum):
    LIVES: str = "lives"
    POINTS: str = "points"
    LEVEL: str = "level"
    TITLE: str = "position_0"
    GAME_OVER: str = "game_over"
    END_OPTIONS: str = "end_options"


class TextGroup(StrEnum):
    GAMEPLAY: str = "gameplay_group"
    GAME_OVER_SCREEN: str = "game_over_screen_group"
    HIGH_SCORES: str = "high_scores_group"


class FontStyle(StrEnum):
    GAMEPLAY: str = "gameplay_style"
    GAME_OVER_SCREEN: str = "game_over_screen_style"
    SCORE_TITLE: str = "high_score_title_style"
    SCORE: str = "high_score_style"


class Folder(StrEnum):
    SRC_DIR = str(Path(__file__).parent.parent.resolve())
    ASSETS_DIR = str(Path(SRC_DIR) / "assets")
    IMAGES_DIR = str(Path(ASSETS_DIR) / "images")
    FONTS_DIR = str(Path(ASSETS_DIR) / "fonts")
    CONFIG_DIR = str(Path(SRC_DIR) / "config")
    DATABASE_DIR = str(Path(SRC_DIR) / "database")


class Difficulty(IntEnum):
    EASY = 0
    MEDIUM = 1
    HARD = 2
    LUDICROUS = 3
    CUSTOM = -1
