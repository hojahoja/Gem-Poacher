import pygame
from pygame.sprite import Group

from sprites import Player, Gem, Enemy
from utilities.constants import Difficulty
from .game_state import GameState

type Character = Player | Enemy
type ProgressionLogic = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]


class GameLogic:
    """A class responsible for providing core functionality of gameplay.

    Attributes:
        _game_state: Instance of GameState class.
        player: Instance of Player class.
        enemies: pygame sprite group class that contains enemy sprites.
        _invulnerability_period: Default value for the player invulnerability period.
        _invulnerability_period_start: Allows the class to track when the
          invulnerability period starts.
    """

    def __init__(self, game_state: GameState, custom_settings: ProgressionLogic | None = None):
        """Initialize the game logic.

        Initializes the base attributes for the class. Player and Enemy Group
        get their own reference variables inside the class, because GameLogic has to
        access them constantly. Invulnerability period variables help with
        handling player invulnerability.
        Args:
            game_state: Instance of GameState class.
        """
        self._game_state: GameState = game_state
        self.player: Player = game_state.player
        self.enemies: Group[Enemy] = game_state.enemies
        self._invulnerability_period: int = 1000
        self._invulnerability_period_start: int = 0
        self._initialize_progression_difficulty_settings(custom_settings)

    def _initialize_progression_difficulty_settings(self, custom_settings: ProgressionLogic | None):
        self._progression_options: list[ProgressionLogic] = [
            ((1, 10), (1, 2), (5, 5)),
            ((2, 6), (2, 3), (4, 4)),
            ((2, 6), (3, 3), (3, 3)),
            ((1, 1), (5, 5), (1, 1)),
            ((2, 6), (2, 3), (4, 4)),
        ]
        if custom_settings:
            self._progression_options.append(custom_settings)

    @property
    def game_over(self):
        return self._game_state.game_over

    def move_player(self, x: int = 0, y: int = 0):
        """Move the player to the given coordinates.

        Moves player using rect.center values. This uses the center of the rendered
        sprite image as the point of the coordinates. Moving the player changes the
        direction variable inside the player sprite instance.

        Args:
            x: x coordinate to move the player to.
            y: y coordinate to move the player to.
        """
        if x > self.player.rect.centerx:
            self.player.direction = "right"
        elif x < self.player.rect.centerx:
            self.player.direction = "left"

        self.player.rect.center = (x, y)

    def move_enemies(self):
        """Moves all enemies inside the enemies group.

        Enemy class is responsible for its own movement logic which this method uses.
        """
        for enemy in self.enemies:
            enemy.move()

    def _run_collision_checks(self):
        """Runs all the collision checks."""
        self._player_gem_collision(self._game_state.gems)
        self._player_wall_collision()
        self._player_enemy_collision()
        self._enemy_wall_collision()

    def detect_border_collision(self, entity: Character) -> bool:
        """Runs detection logic for game border collision.

        Args:
            entity: Player or Enemy class.

        Returns:
            Boolean True if the entity collides with a border else False.

        """
        if (entity.rect.left < 0 or
                entity.rect.right > self._game_state.width or
                entity.rect.top < 0 or
                entity.rect.bottom > self._game_state.height):
            return True
        return False

    def _player_gem_collision(self, gems: Group):
        """Runs a collision detection logic on player and gems.

        Uses pygame.sprite.spritecollide to check whether Player class collides with
        any gem inside the gem group. Upon collision the gem is remove from the group
        and from the game. The value of a removed gem is added to game_states points.

        Args:
            gems: Sprite group containing gems.
        """
        collided_gems: list[Gem] = pygame.sprite.spritecollide(self.player, gems, True)

        if collided_gems:
            for gem in collided_gems:
                self._game_state.add_points(gem.value)

    def _player_wall_collision(self):
        """Checks whether player collides with game borders and calls damage handling"""
        if self.detect_border_collision(self.player):
            self._player_damage_event_handler()

    def _player_enemy_collision(self):
        """Checks whether player collides with enemies and calls damage handling"""
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self._player_damage_event_handler()

    def _enemy_wall_collision(self):
        """Checks whether enemies collides with game borders and changes their direction"""
        for enemy in self.enemies:
            if self.detect_border_collision(enemy):
                if enemy.rect.left < 0:
                    enemy.direction_x = 1
                elif enemy.rect.right > self._game_state.width:
                    enemy.direction_x = -1

                if enemy.rect.top < 0:
                    enemy.direction_y = 1
                elif enemy.rect.bottom > self._game_state.height:
                    enemy.direction_y = -1

    def _player_damage_event_handler(self):
        """Handles the player damage events.

        Checks whether player is currently vulnerable to damage and calls its injure
        function to damage the player if true. In the event that the player takes damage,
        calls the invulnerability handler method.
        """
        if self.player.vulnerable:
            self.player.injure()
            self.activate_player_invulnerability()

    def activate_player_invulnerability(self):
        """Makes player invulnerable to damage and marks the start of the invulnerability.

        After player invulnerability is activated, pygame.time.get_ticks is called to
        get the elapsed time after pygame has been initiated. The value is saved so it
        can be used later when game logic updates.
        """
        self.player.vulnerable = False
        self._invulnerability_period_start = pygame.time.get_ticks()

    def _progress_to_next_level(self):
        self._game_state.increase_level()

        level: int = self._game_state.level
        threshold, enemy_speed, gem_count = self._progression_options[self._game_state.difficulty]

        if level >= threshold[0]:
            self._game_state.spawn_enemy(enemy_speed[0])
            self._game_state.populate_level_with_gems(gem_count[0] + level)
        elif level >= threshold[1]:
            self._game_state.spawn_enemy(enemy_speed[1])
            self._game_state.populate_level_with_gems(gem_count[1] + level)
        else:
            self._game_state.spawn_enemy(speed=1)
            self._game_state.populate_level_with_gems(5)

    def start_new_game(self, difficulty: Difficulty = Difficulty.MEDIUM):
        self._game_state.difficulty = difficulty
        self._game_state.populate_level_with_gems(5)
        self._game_state.spawn_multiple_enemies(enemy_count=3, enemy_speed=1)
        self.activate_player_invulnerability()

    def reset_game(self):
        self._game_state.reset_game_state()
        self._invulnerability_period_start = 0
        self.player.vulnerable = True
        self.player: Player = self._game_state.player
        self.enemies: Group[Enemy] = self._game_state.enemies

    def update(self):
        """Activate all the functionality inside this class

        Update method meant to be called by the running game loop on every iteration
        to keep the game logic running.
        """
        self.move_enemies()
        self._run_collision_checks()

        if not self._game_state.gems:
            self._progress_to_next_level()

        elapsed_time: int = pygame.time.get_ticks() - self._invulnerability_period_start
        if elapsed_time > self._invulnerability_period:
            self.player.vulnerable = True

        self._game_state.sprites.update()
