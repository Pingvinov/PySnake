from collections import deque
from random import choice as rand_choice


class Coordinate(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = new_y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        if isinstance(other, int):
            return Coordinate(self.x + other, self.y + other)
        if isinstance(other, tuple) and len(other) == 2:
            return Coordinate(self.x + other[0], self.y + other[1])
        return Coordinate(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Coordinate(-self.x, -self.y)

    def __sub__(self, other):
        if isinstance(other, int):
            return Coordinate(self.x - other, self.y - other)
        if isinstance(other, tuple) and len(other) == 2:
            return Coordinate(self.x - other[0], self.y - other[1])
        return Coordinate(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Coordinate(self.x * other, self.y * other)

    def __floordiv__(self, other):
        return Coordinate(self.x // other, self.y // other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def close_bounds(func):
    def call_and_moddiv(self, *args):
        new_obj = func(self, *args)
        new_obj.x %= self._max_x
        new_obj.y %= self._max_y
        return TorusCoordinate(new_obj.x, new_obj.y, self._max_x, self._max_y)
    return call_and_moddiv


class TorusCoordinate(Coordinate):
    def __init__(self, x, y, max_x, max_y):
        self._max_x = max_x
        self._max_y = max_y
        super(TorusCoordinate, self).__init__(x, y)

    @close_bounds
    def __add__(self, other):
        return super(TorusCoordinate, self).__add__(other)

    @close_bounds
    def __sub__(self, other):
        return super(TorusCoordinate, self).__sub__(other)

    @close_bounds
    def __mul__(self, other):
        return super(TorusCoordinate, self).__mul__(other)

    @close_bounds
    def __floordiv__(self, other):
        return super(TorusCoordinate, self).__floordiv__(other)


Coord = Coordinate
TCoord = TorusCoordinate


class Pixel(object):
    def __init__(self, coord, rgb=(0, 0, 0)):
        self._coord = coord
        self._rgb = rgb

    def __repr__(self):
        return f"[{self.coordinate}, RGB: {self.rgb}]"

    @property
    def coordinate(self):
        return self._coord

    @property
    def rgb(self):
        return self._rgb

    @rgb.setter
    def rgb(self, rgb):
        if not all([0 <= c <= 255 for c in rgb]):
            raise ValueError(f"Invalid RGB color {rgb}.")
        self._rgb = rgb


class Fruit:
    def __init__(self, coord, col):
        self._color = col
        self._body = Pixel(coord, col)

    def respawn(self, free_pos):
        if len(free_pos) == 0:
            return
        new_coord = rand_choice(free_pos)
        self._body = Pixel(new_coord, self._color)

    @property
    def position(self):
        return self._body.coordinate


class Snake:
    def __init__(self, size, init_pos):
        self.size = size
        self.body = deque()
        self.body_wo_head = set()
        self.body.append(init_pos)
        for i in range(size - 1):
            self.body.append(init_pos - [0, i])

    @property
    def head(self):
        return self.body[-1]

    @property
    def tail(self):
        return self.body[0]

    def move(self, action, grow=False):
        if action == 'H':
            return
        if not grow:
            tail = self.body.popleft()
            self.body_wo_head.remove(tail)
        else:
            self.size += 1
        if action == 'U':
            new_head = self.head + (0, 1)
        elif action == 'D':
            new_head = self.head - (0, 1)
        elif action == 'L':
            new_head = self.head + (1, 0)
        elif action == 'R':
            new_head = self.head - (1, 0)
        else:
            raise ValueError(f"Unknown action {action}.")
        self.body_wo_head.add(self.head)
        self.body.append(new_head)

    def is_selfbiting(self):
        return self.head in self.body_wo_head


class Board(object):
    def __init__(self, n_rows, n_cols):
        self._n_rows = n_rows
        self._n_cols = n_cols
        self._pixels = [Pixel(TCoord(i, j, n_rows, n_cols), (0, 0, 0))
                        for i in range(n_rows) for j in range(n_cols)]

    @property
    def n_rows(self):
        return self._n_rows

    @property
    def n_cols(self):
        return self._n_cols

    def set_all(self, col):
        for p in self:
            p.rgb = col

    def __getitem__(self, items):
        if isinstance(items, int):
            if not 0 <= items < self.n_rows * self.n_cols:
                raise IndexError(f"Pixel index {items} is too large. "
                                 f"Max allowed is {self.n_rows * self.n_cols - 1}")
            return self._pixels[items]
        else:
            if not 0 <= items[0] < self.n_rows:
                raise IndexError(f"Row {items[0]} is out of bounds. Max allowed is {self.n_rows - 1}.")
            if not 0 <= items[1] < self.n_cols:
                raise IndexError(f"Column {items[1]} is out of bounds. Max allowed is {self.n_cols - 1}.")
            return self._pixels[items[0] * self.n_cols + items[1]]

    def __setitem__(self, key, value):
        pixel = self[key]
        pixel.rgb = value

    def __iter__(self):
        for p in self._pixels:
            yield p.rgb


class Environment:
    def __init__(self, size):
        if isinstance(size, int):
            size = (size, size)
        self.world_size = size
        self.snake_size = 1
        self.snake_color = (255, 255, 255)
        self.snake_pos_init = TCoord(size[0], size[1], size[0], size[1]) // 2
        self.snake = None

        self.fruit_size = 1
        self.fruit_color = (255, 0, 0)
        self.fruit = Fruit((0, 0), self.fruit_color)
        self.fruit_prev_pos = TCoord(0, 0, size[0], size[1])

        self.empty_color = (0, 0, 0)

        self.board = Board(size[0], size[1])
        self.score = 0

        self.reset()

    def get_empty_coords(self):
        return [p.position for p in self.board if p.rgb == self.empty_color]

    @property
    def state(self):
        return list(self.board)

    def reset(self):
        self.board.set_all(self.empty_color)
        self.score = 0
        self.snake = Snake(1, self.snake_pos_init)
        self.fruit.respawn(self.get_empty_coords())
        self.fruit_prev_pos = self.fruit.position
        return 'P', self.score

    def update_state(self, action):
        grow_snake = False
        if self.snake.tail == self.fruit_prev_pos:
            grow_snake = True
            self.fruit_prev_pos = self.fruit.position
        self.snake.move(action, grow_snake)
        if self.snake.head == self.fruit.position:
            self.score += 1
            self.fruit.respawn(free_pos=self.get_empty_coords())
        # check for a win
        if self.snake.size == self.board.n_cols * self.board.n_rows:
            return 'W', self.score
        # check for a lost
        if self.snake.is_selfbiting():
            return 'L', self.score
        return 'P', self.score
