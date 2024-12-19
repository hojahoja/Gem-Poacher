from typing import TYPE_CHECKING

from database.database_connection import get_database_connection

if TYPE_CHECKING:
    from sqlite3 import Connection


def _drop_tables(connection: "Connection"):
    connection.execute("DROP TABLE IF EXISTS scores;")
    connection.execute("DROP TABLE IF EXISTS players;")
    connection.commit()


def _create_tables(connection: "Connection") -> None:
    players: str = """
    CREATE TABLE  players (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    """

    scores: str = """
    CREATE TABLE  scores (
        id INTEGER PRIMARY KEY,
        player_id INTEGER NOT NULL REFERENCES players,
        level INTEGER NOT NULL,
        points INTEGER NOT NULL,
        time DATETIME 
    );
    """

    connection.execute(players)
    connection.execute(scores)
    connection.commit()


def initialize_database():
    connection: Connection = get_database_connection()

    _drop_tables(connection)
    _create_tables(connection)


if __name__ == "__main__":
    initialize_database()
