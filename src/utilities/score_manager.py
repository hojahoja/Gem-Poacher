import bisect
from datetime import datetime

from database.score_service import ScoreService
from utilities.score import Score

type ScoreTuple = tuple[str, int, int, str]


class ScoreManager:

    def __init__(self, score_service: ScoreService):
        self._score_service = score_service
        self._init_score_list_()

    def _init_score_list_(self):
        scores: list[ScoreTuple] = self._score_service.get_scores()
        self._scores: list[Score] = [Score(name, level, points, time) for name, level, points, time
                                     in scores]

    def add_score(self, name: str, level: int, points: int):
        if points > 0:
            time: datetime = datetime.now()
            self._score_service.add_new_score(name, level, points, time)
            bisect.insort_right(self._scores, Score(name, level, points, str(time)))

    def get_scores(self) -> list[Score]:
        return self._scores
