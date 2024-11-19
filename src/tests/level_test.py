import unittest
from level import Level


class LevelTest(unittest.TestCase):

    def setUp(self):
        self.level = Level(1280, 720)
        self.level.player.direction = "right"
        self.level.player.rect.center = (420, 420)

    def test_level_initializes_properly(self):
        self.assertEqual(self.level.width, 1280)
        self.assertEqual(self.level.height, 720)

    def test_level_moves_player_position_correctly(self):
        player = self.level.player
        self.assertEqual(player.rect.center, (420, 420))

        self.level.move_player(520, 680)
        self.assertEqual(player.rect.center, (520, 680))

    def test_level_move_player_changes_direction_right(self):
        self.assertEqual(self.level.player.direction, "right")
        self.level.move_player(410, 420)
        self.assertEqual(self.level.player.direction, "left")

    def test_level_move_player_changes_direction_left(self):
        self.level.player.direction = "left"
        self.level.move_player(430, 420)
        self.assertEqual(self.level.player.direction, "right")

    def test_right_direction_doesnt_change_when_moving_toward_right(self):
        self.level.move_player(430, 420)
        self.assertEqual(self.level.player.direction, "right")

    def test_left_direction_doesnt_change_when_moving_toward_left(self):
        self.level.move_player(400, 420)
        self.assertEqual(self.level.player.direction, "left")

    def test_moving_vertically_doesnt_change_direction(self):
        self.level.move_player(420, 300)
        self.assertEqual(self.level.player.direction, "right")

        self.level.move_player(420, 500)
        self.assertEqual(self.level.player.direction, "right")

    def test_border_collision_works_for_left_side(self):
        self.level.move_player(0, 100)
        collides = self.level.detect_border_collision(self.level.player)
        self.assertTrue(collides)

    def test_border_collision_works_for_right_side(self):
        self.level.move_player(1280, 200)
        collides = self.level.detect_border_collision(self.level.player)
        self.assertTrue(collides)

    def test_border_collision_works_for_top_side(self):
        self.level.move_player(100, 0)
        collides = self.level.detect_border_collision(self.level.player)
        self.assertTrue(collides)

    def test_border_collision_works_for_bottom(self):
        self.level.move_player(100, 720)
        collides = self.level.detect_border_collision(self.level.player)
        self.assertTrue(collides)
