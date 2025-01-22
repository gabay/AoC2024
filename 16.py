import dataclasses
import enum
import os
import sys
from queue import PriorityQueue


def main():
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


class Direction(enum.IntEnum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()

    @classmethod
    def directions(cls) -> list["Direction"]:
        return [cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT]


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

    def __lt__(self, other: "Point") -> bool:
        return (self.x, self.y) < (other.x, other.y)

    def step(self, direction: Direction) -> "Point":
        match direction:
            case Direction.UP:
                return Point(self.x, self.y - 1)
            case Direction.DOWN:
                return Point(self.x, self.y + 1)
            case Direction.LEFT:
                return Point(self.x - 1, self.y)
            case Direction.RIGHT:
                return Point(self.x + 1, self.y)


@dataclasses.dataclass
class Board:
    start: Point
    end: Point
    walls: set[Point]

    @classmethod
    def from_string(cls, string: str) -> "Board":
        start = end = None
        walls = set()
        for y, row in enumerate(string.splitlines()):
            for x, cell in enumerate(row):
                if cell == "S":
                    start = Point(x, y)
                if cell == "E":
                    end = Point(x, y)
                if cell == "#":
                    walls.add(Point(x, y))
        assert start and end and walls
        return cls(start, end, walls)


@dataclasses.dataclass(frozen=True)
class State:
    position: Point
    direction: Direction

    def __lt__(self, other: "State") -> bool:
        self_values = (self.position.x, self.position.y, self.direction)
        other_values = (other.position.x, other.position.y, other.direction)
        return self_values < other_values


def part_1(data: str) -> int:
    board = Board.from_string(data)
    seen_states = set()
    next_states: PriorityQueue[tuple[int, State]] = PriorityQueue()
    next_states.put((0, State(board.start, Direction.RIGHT)))
    while next_states:
        score, state = next_states.get()
        if state.position == board.end:
            return score
        if state in seen_states:
            continue
        seen_states.add(state)
        # move
        new_position = state.position.step(state.direction)
        if new_position not in board.walls:
            next_states.put((score + 1, State(new_position, state.direction)))
        # rotate
        for new_dir in Direction.directions():
            if state.direction != new_dir:
                next_states.put((score + 1000, State(state.position, new_dir)))
    return -1


def part_2(data: str) -> int:
    best_path_score = None
    best_path_tiles = set()
    board = Board.from_string(data)
    seen_states: dict[State, int] = {}
    next_states: PriorityQueue[tuple[int, State, list[Point]]] = PriorityQueue()
    next_states.put((0, State(board.start, Direction.RIGHT), [board.start]))
    while next_states:
        score, state, path = next_states.get()
        if best_path_score and score > best_path_score:
            return len(best_path_tiles)
        if state.position == board.end:
            if best_path_score is None:
                best_path_score = score
            best_path_tiles.update(path)
        if seen_states.get(state, score) < score:
            continue
        seen_states[state] = score
        # move
        new_position = state.position.step(state.direction)
        if new_position not in board.walls:
            new_path = path + [new_position]
            next_states.put((score + 1, State(new_position, state.direction), new_path))
        # rotate
        for new_dir in Direction.directions():
            if state.direction != new_dir:
                next_states.put((score + 1000, State(state.position, new_dir), path))
    raise RuntimeError()


if __name__ == "__main__":
    main()
