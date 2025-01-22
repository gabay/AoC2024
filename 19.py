import functools
import os
import sys


def main():
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


class Patterns:
    def __init__(self, patterns: list[str]):
        self.patterns = patterns

    @functools.cache
    def can_make(self, design: str) -> bool:
        if design == "":
            return True
        for pattern in self.patterns:
            if design.startswith(pattern) and self.can_make(design[len(pattern) :]):
                return True
        return False

    @functools.cache
    def count_ways_to_make(self, design: str) -> int:
        if design == "":
            return 1
        ways_to_make = 0
        for pattern in self.patterns:
            if design.startswith(pattern):
                ways_to_make += self.count_ways_to_make(design[len(pattern) :])
        return ways_to_make


def part_1(data: str) -> int:
    patterns_str, designs_str = data.split("\n\n")
    patterns = Patterns(patterns_str.split(", "))
    return len(list(filter(patterns.can_make, designs_str.splitlines())))


def part_2(data: str) -> int:
    patterns_str, designs_str = data.split("\n\n")
    patterns = Patterns(patterns_str.split(", "))
    return sum(map(patterns.count_ways_to_make, designs_str.splitlines()))


if __name__ == "__main__":
    main()
