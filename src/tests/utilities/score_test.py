import unittest
from datetime import datetime, timedelta

from utilities.score import Score


class TestScore(unittest.TestCase):

    def setUp(self):
        self.time = datetime.now()
        self.score = Score("Tester Bester", 100, 100, str(self.time))

    def test_score_is_initialized_with_correct_values(self):
        with self.subTest("Name is set correctly"):
            self.assertEqual("Tester Bester", self.score.name)

        with self.subTest("Level is set correctly"):
            self.assertEqual(100, self.score.level)

        with self.subTest("Points are set correctly"):
            self.assertEqual(100, self.score.points)

        with self.subTest("Time is set correctly"):
            self.assertEqual(str(self.time), self.score.time)

    def test_no_date_returns_a_tuple_with_no_date_value(self):
        with self.subTest("Other values match"):
            no_date_tuple = (self.score.name, self.score.level, self.score.points)
            self.assertEqual(no_date_tuple, self.score.no_date)

        with self.subTest("time is not in tuple"):
            self.assertNotIn(self.score.time, self.score.no_date)

    def test_tuple_returns_correct_values(self):
        expected = (self.score.name, self.score.level, self.score.points, self.score.time)
        self.assertEqual(expected, self.score.tuple)

    def test_repr_returns_correct_string(self):
        expected = f"Score({self.score.name}, {self.score.level}, {self.score.points}, {self.score.time})"
        self.assertEqual(expected, repr(self.score))

    def test_score_with_same_points_and_time_is_equal(self):
        same_score = Score("Bester Tester", 2, 100, str(self.time))
        self.assertEqual(self.score, same_score)

    def test_score_with_same_points_but_different_time_is_not_equal(self):
        different_time = self.time + timedelta(seconds=1)
        different_score = Score("Bester Tester", 2, 100, str(different_time))
        self.assertNotEqual(self.score, different_score)

    def test_score_with_same_time_but_different_points_is_not_equal(self):
        different_points = Score("Bester Tester", 2, 200, str(self.time))
        self.assertNotEqual(self.score, different_points)

    def test_score_is_evaluated_in_reverse_order_for_points(self):
        bigger_score = Score("Bester Tester", 2, 200, str(self.time))
        self.assertLess(bigger_score, self.score)

    def test_score_is_evaluated_in_regular_order_for_time(self):
        earlier_time = self.time - timedelta(seconds=1)
        earlier_score = Score("Bester Tester", 2, 100, str(earlier_time))
        self.assertLess(earlier_score, self.score)
