import unittest
from unittest.mock import patch

import sprites.enemy


class EnemyTest(unittest.TestCase):

    def setUp(self):
        self.image_handler_patcher = patch("sprites.enemy.image_handler")
        self.mock_image_handler = self.image_handler_patcher.start()
        self.enemy = sprites.Enemy(speed=3)
        print("MOCK", self.enemy._frames)

    def tearDown(self):
        self.image_handler_patcher.stop()

    def test_player_initializes_correctly(self):
        self.assertEqual(3, self.enemy.speed)

    def test_enemy_can_be_moved_manually(self):
        self.enemy.place(400, 420)
        enemy_position = (self.enemy.rect.x, self.enemy.rect.y)
        self.assertEqual((400, 420), enemy_position)

    def test_enemy_moves_to_correct_position(self):
        rect_mock = self.mock_image_handler.load_image.return_value.get_rect.return_value
        rect_mock.center = 420, 420
        rect_mock.centerx = 420
        rect_mock.centery = 420

        test_cases = [
            ((1, 1), (423, 423)),
            ((1, -1), (423, 417)),
            ((-1, 1), (417, 423)),
            ((-1, -1), (417, 417)),
        ]

        for direction, expected_position in test_cases:
            with self.subTest(direction=direction):
                self.enemy.direction_x = direction[0]
                self.enemy.direction_y = direction[1]
                self.enemy.move()
                self.assertEqual(expected_position, self.enemy.rect.center)

    @patch("sprites.enemy.pygame.time.get_ticks")
    def test_enemy_updates_current_frame_value_correctly(self, mock_ticks):
        swap_rate = sprites.enemy.FRAME_SWAP_RATE

        test_cases = [
            (swap_rate + 1, 1),
            (swap_rate * 2 + 2, 2),
            (swap_rate * 3 + 3, 0),
            (swap_rate * 4 + 4, 1),
            (swap_rate * 5 + 5, 2),
        ]

        for elapsed_time, expected_frame_value in test_cases:
            with self.subTest(elapsed_time=elapsed_time, expected_frame_value=expected_frame_value):
                mock_ticks.return_value = elapsed_time
                self.enemy.update()
                self.assertEqual(expected_frame_value, self.enemy._current_frame)

    @patch("sprites.enemy.pygame.time.get_ticks")
    def test_enemy_doesnt_change_frame_value_if_enough_time_has_not_passed(self, mock_ticks):
        self.enemy._current_frame = 1
        mock_ticks.return_value = sprites.enemy.FRAME_SWAP_RATE // 2

        self.enemy.update()
        self.assertEqual(1, self.enemy._current_frame)
