from level import Level


# TODO decouple game level information from logic.
class GameLogic:

    def __init__(self, level: Level):
        self.level = level
