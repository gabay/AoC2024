import dataclasses
import functools
import itertools
import operator
import os
import sys


def main():
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


@dataclasses.dataclass
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
class Robot:
    pos: Point
    vel: Point

    @classmethod
    def from_str(cls, s: str) -> "Robot":
        p, v = s[2:].split(" v=")
        px, py = map(int, p.split(","))
        vx, vy = map(int, v.split(","))
        return cls(Point(px, py), Point(vx, vy))

    def step(self, board: Point):
        self.pos += self.vel
        self.pos.x %= board.x
        self.pos.y %= board.y


def count_robots_per_quadrant(robots: list[Robot], board: Point) -> list[int]:
    counters = [0, 0, 0, 0]
    for robot in robots:
        if robot.pos.x == board.x // 2 or robot.pos.y == board.y // 2:
            continue
        quadrant = (robot.pos.x > (board.x // 2)) + (robot.pos.y > (board.y // 2)) * 2
        counters[quadrant] += 1
    return counters


def part_1(data: str) -> int:
    robots = list(map(Robot.from_str, data.splitlines()))
    board = Point(101, 103)
    for robot in robots:
        for _ in range(100):
            robot.step(board)

    return functools.reduce(operator.mul, count_robots_per_quadrant(robots, board))


def part_2(data: str) -> int:
    robots = list(map(Robot.from_str, data.splitlines()))
    board = Point(101, 103)
    for i in itertools.count(1):
        for robot in robots:
            robot.step(board)
        # find a 3x3 area full of robots to identify a christmas tree
        positions = get_positions(robots)
        for x, y in positions:
            for dx, dy in itertools.product((-1, 0, 1), (-1, 0, 1)):
                if (x + dx, y + dy) not in positions:
                    break
            else:
                # draw(positions, board)
                return i

    return -1


def get_positions(robots: list[Robot]) -> dict[tuple[int, int], int]:
    positions: dict[tuple[int, int], int] = {}
    for robot in robots:
        key = (robot.pos.x, robot.pos.y)
        positions[key] = positions.get(key, 0) + 1
    return positions


def draw(positions: dict[tuple[int, int], int], board: Point):
    for y in range(board.y):
        for x in range(board.x):
            print(positions.get((x, y), "."), end="")
        print()


if __name__ == "__main__":
    main()
