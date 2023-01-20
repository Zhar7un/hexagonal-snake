from core.gameObject import GameObject
from core.cell import Cell


class Food(GameObject):
    def __init__(self, cell: Cell):
        self._cell = cell

    @property
    def cell(self):
        return self._cell

    @cell.setter
    def cell(self, new_cell):
        self._cell = new_cell