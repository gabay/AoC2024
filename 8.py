import dataclasses
import itertools
import os
import sys
from typing import Iterable


def main():
    # read input
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


@dataclasses.dataclass
class Antenna:
    x: int
    y: int

    def antinodes(self, other: "Antenna") -> list["Antenna"]:
        dx = self.x - other.x
        dy = self.y - other.y
        return [Antenna(self.x + dx, self.y + dy), Antenna(other.x - dx, other.y - dy)]

    def antinodes2(
        self, other: "Antenna", width: int, height: int
    ) -> Iterable["Antenna"]:
        dx = self.x - other.x
        dy = self.y - other.y
        for i in itertools.count(0):
            x, y = self.x + dx * i, self.y + dy * i
            if not (0 <= x < width and 0 <= y < height):
                break
            yield Antenna(x, y)
        for i in itertools.count(0):
            x, y = other.x - dx * i, other.y - dy * i
            if not (0 <= x < width and 0 <= y < height):
                break
            yield Antenna(x, y)


def get_antennas(rows: list[str]) -> dict[str, list[Antenna]]:
    antennas = {}
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            if cell != ".":
                antennas.setdefault(cell, []).append(Antenna(x, y))
    return antennas


def part_1(data: str) -> int:
    rows = data.splitlines()
    antennas = get_antennas(rows)
    height = len(rows)
    width = len(rows[0])
    antinodes = set()
    for ants in antennas.values():
        for ant_a, ant_b in itertools.combinations(ants, 2):
            for antinode in ant_a.antinodes(ant_b):
                if 0 <= antinode.x < width and 0 <= antinode.y < height:
                    antinodes.add((antinode.x, antinode.y))
    return len(antinodes)


def part_2(data: str) -> int:
    rows = data.splitlines()
    antennas = get_antennas(rows)
    height = len(rows)
    width = len(rows[0])
    antinodes = set()
    for ants in antennas.values():
        for ant_a, ant_b in itertools.combinations(ants, 2):
            for antinode in ant_a.antinodes2(ant_b, width, height):
                antinodes.add((antinode.x, antinode.y))
    return len(antinodes)


if __name__ == "__main__":
    main()
