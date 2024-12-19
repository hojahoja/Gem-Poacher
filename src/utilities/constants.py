from enum import IntEnum, StrEnum
from pathlib import Path


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
