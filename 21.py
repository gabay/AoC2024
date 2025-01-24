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

    @functools.cache
    def get_sequences_for_pressing(self, goal: str) -> list[str]:
        pos = self.keypad.get_position_of_key("A")
        chunks: list[set[str]] = []
        for key in goal:
            next_pos = self.keypad.get_position_of_key(key)
            chunks.append(self.get_sequences_from_to(pos, next_pos))
            pos = next_pos

        return [''.join(i) for i in itertools.product(*chunks)]

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
            seq2_len = sum(get_shortest_sequence_len(seq_chunk, 2) for seq_chunk in get_chunks(seq))
            if shortest is None or shortest > seq2_len:
                shortest = seq2_len
        print(shortest, "*", int(re.search(r"\d+", line).group()))
        complexity = int(re.search(r"\d+", line).group()) * shortest
        result += complexity
    return result

def get_chunks(sequence: str) -> list[str]:
    assert sequence.endswith("A")
    start = 0
    for end, character in enumerate(sequence):
        if character == 'A':
            yield sequence[start:end + 1]
            start = end + 1

@functools.cache
def get_shortest_sequence_len(chunk: str, depth: int, robot: Robot = Robot(DirectionalKeypad())) -> int:
    if depth == 0:
        return len(chunk)
    sequences = list(robot.get_sequences_for_pressing(chunk))
    options = []
    for seq in sequences:
        options.append(sum(get_shortest_sequence_len(seq_chunk, depth - 1, robot) for seq_chunk in get_chunks(seq)))
    return min(options)
    # return sum(_get_shortest_sequence(chunk, depth) for chunk in get_chunks(goal))


def part_2(data: str) -> int:
    numeric_robot = Robot(NumericKeypad())
    result = 0
    for line in data.splitlines():
        print(line)
        shortest = None
        for seq in numeric_robot.get_sequences_for_pressing(line):
            seq2_len = sum(get_shortest_sequence_len(seq_chunk, 25) for seq_chunk in get_chunks(seq))
            if shortest is None or shortest > seq2_len:
                shortest = seq2_len
        print(shortest, "*", int(re.search(r"\d+", line).group()))
        complexity = int(re.search(r"\d+", line).group()) * shortest
        result += complexity
    return result


if __name__ == "__main__":
    main()
