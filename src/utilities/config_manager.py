import configparser
from configparser import ConfigParser
from pathlib import Path

from utilities import constants


# Specific exceptions are handled inside the exception handler,
# but pylint doesn't know that.
# pylint: disable=broad-exception-caught
class ConfigManager:
    """ Manages the configuration settings for the game.

    This class handles the creation and retrieval, of configuration settings
    related to the game's general settings, database configurations, and
    custom difficulty options. It reads and writes to a `.ini` configuration file,
    defining default values and extending its configuration capabilities for
    customizations.

    Attributes:
        self._config An instance of `ConfigParser` used to manage and
            parse configuration settings.
        self._config_path The file path object for the configuration file where
            settings are stored.
    """

    def __init__(self):
        """Initializes the ConfigManager class and sets path to the configuration file."""
        self._config: ConfigParser = ConfigParser(allow_no_value=True)
        self._config_path: Path = Path(constants.Folder.CONFIG_DIR) / "config.ini"

    def _set_default_configs(self):
        """Sets the default configurations for the game, including base game"""

        self._config["GAME SETTINGS"] = {
            "; Currently width, height, and FPS don't do anything": None,
            "width": "1280",
            "height": "720",
            "fps": "120",
            "; Options: EASY, MEDIUM, HARD, LUDICROUS, CUSTOM": None,
            "difficulty": "MEDIUM"
        }

    def _set_database_configs(self):
        """Sets the default configurations for the database file"""

        self._config["DATABASE SETTINGS"] = {
            "; filename of the DB file in src/database folder": None,
            "database path": "score.db"
        }

    def _set_difficulty_settings(self):
        """Sets the default configurations for the custom difficulty settings"""

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
        """Creates a configuration file with default, database, and difficulty sections.

        If one does not already exist or if the `force` parameter is set to True.
        The configuration is written to the specified file path.

        Args:
            force: If True, forces the creation of a new configuration file
                even if one already exists. Defaults to False.
        """
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
        """Gets the database file path from the configuration file.

        This method reads the database configuration settings from the provided
        configuration file path and constructs the full database file path based
        on the folder defined in `constants.Folder.DATABASE_DIR`.

        Returns:
            Returns the constructed database path as a string if
            it is successfully retrieved, or None if an error occurs.

        Raises:
            ConfigParser errors are handled inside the exception handler.
        """
        path: None | str = None
        try:
            self._config.read(self._config_path)
            filename: str = self._config.get("DATABASE SETTINGS", "database path")
            path = str(Path(constants.Folder.DATABASE_DIR) / filename)
        except Exception as exception:
            _config_exceptionhandler(exception)

        return path

    def get_difficulty(self) -> int:
        """Gets the difficulty setting from the configuration file.

        If the configuration is invalid or an error occurs, defaults to the medium difficulty.
        The method reads the configuration file to extract the difficulty setting
        under the "GAME SETTINGS" section of the provided config file path. It
        translates the difficulty setting into its corresponding numerical value.

        Raises:
            KeyError: If the retrieved difficulty setting does not correspond to
                any valid difficulty level defined in constants.Difficulty.
            Exception: For any other exceptions during configuration file reading,
                handled by `_config_exceptionhandler`.

        Returns:
            The difficulty level represented as a numerical value.
        """

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

    def get_custom_difficulty_settings(self) -> tuple[tuple[int, int]] | None:
        """Retrieves configuration for custom difficulty settings from the config file.

        And parses the config into a list of tuples containing integer values. If the settings
        are incomplete or an exception occurs during retrieval the method returns None and
        informs the user that medium settings are being used.


        Returns:
            A tuple containing a list of tuples
            with integers representing the custom difficulty settings, or None if no
            valid settings are available.
        """
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
        """ Retrieves the number of lives a player has based on the configuration settings.

        This method reads the configuration file to determine the player's lives as defined in the
        "player lives" setting under the "CUSTOM DIFFICULTY SETTINGS" section. If the configuration
        file is not accessible or there is an error retrieving the setting,
        a default value of 5 lives
        is returned.

        Returns:
            The number of lives for the player based on the configuration or default value.
        """
        lives: int = 5
        try:
            self._config.read(self._config_path)
            lives = self._config.getint("CUSTOM DIFFICULTY SETTINGS", "player lives")
        except Exception as exception:
            _config_exceptionhandler(exception)

        return lives


def _config_exceptionhandler(exception: Exception):
    """ Handles exceptions raised during configuration processing.

    Provides appropriate messages for specific exception types, including the handling of IOError,
    configparser errors, and ValueError related to invalid integers. Ensures clarity
    in error reporting and user awareness of configuration defaults.

    Args:
        The exception object to be handled.

    Raises:
        Exception: For any other exception not being specifically handled,
    """

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
