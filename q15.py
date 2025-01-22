import dataclasses
import os
import sys


def main():
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, n: int) -> "Point":
        return Point(self.x * n, self.y * n)


@dataclasses.dataclass
class Board:
    robot: Point
    barrels: set[Point]
    wide_barrels: set[Point]
    blocks: set[Point]

    @classmethod
    def from_string(cls, string: str) -> "Board":
        robot = Point(-1, -1)
        barrels = set()
        blocks = set()
        for y, row in enumerate(string.splitlines()):
            for x, cell in enumerate(row):
                if cell == "@":
                    robot = Point(x, y)
                if cell == "O":
                    barrels.add(Point(x, y))
                if cell == "#":
                    blocks.add(Point(x, y))
        return cls(robot, barrels, set(), blocks)

    @classmethod
    def from_string2(cls, string: str) -> "Board":
        robot = Point(-1, -1)
        wide_barrels = set()
        blocks = set()
        for y, row in enumerate(string.splitlines()):
            for x, cell in enumerate(row):
                if cell == "@":
                    robot = Point(x, y)
                if cell == "O":
                    wide_barrels.add(Point(x, y))
                if cell == "#":
                    blocks.add(Point(x, y))
                    blocks.add(Point(x + 1, y))
        return cls(robot, set(), wide_barrels, blocks)

    def get_gps_sum(self) -> int:
        gps_sum = 0
        for barrel in self.barrels | self.wide_barrels:
            gps_sum += barrel.x + barrel.y * 100
        return gps_sum

    def move_up(self):
        up = Point(self.robot.x, self.robot.y - 1)
        if up in self.blocks or (
            up in self.barrels and self.move_barrel_up(up) is False
        ):
            return
        self.robot = up

    def move_barrel_up(self, barrel: Point) -> bool:
        up = Point(barrel.x, barrel.y - 1)
        if up in self.blocks or (
            up in self.barrels and self.move_barrel_up(up) is False
        ):
            return False
        self.barrels.remove(barrel)
        self.barrels.add(up)
        return True

    def move_down(self):
        down = Point(self.robot.x, self.robot.y + 1)
        if down in self.blocks or (
            down in self.barrels and self.move_barrel_down(down) is False
        ):
            return
        self.robot = down

    def move_barrel_down(self, barrel: Point) -> bool:
        down = Point(barrel.x, barrel.y + 1)
        if down in self.blocks or (
            down in self.barrels and self.move_barrel_down(down) is False
        ):
            return False
        self.barrels.remove(barrel)
        self.barrels.add(down)
        return True

    def move_left(self):
        left = Point(self.robot.x - 1, self.robot.y)
        if left in self.blocks or (
            left in self.barrels and self.move_barrel_left(left) is False
        ):
            return
        self.robot = left

    def move_barrel_left(self, barrel: Point) -> bool:
        left = Point(barrel.x - 1, barrel.y)
        if left in self.blocks or (
            left in self.barrels and self.move_barrel_left(left) is False
        ):
            return False
        self.barrels.remove(barrel)
        self.barrels.add(left)
        return True

    def move_right(self):
        right = Point(self.robot.x + 1, self.robot.y)
        if right in self.blocks or (
            right in self.barrels and self.move_barrel_right(right) is False
        ):
            return
        self.robot = right

    def move_barrel_right(self, barrel: Point) -> bool:
        right = Point(barrel.x + 1, barrel.y)
        if right in self.blocks or (
            right in self.barrels and self.move_barrel_right(right) is False
        ):
            return False
        self.barrels.remove(barrel)
        self.barrels.add(right)
        return True

    def move(self, direction: str):
        match direction:
            case "^":
                self.move_up()
            case "v":
                self.move_down()
            case "<":
                self.move_left()
            case ">":
                self.move_right()
            case _:
                raise ValueError(direction)


def part_1(data: str) -> int:
    board_str, moves = data.split("\n\n")
    board = Board.from_string(board_str)
    for move in moves:
        if move in "<>^v":
            board.move(move)
    return board.get_gps_sum()


@dataclasses.dataclass
class Board2:
    robot: Point
    wide_barrels: set[Point]
    blocks: set[Point]

    @classmethod
    def from_string(cls, string: str) -> "Board2":
        robot = Point(-1, -1)
        wide_barrels = set()
        blocks = set()
        for y, row in enumerate(string.splitlines()):
            for x, cell in enumerate(row):
                if cell == "@":
                    robot = Point(x * 2, y)
                if cell == "O":
                    wide_barrels.add(Point(x * 2, y))
                if cell == "#":
                    blocks.add(Point(x * 2, y))
                    blocks.add(Point(x * 2 + 1, y))
        return cls(robot, wide_barrels, blocks)

    def get_gps_sum(self) -> int:
        gps_sum = 0
        for barrel in self.wide_barrels:
            gps_sum += barrel.x + barrel.y * 100
        return gps_sum

    def has_barrel(self, point: Point) -> bool:
        return point in self.wide_barrels or (point - Point(1, 0)) in self.wide_barrels

    def get_barrel(self, point: Point) -> Point | None:
        if point in self.wide_barrels:
            return point
        left = point - Point(1, 0)
        if left in self.wide_barrels:
            return left
        return None

    def move_up(self):
        up = Point(self.robot.x, self.robot.y - 1)
        if up in self.blocks:
            return
        barrel = self.get_barrel(up)
        if barrel:
            if not self.can_move_barrel_up(barrel):
                return
            self.move_barrel_up(barrel)
        self.robot = up

    def can_move_barrel_up(self, barrel: Point) -> bool:
        up_points = [barrel + Point(0, -1), barrel + Point(1, -1)]
        for point in up_points:
            if point in self.blocks:
                return False
            up_barrel = self.get_barrel(point)
            if up_barrel is not None and not self.can_move_barrel_up(up_barrel):
                return False
        return True

    def move_barrel_up(self, barrel: Point):
        up_points = [barrel + Point(0, -1), barrel + Point(1, -1)]
        for point in up_points:
            up_barrel = self.get_barrel(point)
            if up_barrel is not None:
                self.move_barrel_up(up_barrel)
        self.wide_barrels.remove(barrel)
        self.wide_barrels.add(up_points[0])

    def move_down(self):
        down = Point(self.robot.x, self.robot.y + 1)
        if down in self.blocks:
            return
        barrel = self.get_barrel(down)
        if barrel:
            if not self.can_move_barrel_down(barrel):
                return
            self.move_barrel_down(barrel)
        self.robot = down

    def can_move_barrel_down(self, barrel: Point) -> bool:
        down_points = [barrel + Point(0, 1), barrel + Point(1, 1)]
        for point in down_points:
            if point in self.blocks:
                return False
            down_barrel = self.get_barrel(point)
            if down_barrel is not None and not self.can_move_barrel_down(down_barrel):
                return False
        return True

    def move_barrel_down(self, barrel: Point):
        down_points = [barrel + Point(0, 1), barrel + Point(1, 1)]
        for point in down_points:
            down_barrel = self.get_barrel(point)
            if down_barrel is not None:
                self.move_barrel_down(down_barrel)
        self.wide_barrels.remove(barrel)
        self.wide_barrels.add(down_points[0])

    def move_left(self):
        left = Point(self.robot.x - 1, self.robot.y)
        if left in self.blocks:
            return
        barrel = self.get_barrel(left)
        if barrel:
            if not self.can_move_barrel_left(barrel):
                return
            self.move_barrel_left(barrel)
        self.robot = left

    def can_move_barrel_left(self, barrel: Point) -> bool:
        left = barrel - Point(1, 0)
        if left in self.blocks:
            return False
        left_barrel = self.get_barrel(left)
        if left_barrel is not None and not self.can_move_barrel_left(left_barrel):
            return False
        return True

    def move_barrel_left(self, barrel: Point):
        left = barrel - Point(1, 0)
        left_barrel = self.get_barrel(left)
        if left_barrel is not None:
            self.move_barrel_left(left_barrel)
        self.wide_barrels.remove(barrel)
        self.wide_barrels.add(left)

    def move_right(self):
        right = Point(self.robot.x + 1, self.robot.y)
        if right in self.blocks:
            return
        if right in self.wide_barrels:
            if not self.can_move_barrel_right(right):
                return
            self.move_barrel_right(right)
        self.robot = right

    def can_move_barrel_right(self, barrel: Point) -> bool:
        right = barrel + Point(2, 0)
        if right in self.blocks:
            return False
        if right in self.wide_barrels and not self.can_move_barrel_right(right):
            return False
        return True

    def move_barrel_right(self, barrel: Point):
        right = barrel + Point(1, 0)
        right_barrel = barrel + Point(2, 0)
        if right_barrel in self.wide_barrels:
            self.move_barrel_right(right_barrel)
        self.wide_barrels.remove(barrel)
        self.wide_barrels.add(right)

    def move(self, direction: str):
        match direction:
            case "^":
                self.move_up()
            case "v":
                self.move_down()
            case "<":
                self.move_left()
            case ">":
                self.move_right()
            case _:
                raise ValueError(direction)


def part_2(data: str) -> int:
    board_str, moves = data.split("\n\n")
    board = Board2.from_string(board_str)
    for move in moves:
        if move in "<>^v":
            board.move(move)
    draw(board)
    return board.get_gps_sum()


def draw(board: Board2):
    height = max(block.y for block in board.blocks) + 1
    width = max(block.x for block in board.blocks) + 1
    for y in range(height):
        for x in range(width):
            if Point(x, y) in board.blocks:
                print("#", end="")
            elif Point(x, y) in board.wide_barrels:
                print("[", end="")
            elif x > 0 and Point(x - 1, y) in board.wide_barrels:
                print("]", end="")
            elif Point(x, y) == board.robot:
                print("@", end="")
            else:
                print(".", end="")
        print()


if __name__ == "__main__":
    main()
