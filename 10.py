import os
import sys
from functools import cache


def main():
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


def part_1(data: str) -> int:
    matrix = tuple([tuple(map(int, row)) for row in data.splitlines()])
    result = 0
    for y, row in enumerate(matrix):
        for x, height in enumerate(row):
            if height == 0:
                result += len(get_trailhead_destinations(matrix, x, y))
    return result


@cache
def get_trailhead_destinations(
    matrix: tuple[tuple[int]], x: int, y: int
) -> set[tuple[int, int]]:
    if matrix[y][x] == 9:
        return set([(x, y)])
    destinations = set()
    for nx in (x - 1, x + 1):
        if 0 <= nx < len(matrix[0]) and matrix[y][nx] == matrix[y][x] + 1:
            destinations |= get_trailhead_destinations(matrix, nx, y)
    for ny in (y - 1, y + 1):
        if 0 <= ny < len(matrix) and matrix[ny][x] == matrix[y][x] + 1:
            destinations |= get_trailhead_destinations(matrix, x, ny)
    return destinations


@cache
def get_trailhead_rating(matrix: tuple[tuple[int]], x: int, y: int) -> int:
    if matrix[y][x] == 9:
        return 1
    rating = 0
    for nx in (x - 1, x + 1):
        if 0 <= nx < len(matrix[0]) and matrix[y][nx] == matrix[y][x] + 1:
            rating += get_trailhead_rating(matrix, nx, y)
    for ny in (y - 1, y + 1):
        if 0 <= ny < len(matrix) and matrix[ny][x] == matrix[y][x] + 1:
            rating += get_trailhead_rating(matrix, x, ny)
    return rating


def part_2(data: str) -> int:
    matrix = tuple([tuple(map(int, row)) for row in data.splitlines()])
    result = 0
    for y, row in enumerate(matrix):
        for x, height in enumerate(row):
            if height == 0:
                result += get_trailhead_rating(matrix, x, y)
    return result


if __name__ == "__main__":
    main()
