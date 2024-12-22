import sqlite3

from utilities.config_manager import ConfigManager


def get_database_connection() -> sqlite3.Connection:
    cfg: ConfigManager = ConfigManager()
    cfg.create_config()
    database_file: str = cfg.get_database_path()
    connection: sqlite3.Connection = sqlite3.connect(database_file)
    return connection
