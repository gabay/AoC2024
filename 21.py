import dataclasses
import functools
import itertools
import os
import re
import sys
from typing import Iterable, Protocol


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


class Keypad(Protocol):
    POSITION_BY_KEY: dict[str, Point] = {}
    KEY_BY_POSITION: dict[Point, str] = {}

    def get_position_of_key(self, key: str) -> Point:
        return self.POSITION_BY_KEY[key]

    def get_key_in_position(self, position: Point) -> str:
        return self.KEY_BY_POSITION[position]


class NumericKeypad(Keypad):
    POSITION_BY_KEY = {
        "0": Point(1, 3),
        "1": Point(0, 2),
        "2": Point(1, 2),
        "3": Point(2, 2),
        "4": Point(0, 1),
        "5": Point(1, 1),
        "6": Point(2, 1),
        "7": Point(0, 0),
        "8": Point(1, 0),
        "9": Point(2, 0),
        "A": Point(2, 3),
    }
    KEY_BY_POSITION = {position: key for key, position in POSITION_BY_KEY.items()}


class DirectionalKeypad(Keypad):
    POSITION_BY_KEY = {
        "^": Point(1, 0),
        "<": Point(0, 1),
        "v": Point(1, 1),
        ">": Point(2, 1),
        "A": Point(2, 0),
    }
    KEY_BY_POSITION = {position: key for key, position in POSITION_BY_KEY.items()}


@dataclasses.dataclass(frozen=True)
class Robot:
    keypad: Keypad

    def get_sequences_for_pressing(self, goal: str) -> Iterable[str]:
        pos = self.keypad.get_position_of_key("A")
        chunks: list[set[str]] = []
        for key in goal:
            next_pos = self.keypad.get_position_of_key(key)
            chunks.append(self.get_sequences_from_to(pos, next_pos))
            pos = next_pos

        for i in itertools.product(*chunks):
            yield "".join(i)

    @functools.cache
    def get_sequences_from_to(self, src: Point, dst: Point) -> set[str]:
        delta = dst - src
        updown = ("^" * -delta.y) + ("v" * delta.y)
        leftright = ("<" * -delta.x) + (">" * delta.x)
        result = set()
        ys = range(min(src.y, dst.y), max(src.y, dst.y) + 1)
        if all(Point(src.x, y) in self.keypad.KEY_BY_POSITION for y in ys):
            result.add(updown + leftright + "A")

        xs = range(min(src.x, dst.x), max(src.x, dst.x) + 1)
        if all(Point(x, src.y) in self.keypad.KEY_BY_POSITION for x in xs):
            result.add(leftright + updown + "A")
        return result


def part_1(data: str) -> int:
    numeric_robot = Robot(NumericKeypad())
    result = 0
    for line in data.splitlines():
        print(line)
        shortest = None
        for seq in numeric_robot.get_sequences_for_pressing(line):
            seq2 = get_shortest_sequence(seq, 2)
            if shortest is None or len(shortest) > len(seq2):
                shortest = seq2
        print(len(shortest), "*", int(re.search("\d+", line).group()))
        complexity = int(re.search("\d+", line).group()) * len(shortest)
        result += complexity
    return result


def get_shortest_sequence(goal: str, depth: int) -> str:
    robot = Robot(DirectionalKeypad())
    next_depth_sequences = [goal]
    for depth in range(depth):
        sequences = next_depth_sequences
        next_depth_sequences = []
        print(depth, len(sequences))
        shortest_length = min(map(len, sequences))
        # print(
        #     "trimmed:",
        #     len([s for s in sequences if len(s) > shortest_length]),
        #     "/",
        #     len(sequences),
        # )
        for seq in [sequences[0]]:
            if len(seq) == shortest_length:
                next_depth_sequences += robot.get_sequences_for_pressing(seq)
    return min(next_depth_sequences, key=len)


# DID NOT FINISH
def part_2(data: str) -> int:
    numeric_robot = Robot(NumericKeypad())
    result = 0
    for line in data.splitlines():
        print(line)
        shortest = None
        for seq in numeric_robot.get_sequences_for_pressing(line):
            seq2 = get_shortest_sequence(seq, 5)
            if shortest is None or len(shortest) > len(seq2):
                shortest = seq2
        print(len(shortest), "*", int(re.search("\d+", line).group()))
        complexity = int(re.search("\d+", line).group()) * len(shortest)
        result += complexity
    return result


if __name__ == "__main__":
    main()
