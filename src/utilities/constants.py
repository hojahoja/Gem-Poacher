import os
from enum import IntEnum, StrEnum


class Folder(StrEnum):
    SRC_DIR = os.path.join(os.path.dirname(__file__), "..")
    ASSETS_DIR = os.path.join(SRC_DIR, "assets")
    IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
    FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
    CONFIG_DIR = os.path.join(SRC_DIR, "config")


class Difficulty(IntEnum):
    EASY = 0
    MEDIUM = 1
    HARD = 2
    LUDICROUS = 3
    CUSTOM = -1
