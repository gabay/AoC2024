import dataclasses
import os
import sys


def main():
    # read input
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


@dataclasses.dataclass
class Row:
    result: int
    numbers: list[int]

    @classmethod
    def from_line(cls, line: str) -> "Row":
        result_str, numbers_str = line.split(": ")
        return cls(int(result_str), list(map(int, numbers_str.split())))

    def get_possible_results(self) -> set[int]:
        results = set([self.numbers[0]])
        for number in self.numbers[1:]:
            results = set([r + number for r in results] + [r * number for r in results])
        return results

    def get_possible_results2(self) -> set[int]:
        results = set([self.numbers[0]])
        for number in self.numbers[1:]:
            results = set(
                [r + number for r in results]
                + [r * number for r in results]
                + [int(str(r) + str(number)) for r in results]
            )
        return results


def part_1(data: str) -> int:
    result = 0
    for line in data.splitlines():
        row = Row.from_line(line)
        if row.result in row.get_possible_results():
            result += row.result
    return result


def part_2(data: str) -> int:
    result = 0
    for line in data.splitlines():
        row = Row.from_line(line)
        if row.result in row.get_possible_results2():
            result += row.result
    return result


if __name__ == "__main__":
    main()
