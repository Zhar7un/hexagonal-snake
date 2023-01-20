from core.cell import Cell
from core.cell import CellType
from core.gameObject import GameObject
from core.position import Position


class Map(GameObject):
    def __init__(self, map_width: int, map_height: int):
        self._width = map_width  # size of x-axis
        self._height = map_height  # size of y-axis
        self.__create_map(map_width, map_height)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def cells(self):
        return self._cells

    def get_cell(self, position: Position):
        return self._cells[position.y][position.x]

    def get_food_cell(self):
        return [cell for cell in sum(self._cells, []) if cell.type == CellType.FOOD][0]

    def get_free_cells(self):
        return [cell for cell in sum(self._cells, []) if cell.type == CellType.FREE]

    def __create_map(self, width: int, height: int):
        """Creates the map of cells with free cell type which represented by 2-dimensional array"""
        self._cells = [[Cell(Position(x, y), CellType.FREE) for x in range(width - (y % 2))] for y in range(height)]
