import sqlite3
import sys
from datetime import datetime
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from sqlite3 import Connection, Cursor

type ScoreTuple = tuple[str, int, int, str]


class ScoreService:
    """Represents a service for managing player scores within a database

    This class is designed for interaction with a database or relevant data
    storage system using an established connection. It supports operations like
    adding new player records, storing scores, and retrieving sorted score lists
    while handling potential errors gracefully. Private methods such as `_insert_player`
    and `_insert_score` enable streamlined management of player and score-related
    data.

    Attributes:
        connection: Connection instance used to establish and manage
            communication with a database or a network service.
    """

    def __init__(self, connection: "Connection"):
        """Initializes the ScoreService instance with a database connection.

        Args:
            connection: database connection
        """
        self.connection: Connection = connection

    def _insert_player(self, name: str) -> int | None:
        """Inserts a new player into the database and retrieves their ID.

        This function attempts to insert a player with the provided name into the
        `players` table of the database. If the player already exists, it skips the
        insertion due to the `INSERT or IGNORE` SQL statement and retrieves their ID.
        In case of an operational error during the database operation, the exception
        is handled by the internal `_exception_handler` method.

        Args:
            name: The name of the player to be inserted into the database.

        Returns:
            An integer representing the ID of the inserted or existing player, or
            None if the operation fails.
        """
        cursor: Cursor = self.connection.cursor()
        player_id: int | None = None

        try:
            sql: str = "INSERT or IGNORE INTO players (name) VALUES (?);"
            cursor.execute(sql, (name,))

            sql: str = "SELECT id FROM players WHERE name = ?;"
            player_id: int = cursor.execute(sql, (name,)).fetchone()[0]
            self.connection.commit()
        except sqlite3.OperationalError as error:
            self._exception_handler(error)

        return player_id

    def _insert_score(self, player_id: int, level: int, points: int, time: datetime):
        """Inserts a new score into the database for a specific player.

        This method takes player's details and score information such as player ID, level,
        points, and the timestamp of the score, and inserts this data into the `scores`
        table. If an exception occurs during database insertion , the error is handled by
        delegating it to the `_exception_handler` method.

        Args:
            player_id: The unique identifier of the player. Cannot be None.
            level: The game level the player achieved the score on.
            points: The score points earned by the player.
            time: The timestamp when the score was achieved.
        """
        if player_id is None:
            return

        cursor: Cursor = self.connection.cursor()
        sql: str = "INSERT INTO scores (player_id, level, points, time) VALUES (?, ?, ?, ?);"

        try:
            cursor.execute(sql, (player_id, level, points, time))
            self.connection.commit()
        except sqlite3.OperationalError as error:
            self._exception_handler(error)

    def add_new_score(self, name: str, level: int, points: int, time: datetime):
        """Adds a new score to the database by inserting player details and score information.

        This method first creates a new player record using the provided player name, retrieves
        a player ID, and then associates the player's ID with their score details, storing all
        relevant data. If the player already exists the new score will be associated with the
        player and player's ID will be retrieved.

        Args:
            name: The name of the player.
            level: The level reached by the player.
            points: The score points earned by the player.
            time: The time the score was recorded.
        """
        player_id: int = self._insert_player(name)

        self._insert_score(player_id, level, points, time)

    def get_scores(self) -> list[ScoreTuple]:
        """Retrieves a list of scores along with player details, sorted by points in descending
        order and time.

        This method queries the database to fetch all player names, levels, points, and times.
        The results are ordered primarily by descending points, and, in case of ties, by time
        in ascending order. Upon encountering a database operational error, the error is handled
        by delegating it to the `_exception_handler` method.

        Returns:
            A list of records containing player names, levels, points, and
            time, sorted as described.

        Raises:
            sqlite3.OperationalError: If an error occurs during the SQL query.
        """

        cursor: Cursor = self.connection.cursor()

        sql: str = """
        SELECT name, level, points, time
        FROM players JOIN scores
            ON players.id = scores.player_id
        ORDER BY 
            points DESC,
            time;
        """

        try:
            cursor.execute(sql)
        except sqlite3.OperationalError as error:
            self._exception_handler(error)

        return cursor.fetchall()

    def _exception_handler(self, exception: Exception):
        """Handles exceptions that arise during runtime and takes appropriate action
        based on the nature of the error.

        If the exception contains the phrase "no such table" error, it provides user
        feedback on the missing database initialization and subsequently terminates
        the application gracefully. For all other exceptions, it re-raises them to
        ensure proper handling elsewhere.

        Args:
            exception: The exception encountered during the program's execution.
        """
        if "no such table" in exception.args[0]:
            print("Trying to run the game without initializing the database.")
            print("Please refer to the user manual on how to initialize the database.")
            self.connection.close()
            pygame.quit()
            sys.exit()
        else:
            raise exception
