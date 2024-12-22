import sqlite3
import sys
from datetime import datetime
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from sqlite3 import Connection, Cursor

type ScoreTuple = tuple[str, int, int, str]


class ScoreService:

    def __init__(self, connection: "Connection"):
        self.connection: Connection = connection

    def _insert_player(self, name: str) -> int | None:
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
        player_id: int = self._insert_player(name)

        self._insert_score(player_id, level, points, time)

    def get_scores(self) -> list[ScoreTuple]:
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
        if "no such table" in exception.args[0]:
            print("Trying to run the game without initializing the database.")
            print("Please refer to the user manual on how to initialize the database.")
            self.connection.close()
            pygame.quit()
            sys.exit()
        else:
            raise exception
