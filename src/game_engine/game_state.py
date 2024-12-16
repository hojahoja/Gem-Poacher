from random import randint, choice

from pygame.sprite import Group

from sprites import Player, Gem
from sprites.enemy import Enemy
from utilities.constants import Difficulty

type SpawnableObject = Gem | Enemy


class GameState:
    """A class responsible for keeping and updating game state information.

    Mostly for information, but has simple logic that is relevant to itself.
    The main logic is related to spawning game objects. Provides the methods
    for spawning gems and Enemies, but is not responsible for deciding when
    to use them.

    Attributes:
        width: The width of the game window.
        height: The height of the game window.
        player: Instance of Player class.
        gems: pygame sprite group class that contains gem sprites.
        enemies: pygame sprite group class that contains enemy sprites.
        sprites: pygame sprite group class that contains all game sprites.
        _points: Total number of points earned during the game.
    """

    def __init__(self, width: int, height: int, difficulty: int = Difficulty.MEDIUM,
                 lives: int = 18):
        """Initialize the game state.

        Keeps track of the game width and height variables. Initializes the sprites
        and sprites groups and keeps track of points. Adds player sprite to the main
        sprites group upon initialization.

        Args:
            width: The width of the game window.
            height: The height of the game window.
        """
        self._state_variables: dict[str, int] = {
            "initial_lives": lives,
            "difficulty": difficulty,
            "height": height,
            "width": width,
        }
        self._initialize_gameplay_variables()

    def _initialize_gameplay_variables(self):
        """Helper function for initializing game objects.

        Helper function for initializing game objects. Seperated into its own method
        so it can be called when resetting the game state.
        """

        if self.difficulty != Difficulty.CUSTOM:
            lives = 18 // (self.difficulty + 1)
        else:
            lives = self._state_variables["initial_lives"]
        self.player: Player = Player(player_lives=lives)
        self.gems: Group = Group()
        self.enemies: Group = Group()
        self.sprites: Group = Group()
        self._state_variables["points"] = 0
        self._state_variables["level"] = 1

        self.sprites.add(self.player)

    @property
    def width(self):
        return self._state_variables["width"]

    @property
    def height(self):
        return self._state_variables["height"]

    @width.setter
    def width(self, value: int):
        self._state_variables["width"] = value

    @height.setter
    def height(self, value: int):
        self._state_variables["height"] = value

    @property
    def difficulty(self):
        return self._state_variables["difficulty"]

    @difficulty.setter
    def difficulty(self, difficulty: Difficulty):
        self._state_variables["difficulty"] = difficulty.value

    @property
    def points(self):
        """Return the total number of points earned during the game.

        Returns:
            Points as an integer value.
        """
        return self._state_variables["points"]

    def add_points(self, points: int):
        """Adds the given points value to the total points earned during the game.

        Args:
            points: value of points to be added.
        """
        if points >= 0:
            self._state_variables["points"] += points

    @property
    def level(self):
        return self._state_variables["level"]

    @property
    def game_over(self):
        return self.player.lives == 0

    def increase_level(self):
        self._state_variables["level"] += 1

    def _generate_random_spawn_point(self, game_object: SpawnableObject) -> tuple[int, int]:
        """Generate a random spawn point coordinate.

        Generates a random spawn point coordinate and returns them as a tuple.
        takes a Gem or Enemy sprites as a parameter to figure out their height and width.
        This is done so that the sprites spawns can be kept within game borders.

        Args:
            game_object: Gem or Enemy sprite object.

        Returns:
            x, y coordinates as a tuple of two integers.
        """
        end_x: int = game_object.rect.width
        end_y: int = game_object.rect.height
        x: int = randint(1, self.width - end_x)
        y: int = randint(1, self.height - end_y)

        return x, y

    def spawn_enemy(self, speed: int = 1):
        """Spawn an enemy into the game.

        Creates an Enemy with a random movement direction and default speed of 1.
        Adds the created Enemy to enemies and sprites groups.

        Args:
            speed:
        """
        direction: tuple[int, int] = choice(((1, 1), (-1, 1), (1, -1), (-1, -1)))

        enemy: Enemy = Enemy(direction=direction, speed=speed)
        self._add_game_object_to_group(enemy, self.enemies)

        self.sprites.add(enemy)

    def spawn_multiple_enemies(self, enemy_count: int, enemy_speed: int):
        for _ in range(enemy_count):
            self.spawn_enemy(enemy_speed)

    def _add_game_object_to_group(self, game_object: SpawnableObject, group: Group):
        """Adds the given game object to the given group.

        Takes the game object sprite given as the parameter and places them on a random
        coordinate value on the map. After object is placed it is added to the group
        that was given as parameter.

        Args:
            game_object: Gem or Enemy sprite object.
            group: Group object that the game_object will be added to.
        """
        coord: tuple[int, int] = self._generate_random_spawn_point(game_object)
        game_object.place(*coord)
        group.add(game_object)

    def reset_game_state(self):
        self._initialize_gameplay_variables()

    def populate_level_with_gems(self, amount: int = 1):
        """Populate the level with the given amount of gems.

        creates the specified amount of gems and adds them to the game state.
        uses add_game_object_to_group method. which generates a random coordinates
        for every object it adds to the game state.

        Args:
            amount: The number of gems to add.
        """
        for _ in range(amount):
            gem: Gem = Gem()
            self._add_game_object_to_group(gem, self.gems)

        self.sprites.add(self.gems)
