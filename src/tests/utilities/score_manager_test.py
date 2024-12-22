import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from database.score_service import ScoreService
from utilities.score import Score
from utilities.score_manager import ScoreManager


class TestScoreManager(unittest.TestCase):

    def setUp(self):
        self.date = datetime.now()

        self.score_list = [
            ("Jake", 0, 9001, str(self.date - timedelta(days=2))),
            ("Take", 1, 9001, str(self.date)),
            ("Make", 2, 9001, str(self.date + timedelta(days=2))),
            ("Lake", 3, 9000, str(self.date))
        ]

        self.score_service = Mock(spec=ScoreService)
        self.score_service.get_scores.return_value = self.score_list
        self.score_manager = ScoreManager(self.score_service)

    def test_score_manager_creates_correct_list_upon_initialization(self):
        score_object_list = [Score(val[0], val[1], val[2], val[3]) for val in self.score_list]

        self.assertEqual(score_object_list, self.score_manager.get_scores())

    def test_score_manager_works_fine_with_an_empty_list(self):
        self.score_service.get_scores.return_value = []
        score_manager = ScoreManager(self.score_service)

        self.assertEqual([], score_manager.get_scores())

    def test_score_doesnt_get_added_if_points_are_less_than_1(self):
        self.score_manager.add_score("Jake", 1, 0)
        self.assertEqual(4, len(self.score_manager.get_scores()))

    def test_scores_get_added_in_correct_order(self):
        test_cases = (
            ("Lake-less", 420, 8000, 4),
            ("Make-more", 420, 9001, 2),
            ("Jake-more", 420, 9002, 0),
        )

        for name, level, points, index in test_cases:
            with self.subTest(expected_name=name):
                self.score_manager.add_score(name, level, points)
                score = self.score_manager.get_scores()[index]
                self.assertEqual(name, score.name)

    def test_add_score_service_add_new_score_gets_called_with_correct_parameters(self):
        with patch("utilities.score_manager.datetime") as mock_datetime:
            mock_datetime.now.return_value = self.date
            self.score_manager.add_score("Fake", 0, 8999)
            self.score_service.add_new_score.assert_called_once_with("Fake", 0, 8999, self.date)
