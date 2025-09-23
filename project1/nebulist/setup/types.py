from enum import Enum


class Action(Enum):
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)


class Cell(Enum):
    OPEN = 0
    ROBOT = 1
    BLOCKED = 2

    def __str__(self) -> str:
        if self == Cell.OPEN:
            return " "
        elif self == Cell.ROBOT:
            return "R"
        elif self == Cell.BLOCKED:
            return "#"
        return str(self.value)
