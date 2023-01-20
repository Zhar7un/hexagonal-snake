from core.map import Map
from core.snake import Snake
from core.snake import SnakeDirection
from core.position import Position
from core.snake import FoodEaten
from core.snake import SnakeCrashed
from core.snake import IrregularSnakeDirectionChange
from core.snake import SnakeMoved
from core.food import Food
from core.cell import CellType
from eventing.eventBus import EventBus
from eventing.event import Event
import arcade
import numpy as np
import math


GREEN = (0, 250, 154)


class NoFreeCells(Event):
    pass


class GameMenu(arcade.View):
    def __int__(self):
        pass


class SnakeGame(arcade.Window):
    def __init__(self, map_width: int, map_height: int, title, cell_size=30):
        self._cell_size = cell_size
        super().__init__(self.calculate_width(map_width), self.calculate_height(map_height), title)
        self.center_window()
        arcade.set_background_color(arcade.color.AFRICAN_VIOLET)
        self.set_update_rate(1/2)
        self._eventBus = EventBus()
        self._eventBus.register(NoFreeCells().get_type(), lambda: self.__finish(True))
        self._eventBus.register(FoodEaten().get_type(), self.__spawn_food)
        self._eventBus.register(FoodEaten().get_type(), lambda: arcade.Sound("Sounds/Food_eaten.mp3").play())
        self._eventBus.register(SnakeCrashed().get_type(), lambda: self.__finish(False))
        self._eventBus.register(IrregularSnakeDirectionChange().get_type(),
                                lambda: arcade.Sound("Sounds/IrregularSnakeDirectionChange.mp3").play())
        self._eventBus.register(SnakeMoved().get_type(), lambda: arcade.Sound("Sounds/moved.mp3").play())
        self._map = Map(map_width, map_height)
        self._is_map_drawn = False
        self._snake = Snake(self._map, self._eventBus)
        self._food = self.__spawn_food()
        self._end = False
        self._win = False
        self._lose_sprite = arcade.Sprite("Sprites/finish.png", center_x=self.width / 2, center_y=self.height / 2)
        self._lose_sound = arcade.Sound("Sounds/finish.mp3")
        self._selected_direction = SnakeDirection.UP_RIGHT

    @property
    def selected_direction(self):
        return self._selected_direction

    @selected_direction.setter
    def selected_direction(self, new_direction):
        if new_direction is not self._selected_direction.get_opposite():
            self._selected_direction = new_direction
        else:
            self._eventBus.post(IrregularSnakeDirectionChange())

    @property
    def map(self):
        return self._map

    def calculate_width(self, map_width):
        return round(math.sqrt(3) * self._cell_size * map_width)

    def calculate_height(self, map_height):
        if map_height % 2 == 1:
            return round((3 * (map_height//2 + 1) - 1) * self._cell_size)
        else:
            return round((3 * (map_height/2) - 1 + 1.5) * self._cell_size)

    def __finish(self, win):
        self._end = True
        if not win:
            self._lose_sound.play()
            arcade.start_render()
            self._lose_sprite.width = self.width
            self._lose_sprite.height = self.height
            self._lose_sprite.draw()
            arcade.finish_render()
        else:
            pass

    def draw_map(self):
        for cell in sum(self._map.cells, []):
            self.__draw_regular_hexagon(self.get_center(cell.position), self._cell_size, GREEN, arcade.color.HOOKER_GREEN)

    def get_center(self, position: Position) -> tuple:
        return ((2 * position.x + 1 + position.y % 2) * self._cell_size * math.sqrt(3) / 2,
                (3 * (position.y - position.y % 2) / 2 + 1) * self._cell_size + 1.5 * self._cell_size * (position.y % 2))

    def on_draw(self):
        if self._end and not self._win:
            return

        arcade.start_render()
        self.draw_map()

        for cell in self._snake.body:
            self.__draw_regular_hexagon(self.get_center(cell.position), self._cell_size - 2.5,
                                        arcade.color.GOLD)

        self.__draw_regular_hexagon(self.get_center(self._food.cell.position), self._cell_size - 2.5,
                                    arcade.color.AMARANTH)
        arcade.finish_render()

    def on_update(self, delta_time: float):
        self._snake.direction = self._selected_direction
        self._snake.update()
        self._food.cell = self._map.get_food_cell()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.selected_direction = SnakeDirection.UP_LEFT
        if symbol == arcade.key.E:
            self.selected_direction = SnakeDirection.UP_RIGHT
        if symbol == arcade.key.A:
            self.selected_direction = SnakeDirection.LEFT
        if symbol == arcade.key.D:
            self.selected_direction = SnakeDirection.RIGHT
        if symbol == arcade.key.X:
            self.selected_direction = SnakeDirection.DOWN_RIGHT
        if symbol == arcade.key.Z:
            self.selected_direction = SnakeDirection.DOWN_LEFT

    def __spawn_food(self) -> Food:
        free_cells = self._map.get_free_cells()
        if len(free_cells) == 0:
            self._eventBus.post(NoFreeCells())
        new_food_cell = free_cells[np.random.randint(len(free_cells))]
        new_food_cell.type = CellType.FOOD
        return Food(new_food_cell)

    @staticmethod
    def __draw_regular_hexagon(center, size, color, border_color=None):
        vertices = [
            (center[0], center[1] + size),
            (center[0] + size * (math.sqrt(3)/2), center[1] + size / 2),
            (center[0] + size * (math.sqrt(3)/2), center[1] - size / 2),
            (center[0], center[1] - size),
            (center[0] - size * (math.sqrt(3) / 2), center[1] - size / 2),
            (center[0] - size * (math.sqrt(3) / 2), center[1] + size / 2),
            ]
        arcade.draw_polygon_filled(vertices, color)

        if border_color is not None:
            arcade.draw_polygon_outline(vertices, border_color, 5)


myWindow = SnakeGame(5, 4, 'Test')
arcade.run()
