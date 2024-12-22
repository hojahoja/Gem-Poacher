import os
import unittest
from datetime import timedelta, datetime
from pathlib import Path
from unittest.mock import patch

import initialize_database
from database.database_connection import get_database_connection
from database.score_service import ScoreService


class TestScoreService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with patch("database.database_connection.ConfigManager") as mock_config_manager:
            cls.test_db = Path(__file__).resolve().parent / "test.db"
            mock_instance = mock_config_manager.return_value
            mock_instance.get_database_path.return_value = cls.test_db

            if cls.test_db.exists():
                os.remove(cls.test_db)

            cls.connection = get_database_connection()
            initialize_database.initialize_database()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def _create_player_data(self):
        cursor = self.connection.cursor()
        sql = """
        INSERT INTO players (id, name) VALUES (0, 'Make'),(1, 'Jake'),(2, 'Take'),(3, 'Kake');
        """

        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def _create_score_data(self):
        cursor = self.connection.cursor()

        times = [
            str(self.date - timedelta(days=2)),
            str(self.date),
            str(self.date + timedelta(days=2)),
            str(self.date)
        ]

        sql = """
        INSERT INTO scores (player_id, level, points, time) VALUES
            (0, 0, 9001, ?),
            (1, 1, 9001, ?),
            (2, 2, 9001, ?),
            (3, 3, 9000, ?);
        """

        cursor.execute(sql, times)
        self.connection.commit()

    def setUp(self):
        self.date = datetime.now()
        self._create_player_data()
        self._create_score_data()
        self.score_service = ScoreService(self.connection)

        self.score_list = [
            ("Make", 0, 9001, str(self.date - timedelta(days=2))),
            ("Jake", 1, 9001, str(self.date)),
            ("Take", 2, 9001, str(self.date + timedelta(days=2))),
            ("Kake", 3, 9000, str(self.date))
        ]

    def tearDown(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM scores;")
        cursor.execute("DELETE FROM players;")
        cursor.close()

        self.connection.commit()

    def test_get_scores_returns_correct_scores(self):
        scores = self.score_service.get_scores()
        self.assertEqual(self.score_list, scores)

    def test_inserting_new_score_adds_it_to_the_database(self):
        self.score_service.add_new_score("Fake", 0, 8999, self.date)
        scores = self.score_service.get_scores()
        self.assertEqual(scores[-1], ("Fake", 0, 8999, str(self.date)))

    def test_scores_are_sorted_in_expected_order(self):
        test_cases = (
            ("Kake-less", 420, 8000, 4),
            ("Take-more", 420, 9001, 2),
            ("Make-more", 420, 9002, 0),
        )

        for name, level, points, index in test_cases:
            with self.subTest(expected_name=name):
                self.score_service.add_new_score(name, level, points, self.date)
                score = self.score_service.get_scores()[index]
                self.assertEqual(name, score[0])
