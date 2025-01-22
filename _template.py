import os
import sys


def main():
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


def part_1(data: str) -> int:
    return -1


def part_2(data: str) -> int:
    return -1


if __name__ == "__main__":
    main()
