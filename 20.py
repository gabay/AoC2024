import collections
import dataclasses
import enum
import os
import sys
from typing import Iterable


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

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


TWO_STEPS_DX_DY = [(2, 0), (1, 1), (0, 2), (-1, 1), (-2, 0), (-1, -1), (0, -2), (1, -1)]


@dataclasses.dataclass
class Board:
    start: Point
    end: Point
    walls: set[Point]
    width: int
    height: int

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
        return cls(start, end, walls, width=x + 1, height=y + 1)

    def bfs_cheats(self) -> Iterable[int]:
        visited = set()
        neighbors: collections.deque = collections.deque([(self.start, [])])
        while neighbors:
            neighbor, path = neighbors.popleft()
            # out of bounds
            if not (0 <= neighbor.x < self.width and 0 <= neighbor.y < self.height):
                continue
            # visited / invalid location
            if neighbor in visited or neighbor in self.walls:
                continue
            visited.add(neighbor)

            if neighbor == self.end:
                final_path = path + [neighbor]
                # traverse path and find cheats
                for index, p in enumerate(final_path):
                    for dx, dy in TWO_STEPS_DX_DY:
                        np = p + Point(dx, dy)
                        if np in visited and np in final_path[index + 3 :]:
                            yield final_path[index + 3 :].index(np) + 1
                break

            new_path = path + [neighbor]
            neighbors.append((neighbor + Point(1, 0), new_path))
            neighbors.append((neighbor - Point(1, 0), new_path))
            neighbors.append((neighbor + Point(0, 1), new_path))
            neighbors.append((neighbor - Point(0, 1), new_path))

    def bfs_cheats2(self, min_length: int) -> Iterable[int]:
        visited = set()
        neighbors: collections.deque = collections.deque([(self.start, [])])
        while neighbors:
            neighbor, path = neighbors.popleft()
            # out of bounds
            if not (0 <= neighbor.x < self.width and 0 <= neighbor.y < self.height):
                continue
            # visited / invalid location
            if neighbor in visited or neighbor in self.walls:
                continue
            visited.add(neighbor)

            if neighbor == self.end:
                final_path = path + [neighbor]
                # traverse path and find cheats
                for index, p in enumerate(final_path):
                    for index2, p2 in enumerate(
                        final_path[index + min_length :], min_length
                    ):
                        dp = p2 - p
                        delta = abs(dp.x) + abs(dp.y)
                        if delta > 20:
                            continue
                        time_saved = index2 - delta
                        if time_saved >= min_length:
                            # print("time saved:", time_saved)
                            yield time_saved

                break

            new_path = path + [neighbor]
            neighbors.append((neighbor + Point(1, 0), new_path))
            neighbors.append((neighbor - Point(1, 0), new_path))
            neighbors.append((neighbor + Point(0, 1), new_path))
            neighbors.append((neighbor - Point(0, 1), new_path))


def part_1(data: str) -> int:
    board = Board.from_string(data)
    results = list(board.bfs_cheats())
    return sum(1 for res in results if res >= 100)


def part_2(data: str) -> int:
    board = Board.from_string(data)
    return len(list(board.bfs_cheats2(100)))


if __name__ == "__main__":
    main()
