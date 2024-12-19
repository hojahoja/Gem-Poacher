class Score:
    def __init__(self, name: str, level: int, points: int, time: str):
        self.name: str = name
        self.level: int = level
        self.points: int = points
        self.time: str = time

    @property
    def no_date(self) -> tuple[str, int, int]:
        return self.name, self.level, self.points

    @property
    def tuple(self) -> tuple[str, int, int, str]:
        return self.name, self.level, self.points, self.time

    def __repr__(self) -> str:
        return f"Score({self.name}, {self.level}, {self.points}, {self.time})"

    def __eq__(self, other) -> bool:
        return (self.points, self.time) == (other.points, other.time)

    def __lt__(self, other) -> bool:
        return (-self.points, self.time) < (-other.points, other.time)
