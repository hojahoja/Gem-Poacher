import sqlite3

from utilities.config_manager import ConfigManager

CFG: ConfigManager = ConfigManager()
CFG.create_config()
DATABASE_FILE: str = CFG.get_database_path()
CONNECTION: sqlite3.Connection = sqlite3.connect(DATABASE_FILE)


def get_database_connection() -> sqlite3.Connection:
    return CONNECTION
