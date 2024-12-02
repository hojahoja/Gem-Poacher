import unittest

from pygame.sprite import Group

from game_engine import GameLogic, GameState
from sprites import Player, Gem


class StubGameState(GameState):
    def __init__(self):
        self.height = 720
        self.width = 1280
        self.player = Player(lives=2)
        self.gems = Group()
        self.sprites = Group()

        self.gems.add(Gem(800, 800, ))
        self.sprites.add(self.player)
        self.sprites.add(self.gems)

        self.populate_called = 0

    def populate_level_with_gems(self, amount: int = 1):
        self.populate_called += 1


class GameLogicTest(unittest.TestCase):

    def setUp(self):
        self.game_state = StubGameState()
        self.player = self.game_state.player
        self.player.rect.center = (420, 420)
        self.game_state.player = self.player
        self.game_logic = GameLogic(self.game_state)

    def test_moves_player_position_correctly(self):
        self.assertEqual((420, 420), self.player.rect.center)

        self.game_logic.move_player(520, 680)
        self.assertEqual((520, 680), self.player.rect.center)

    def test_move_player_changes_direction_right(self):
        self.assertEqual("right", self.player.direction)
        self.game_logic.move_player(410, 420)
        self.assertEqual("left", self.player.direction)

    def test_move_player_changes_direction_left(self):
        self.player.direction = "left"
        self.game_logic.move_player(430, 420)
        self.assertEqual("right", self.player.direction)

    def test_right_direction_doesnt_change_when_moving_toward_right(self):
        self.game_logic.move_player(430, 420)
        self.assertEqual("right", self.player.direction)

    def test_left_direction_doesnt_change_when_moving_toward_left(self):
        self.game_logic.move_player(400, 420)
        self.assertEqual("left", self.player.direction)

    def test_moving_vertically_doesnt_change_direction(self):
        self.game_logic.move_player(420, 300)
        self.assertEqual("right", self.player.direction)

        self.game_logic.move_player(420, 500)
        self.assertEqual("right", self.player.direction)

    def test_border_collision_works_for_left_side(self):
        self.game_logic.move_player(0, 100)
        collides = self.game_logic.detect_border_collision(self.player)
        self.assertTrue(collides)

    def test_border_collision_works_for_right_side(self):
        self.game_logic.move_player(1280, 200)
        collides = self.game_logic.detect_border_collision(self.player)
        self.assertTrue(collides)

    def test_border_collision_works_for_top_side(self):
        self.game_logic.move_player(100, 0)
        collides = self.game_logic.detect_border_collision(self.player)
        self.assertTrue(collides)

    def test_border_collision_works_for_bottom(self):
        self.game_logic.move_player(100, 720)
        collides = self.game_logic.detect_border_collision(self.player)
        self.assertTrue(collides)

    def test_no_collision_detect_when_player_is_not_at_the_border(self):
        collides = self.game_logic.detect_border_collision(self.player)
        self.assertFalse(collides)

    def test_player_wall_collison_triggers_player_damage(self):
        self.game_logic.move_player(0, 100)
        self.game_logic.update()
        self.assertEqual(1, self.player.lives)

    def test_moving_player_without_hitting_walls_doesnt_damage_player(self):
        self.game_logic.move_player(200, 200)
        self.game_logic.update()
        self.assertEqual(2, self.player.lives)

    def test_player_gem_collison_triggers_gem_removal(self):
        gems = self.game_state.gems
        self.assertEqual(1, len(gems))
        self.game_logic.move_player(800, 800)
        self.game_logic.update()
        self.assertEqual(0, len(gems))

    def test_empty_gem_group_triggers_populate_gems(self):
        self.assertEqual(0, self.game_state.populate_called)
        self.game_logic.move_player(800, 800)
        self.game_logic.update()
        self.assertEqual(1, self.game_state.populate_called)
