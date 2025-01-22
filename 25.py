import itertools

import os
import sys


def main():
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))

def has_collision(a: str, b: str) -> bool:
    return any(aa == '#' and bb == '#' for aa, bb in zip(a, b))

def part_1(data: str) -> int:
    items = data.split("\n\n")
    result = 0
    for a, b in itertools.combinations(items, 2):
        if not has_collision(a, b):
            result += 1
    return result

def part_2(data: str) -> int:
    return -1

if __name__ == "__main__":
    main()
