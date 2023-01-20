from enum import Enum
from core.gameObject import GameObject
from core.position import Position


class CellType(Enum):
    FREE = 1
    SNAKE = 2
    FOOD = 3

    def __str__(self):
        return self.name.lower()


class Cell(GameObject):
    def __init__(self, position: Position, cell_type: CellType):
        self._position = position
        self.type = cell_type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, cell_type: CellType):
        self._type = cell_type

    @property
    def position(self):
        return self._position
