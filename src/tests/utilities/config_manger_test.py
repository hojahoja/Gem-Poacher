import unittest
from configparser import ConfigParser
from pathlib import Path
from unittest.mock import patch

from utilities import constants
from utilities.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):

    def setUp(self):
        self.folder_patcher = patch("utilities.config_manager.constants.Folder")
        self.mock_folder = self.folder_patcher.start()

        self.mock_folder.CONFIG_DIR = Path(__file__).resolve().parent
        self.config_ini = self.mock_folder.CONFIG_DIR / "config.ini"

        self.config_manager = ConfigManager()
        self.config_manager.create_config()

        self.folder_patcher.stop()

        self.config_parser = ConfigParser()
        self.config_parser.read(self.config_ini)

    def test_file_is_found_after_initialization(self):
        self.assertTrue(self.config_ini.exists())

    def test_get_database_patch_returns_correct_path(self):
        path = self.config_manager.get_database_path()
        self.assertEqual(path, str(Path(constants.Folder.DATABASE_DIR) / "score.db"))

    def test_config_manager_returns_correct_value_after_changing_it(self):
        self.config_parser.set("GAME SETTINGS", "difficulty", "hard")
        with open(self.config_ini, "w", encoding="utf-8") as configfile:
            self.config_parser.write(configfile)

        self.assertEqual(constants.Difficulty.HARD, self.config_manager.get_difficulty())

        self.config_parser.set("GAME SETTINGS", "difficulty", "medium")
        with open(self.config_ini, "w", encoding="utf-8") as configfile:
            self.config_parser.write(configfile)

        self.assertEqual(constants.Difficulty.MEDIUM, self.config_manager.get_difficulty())

    def test_get_difficulty_returns_medium_by_default(self):
        self.config_manager.create_config(force=True)
        difficulty = self.config_manager.get_difficulty()
        self.assertEqual(constants.Difficulty.MEDIUM, difficulty)

    def test_get_player_lives_returns_correct_value(self):
        lives = self.config_manager.get_player_lives()
        self.assertEqual(9, lives)
