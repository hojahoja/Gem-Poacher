import configparser
from configparser import ConfigParser
from pathlib import Path

from utilities import constants


# Specific exceptions are handled inside the exception handler,
# but pylint doesn't know that.
# pylint: disable=broad-exception-caught
class ConfigManager:

    def __init__(self):
        self._config: ConfigParser = ConfigParser(allow_no_value=True)
        self._config_path: Path = Path(constants.Folder.CONFIG_DIR) / "config.ini"

    def _set_default_configs(self):
        self._config["GAME SETTINGS"] = {
            "; Currently width, height, and FPS don't do anything": None,
            "width": "1280",
            "height": "720",
            "fps": "120",
            "; Options: EASY, MEDIUM, HARD, LUDICROUS, CUSTOM": None,
            "difficulty": "MEDIUM"
        }

    def _set_database_configs(self):

        self._config["DATABASE SETTINGS"] = {
            "; filename of the DB file in src/database folder": None,
            "database path": "score.db"
        }

    def _set_difficulty_settings(self):
        self._config["CUSTOM DIFFICULTY SETTINGS"] = {
            "; These settings will be used if you choose custom difficulty in GAME SETTINGS": None,
            "; Thresholds change something after reaching the specified level": None,
            "; Set the first threshold to 1 if you want these values from start of the game": None,
            "dynamic difficulty first threshold": "2",
            "dynamic difficulty second threshold": "6",
            "; How values change after reaching specific thresholds": None,
            "; Default value before reaching the first threshold is 1": None,
            "enemy speed threshold 1": "2",
            "enemy speed threshold 2": "3",
            "; 5 gems are spawned before a threshold is reached": None,
            "; After the first threshold gems spawn at the rate of level + value set": None,
            "gem spawn rate threshold 1": "4",
            "gem spawn rate threshold 2": "4",
            "player lives": "9"
        }

    def create_config(self, force: bool = False):

        if not self._config_path.exists() or force:
            self._set_default_configs()
            self._set_database_configs()
            self._set_difficulty_settings()

            try:
                with open(self._config_path, "w", encoding="utf-8") as configfile:
                    self._config.write(configfile)
            except IOError as exception:
                print("Something went wrong while creating config:")
                print(repr(exception))

    def get_database_path(self) -> None | str:
        path: None | str = None
        try:
            self._config.read(self._config_path)
            filename: str = self._config.get("DATABASE SETTINGS", "database path")
            path = str(Path(constants.Folder.DATABASE_DIR) / filename)
        except Exception as exception:
            _config_exceptionhandler(exception)

        return path

    def get_difficulty(self) -> int:
        difficulty: int = constants.Difficulty.MEDIUM

        try:
            self._config.read(self._config_path)
            setting: str = self._config.get("GAME SETTINGS", "difficulty").upper()
            difficulty = constants.Difficulty[setting].value
        except KeyError as exception:
            print(f"Config error: {exception} is not a valid difficulty setting", )
        except Exception as exception:
            _config_exceptionhandler(exception)
            print("Defaulting to Medium difficulty")
        return difficulty

    def get_custom_difficulty_settings(self):
        setting: list[tuple[int, int]] = []

        try:
            self._config.read(self._config_path)
            options: list[str] = self._config.options("CUSTOM DIFFICULTY SETTINGS")
            if len(options) < 6:
                print("Custom difficulty settings are broken, defaulting to medium settings")
            else:
                for option_1, option_2 in zip(*[iter(options[:6])] * 2):
                    combined_option: tuple[int, int] = (
                        self._config.getint("CUSTOM DIFFICULTY SETTINGS", option_1),
                        self._config.getint("CUSTOM DIFFICULTY SETTINGS", option_2)
                    )
                    setting.append(combined_option)
        except Exception as exception:
            _config_exceptionhandler(exception)

        return tuple(setting) if setting else None

    def get_player_lives(self) -> int:
        lives: int = 9
        try:
            self._config.read(self._config_path)
            lives = self._config.getint("CUSTOM DIFFICULTY SETTINGS", "player lives")
        except Exception as exception:
            _config_exceptionhandler(exception)

        return lives


def _config_exceptionhandler(exception: Exception):
    try:
        raise exception
    except IOError:
        print("Something went wrong when reading the config file: \n", repr(exception))
    except configparser.NoOptionError:
        print("Config error:", exception)
    except configparser.NoSectionError:
        print("Config error:", exception)
    except ValueError as error:
        if "invalid literal for int()" in repr(error):
            incorrect_value: str = repr(error).split("'")[1]
            print(f"Config error: {incorrect_value} is not a valid integer")
        else:
            raise error
    finally:
        print("Deleting the config file will restore default settings")
