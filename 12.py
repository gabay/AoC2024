import dataclasses
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


def part_1(data: str) -> int:
    result = 0
    for region in get_regions(data.splitlines()):
        result += region.area() * region.perimeter()
    return result


@dataclasses.dataclass
class Region:
    points: set[tuple[int, int]]

    def area(self) -> int:
        return len(self.points)

    def perimeter(self) -> int:
        perimeter = 0
        for x, y in self.points:
            for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                if (x + dx, y + dy) not in self.points:
                    perimeter += 1
        return perimeter

    def sides(self) -> int:
        sides = 0
        for x, y in self.points:
            for dy in (-1, 1):
                # look for the rightmost horizontal boundry
                if (x, y + dy) not in self.points:
                    if (x + 1, y) not in self.points or (x + 1, y + dy) in self.points:
                        sides += 1
            for dx in (-1, 1):
                # look for the bottom-most vertical boundry
                if (x + dx, y) not in self.points:
                    if (x, y + 1) not in self.points or (x + dx, y + 1) in self.points:
                        sides += 1
        return sides


def get_regions(board: list[str]) -> Iterable[Region]:
    visited = set()
    for y, row in enumerate(board):
        for x in range(len(row)):
            if (x, y) not in visited:
                region = get_region_at(board, x, y)
                yield region
                visited |= region.points


def get_region_at(board: list[str], x: int, y: int) -> Region:
    sign = board[y][x]
    width = len(board[0])
    height = len(board)
    points = set()
    neighbors = [(x, y)]
    while neighbors:
        xx, yy = neighbors.pop()
        in_board = 0 <= xx < width and 0 <= yy < height
        if in_board and (xx, yy) not in points and board[yy][xx] == sign:
            points.add((xx, yy))
            for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                neighbors.append((xx + dx, yy + dy))
    return Region(points)


def part_2(data: str) -> int:
    result = 0
    for region in get_regions(data.splitlines()):
        result += region.area() * region.sides()
    return result


if __name__ == "__main__":
    main()
