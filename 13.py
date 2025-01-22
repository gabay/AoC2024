import dataclasses
import itertools
import os
import re
import sys

import numpy as np


def main():
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


def part_1(data: str) -> int:
    claws = [Claw.from_string(chunk) for chunk in data.split("\n\n")]
    return sum(map(Claw.get_cheapest_solution_linalg, claws))


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
class Claw:
    a: Point
    b: Point
    goal: Point

    @classmethod
    def from_string(cls, s: str) -> "Claw":
        ax, ay = map(int, re.search(r"Button A: X\+(\d+), Y\+(\d+)", s).groups())
        bx, by = map(int, re.search(r"Button B: X\+(\d+), Y\+(\d+)", s).groups())
        goalx, goaly = map(int, re.search(r"Prize: X=(\d+), Y=(\d+)", s).groups())
        return cls(Point(ax, ay), Point(bx, by), Point(goalx, goaly))

    def get_cheapest_solution(self) -> int:
        for a_presses in itertools.count():
            goal = self.goal - (self.a * a_presses)
            if goal.x < 0 or goal.y < 0:
                return 0
            b_presses = goal.x // self.b.x
            if self.b * b_presses == goal:
                return a_presses * 3 + b_presses
        raise RuntimeError()

    def get_cheapest_solution_linalg(self) -> int:
        # solve linear equation:
        # | AX | BX | GOALX |
        # | AY | BY | GOALY |
        matrix = np.array(
            [[self.a.x, self.b.x, self.goal.x], [self.a.y, self.b.y, self.goal.y]],
            dtype=float,
        )
        # clear leding zero from second row
        matrix[1] = matrix[1] - matrix[0] * (matrix[1, 0] / matrix[0, 0])
        # clear trailing zero from first row
        matrix[0] = matrix[0] - matrix[1] * (matrix[0, 1] / matrix[1, 1])
        # normalize
        matrix[0] = matrix[0] / matrix[0, 0]
        matrix[1] = matrix[1] / matrix[1, 1]

        # option 2 - use numpy linal
        # solution = np.linalg.solve(matrix[:, :2], matrix[:, 2])

        # accept only integer solutions
        a_presses, b_presses = matrix[:, 2]
        if (
            abs(a_presses - round(a_presses)) < 1e-3
            and abs(b_presses - round(b_presses)) < 1e-3
        ):
            return round(a_presses) * 3 + round(b_presses)
        return 0


def part_2(data: str) -> int:
    claws = list(map(Claw.from_string, data.split("\n\n")))
    for claw in claws:
        claw.goal.x += 10_000_000_000_000
        claw.goal.y += 10_000_000_000_000
    return sum(map(Claw.get_cheapest_solution_linalg, claws))


if __name__ == "__main__":
    main()
