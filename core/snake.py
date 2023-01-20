from collections import deque
from core.map import Map
from core.cell import CellType
from eventing.event import Event
from eventing.eventBus import EventBus
from enum import Enum
from core.gameObject import GameObject
from core.position import Position


class SnakeCrashed(Event):
    pass


class FoodEaten(Event):
    pass


class IrregularSnakeDirectionChange(Event):
    pass

class SnakeMoved(Event):
    pass

class SnakeDirection(Enum):
    UP_LEFT = (-1, 1)
    UP_RIGHT = (0, 1)
    RIGHT = (1, 0)
    DOWN_RIGHT = (1, -1)
    DOWN_LEFT = (0, -1)
    LEFT = (-1, 0)

    def __getitem__(self, item):
        return self.value[item]

    def __str__(self):
        return self.name.lower().replace('_', '-')

    def get_opposite(self):
        return SnakeDirection(tuple(-element for element in self.value))


class Snake(GameObject):
    def __init__(self, game_map: Map, event_bus: EventBus):
        self._map = game_map
        self._eventBus = event_bus

        # spawn snake on center cell of map
        self._head = self.map.get_cell(Position(self.map.width // 2, self.map.height // 2))
        self._head.type = CellType.SNAKE
        self._body = deque([self._head])
        self._length = 1
        self._direction = SnakeDirection.UP_RIGHT
        self._last_left_cell = None
        self._alive = True

    @property
    def map(self):
        return self._map

    @property
    def body(self):
        return self._body

    @property
    def head(self):
        return self._head

    @property
    def last_left_cell(self):
        return self._last_left_cell

    @property
    def length(self):
        return self._length

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_direction):
        if new_direction is not self._direction.get_opposite():
            self._direction = new_direction
        else:
            pass

    def __next_cell(self):
        canonical_position = Position(
            (self.body[0].position.x + self._direction[0]),
            (self.body[0].position.y + self._direction[1]))

        shifted_position = canonical_position

        if self.body[0].position.y % 2 == 0 and self.direction[1] == -1:
            shifted_position = Position(canonical_position.x - 1, canonical_position.y)

        if self.body[0].position.y % 2 == 1 and self.direction[1] == 1:
            shifted_position = Position(canonical_position.x + 1, canonical_position.y)

        shifted_position = Position(shifted_position.x % (self._map.width - (shifted_position.y % 2)),
                                    shifted_position.y % self._map.height)

        return self._map.get_cell(shifted_position)

    def __move(self):
        self._head = self.__next_cell()
        self._body.appendleft(self._head)
        self._map.get_cell(self.body[0].position).type = CellType.SNAKE
        self._last_left_cell = self._body.pop()
        self._last_left_cell.type = CellType.FREE

    def __grow_up(self):
        self._head = self.__next_cell()
        self._body.appendleft(self._head)
        self._map.get_cell(self.body[0].position).type = CellType.SNAKE

    def update(self):
        if not self._alive:
            return

        next_cell = self.__next_cell()
        if next_cell.type is CellType.FREE or next_cell == self._body[-1]:
            self.__move()
            self._eventBus.post(SnakeMoved())
            return

        elif next_cell.type is CellType.FOOD:
            self.__grow_up()
            self._eventBus.post(FoodEaten())
            return

        elif next_cell.type is CellType.SNAKE:
            self._eventBus.post(SnakeCrashed())
            self._alive = False
            return
