import enum
import os
import sys


def main():
    # read input
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


def rotate_right(direction: int) -> int:
    if direction == UP:
        return RIGHT
    if direction == RIGHT:
        return DOWN
    if direction == DOWN:
        return LEFT
    if direction == LEFT:
        return UP
    raise RuntimeError(direction)


def step(x: int, y: int, direction: int) -> tuple[int, int]:
    if direction == UP:
        return x, y - 1
    if direction == DOWN:
        return x, y + 1
    if direction == LEFT:
        return x - 1, y
    if direction == RIGHT:
        return x + 1, y
    raise RuntimeError(x, y, direction)


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()

    def rotate_right(self) -> "Direction":
        if self == Direction.UP:
            return Direction.RIGHT
        if self == Direction.RIGHT:
            return Direction.DOWN
        if self == Direction.DOWN:
            return Direction.LEFT
        if self == Direction.LEFT:
            return Direction.UP
        raise RuntimeError(self)


def part_1(data):
    return len(get_visited_positions(data.splitlines()))


def get_visited_positions(board: list[str]) -> set[tuple[int, int]] | None:
    height = len(board)
    width = len(board[0])
    x, y, direction = get_pos_and_direction(board)
    visited = set()
    pos_and_dir = set()
    # loop
    while True:
        # add current place to visited
        visited.add((x, y))
        if (x, y, direction) in pos_and_dir:
            return None  # denotes a loop
        pos_and_dir.add((x, y, direction))
        # step
        new_x, new_y = step(x, y, direction)
        # out of bounds
        if not (0 <= new_x < width and 0 <= new_y < height):
            break
        # wall
        if board[new_y][new_x] == "#":
            direction = rotate_right(direction)
        # no wall
        else:
            x, y = new_x, new_y

    return visited


def get_pos_and_direction(board: list[str]) -> tuple[int, int, int]:
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            match cell:
                case "^":
                    return x, y, UP
                case "v":
                    return x, y, DOWN
                case "<":
                    return x, y, LEFT
                case ">":
                    return x, y, RIGHT
    raise RuntimeError(board)


def part_2(data):
    # put obstacle in each place and see if it's a loop
    board = data.splitlines()
    visited_positions = get_visited_positions(board)
    result = 0
    for x, y in visited_positions:
        if board[y][x] == ".":
            old_row = board[y]
            new_row = old_row[:x] + "#" + old_row[x + 1 :]
            board[y] = new_row
            if get_visited_positions(board) is None:
                # loop detected
                result += 1
            board[y] = old_row

    return result


if __name__ == "__main__":
    main()
