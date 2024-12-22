class Score:
    """Represents a single score entry in the scoreboard.

    The Score class represents a single score entry, which includes the players name
    level reached, points scored, and the time when the score was recorded.
    It also provides utility methods to compare scores and retrieve score information.

    Attributes:
        name: The name of the player.
        level: The level the player has reached.
        points: The points scored by the player.
        time: The time at which the score was recorded.
    """

    def __init__(self, name: str, level: int, points: int, time: str):
        """Initializes the score object.

        Args:
            name: The name of the player.
            level: The level the player has achieved.
            points: The number of points the player has scored.
            time: The time the player has spent in the game.
        """
        self.name: str = name
        self.level: int = level
        self.points: int = points
        self.time: str = time

    @property
    def no_date(self) -> tuple[str, int, int]:
        """Returns a tuple containing attributes without a date component.

        This property method retrieves and returns a collection of attributes
        excluding any date-related information. The output is a tuple
        containing the name, level, and points attributes of the object.

        Returns:
            A tuple containing the mentioned values.
        """
        return self.name, self.level, self.points

    @property
    def tuple(self) -> tuple[str, int, int, str]:
        """Returns a tuple representation of the object.

        Returns:
            A tuple containing all the object's attributes
        """
        return self.name, self.level, self.points, self.time

    def __repr__(self) -> str:
        """Provides a string representation of the Score instance."""
        return f"Score({self.name}, {self.level}, {self.points}, {self.time})"

    def __eq__(self, other) -> bool:
        """Determines if two objects are equal based on their attributes.

        This method compares the `points` and `time` attributes of the object
        calling the method with those of another object to determine equality.

        Args:
            other: The object to compare with the current instance.

        Returns:
            bool: True if the two objects have the same `points` and `time`
            attributes; False otherwise.
        """
        return (self.points, self.time) == (other.points, other.time)

    def __lt__(self, other) -> bool:
        """Compares two objects based on their points and time attributes using less than
         comparison.

        The comparison prioritizes higher points over lower and earlier
        time over later for objects with identical points.

        Args:
            other: The object to compare against.

        Returns:
            bool: True if the current object is considered less than the other
            object, False otherwise.
        """
        return (-self.points, self.time) < (-other.points, other.time)
