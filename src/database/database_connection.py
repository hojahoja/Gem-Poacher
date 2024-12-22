import sqlite3

from utilities.config_manager import ConfigManager


def get_database_connection() -> sqlite3.Connection:
    """Establish a connection to the SQLite database defined in the configuration file.

    This function utilizes the ConfigManager class to get the filename of the database.
    It then establishes and returns a connection to the SQLite database using the provided filename.

    Returns:
        A SQLite database connection object.
    """
    cfg: ConfigManager = ConfigManager()
    cfg.create_config()
    database_file: str = cfg.get_database_path()
    connection: sqlite3.Connection = sqlite3.connect(database_file)
    return connection
