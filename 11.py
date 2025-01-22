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


def part_1(data: str) -> int:
    stones = list(map(int, data.split()))
    for _ in range(25):
        stones = blink(stones)
    return len(stones)


def blink(stones: list[int]) -> list[int]:
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            stone_str = str(stone)
            n = len(stone_str) // 2
            new_stones += [int(stone_str[:n]), int(stone_str[n:])]
        else:
            new_stones.append(stone * 2024)
    return new_stones


@functools.cache
def count_blink_n(stone: int, n: int) -> int:
    if n == 0:
        return 1
    if stone == 0:
        return count_blink_n(1, n - 1)
    if len(str(stone)) % 2 == 0:
        stone_str = str(stone)
        half_stone_len = len(stone_str) // 2
        a = int(stone_str[:half_stone_len])
        b = int(stone_str[half_stone_len:])
        return count_blink_n(a, n - 1) + count_blink_n(b, n - 1)
    return count_blink_n(stone * 2024, n - 1)


def part_2(data: str) -> int:
    stones = list(map(int, data.split()))
    return sum([count_blink_n(stone, 75) for stone in stones])


if __name__ == "__main__":
    main()
