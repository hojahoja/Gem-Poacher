from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlite3 import Connection, Cursor

type ScoreTuple = tuple[str, int, int, str]


class ScoreService:

    def __init__(self, connection: "Connection"):
        self.connection: Connection = connection
        self._init_player_ids()

    def _insert_player(self, name: str) -> int:
        cursor: Cursor = self.connection.cursor()

        sql: str = "INSERT INTO players (name) VALUES (?);"

        cursor.execute(sql, (name,))
        player_id: int = cursor.lastrowid
        self.connection.commit()

        return player_id

    def _insert_score(self, player_id: int, level: int, points: int, time: datetime):
        cursor: Cursor = self.connection.cursor()

        sql: str = "INSERT INTO scores (player_id, level, points, time) VALUES (?, ?, ?, ?);"

        cursor.execute(sql, (player_id, level, points, time))
        self.connection.commit()

    def _init_player_ids(self):
        cursor: Cursor = self.connection.cursor()
        sql: str = "SELECT name, id FROM players;"
        result: list[tuple[str, int]] = cursor.execute(sql).fetchall()

        self.players: dict[str, int] = {name: player_id for name, player_id in result}

    def add_new_score(self, name: str, level: int, points: int, time: datetime):
        if name not in self.players:
            player_id: int = self._insert_player(name)
        else:
            player_id: int = self.players[name]

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

        cursor.execute(sql)
        return cursor.fetchall()
