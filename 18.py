import collections
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

    def __lt__(self, other: "Point") -> bool:
        return (self.x, self.y) < (other.x, other.y)

    @classmethod
    def from_string(cls, string: str) -> "Point":
        x, y = map(int, string.split(","))
        return cls(x, y)


@dataclasses.dataclass
class Board:
    walls: set[Point]
    edge: Point

    def bfs(self, start: Point, end: Point) -> int:
        visited = set()
        neighbors: collections.deque = collections.deque()
        neighbors.append((start, 0))
        while neighbors:
            neighbor, length = neighbors.popleft()
            # out of bounds
            if not (0 <= neighbor.x <= self.edge.x and 0 <= neighbor.y <= self.edge.y):
                continue
            # visited / invalid location
            if neighbor in visited or neighbor in self.walls:
                continue
            visited.add(neighbor)

            if neighbor == end:
                return length

            neighbors.append((neighbor + Point(1, 0), length + 1))
            neighbors.append((neighbor - Point(1, 0), length + 1))
            neighbors.append((neighbor + Point(0, 1), length + 1))
            neighbors.append((neighbor - Point(0, 1), length + 1))
        return -1


def part_1(data: str) -> int:
    walls = list(map(Point.from_string, data.splitlines()))
    board_size = 70  # 6  # for the example
    prefix = 1024  # 12 # for the example
    board = Board(set(walls[:prefix]), Point(board_size, board_size))
    return board.bfs(Point(0, 0), Point(board_size, board_size))


def part_2(data: str) -> str:
    walls = list(map(Point.from_string, data.splitlines()))
    board_size = 70
    # binary search
    hi = len(walls) - 1
    lo = 0
    while hi > lo:
        mid = (hi + lo) // 2
        board = Board(set(walls[:mid]), Point(board_size, board_size))
        if board.bfs(Point(0, 0), Point(board_size, board_size)) == -1:
            hi = mid - 1
        else:
            lo = mid + 1
    assert hi == lo
    blocking_point = walls[lo]
    return ",".join(map(str, [blocking_point.x, blocking_point.y]))


if __name__ == "__main__":
    main()
