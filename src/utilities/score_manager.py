import bisect
from datetime import datetime

from database.score_service import ScoreService
from utilities.score import Score

type ScoreTuple = tuple[str, int, int, str]


class ScoreManager:
    """ Manages and maintains a list of game scores.

    This class is responsible for interacting with the ScoreService to retrieve,
    add, and manage a sorted list of game scores. It initializes the scores, handles
    updates, and ensures the scores are maintained in a sorted order for efficient
    storage and retrieval. It maintains a local copy of the scores for efficient retrieval.
    It is assumed that the scores are already in sorted order when initialized as the class uses
    bisect to maintain the sorted order.

    Attributes:
        self._score_service: Service used to interact with underlying score
            storage for fetching and inserting scores.
        self._scores: List of Score objects sorted in ascending order as
            per defined criteria in Score.
    """

    def __init__(self, score_service: ScoreService):
        """Initializes a new instance of the class.

        This constructor sets up the instance by assigning the provided score_service
        to an internal attribute. It also initializes the score list by invoking the
        internal method _init_score_list.

        Args:
            score_service: Service used for score-related database operations.
        """
        self._score_service = score_service
        self._init_score_list()

    def _init_score_list(self):
        """Initializes the list of scores by fetching data from the score service
        and transforming it into a list of `Score` objects.
        """
        scores: list[ScoreTuple] = self._score_service.get_scores()
        self._scores: list[Score] = [Score(name, level, points, time) for name, level, points, time
                                     in scores]

    def add_score(self, name: str, level: int, points: int):
        """Adds a new score entry for a player with the specified details.

        This method records the score of a player including their name, the level
        at which the score was achieved, and the points scored. If the points
        are greater than zero, it creates a timestamp for the score, adds it
        to an internal score service, and updates the local list of scores with bisect.

        Args:
            name: The name of the player.
            level: The level at which the score was achieved.
            points: The points scored by the player.

        """
        if points > 0:
            time: datetime = datetime.now()
            self._score_service.add_new_score(name, level, points, time)
            bisect.insort_right(self._scores, Score(name, level, points, str(time)))

    def get_scores(self) -> list[Score]:
        """Retrieves the list of `Score` objects

        Returns:
            A list containing Score objects.
        """
        return self._scores
