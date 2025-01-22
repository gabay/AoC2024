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
class Rule:
    a: int
    b: int

    @classmethod
    def from_line(cls, line: str) -> "Rule":
        a, b = map(int, line.split("|"))
        return cls(a, b)

    def validate(self, items: list[int]) -> bool:
        if (
            self.a in items
            and self.b in items
            and items.index(self.a) > items.index(self.b)
        ):
            return False
        return True


def part_1(data):
    rules_str, items_str = data.split("\n\n")
    rules = list(map(Rule.from_line, rules_str.splitlines()))

    result = 0
    for row_str in items_str.splitlines():
        row = list(map(int, row_str.split(",")))
        if all(rule.validate(row) for rule in rules):
            result += row[len(row) // 2]
    return result


def part_2(data):

    rules_str, items_str = data.split("\n\n")
    rules = list(map(Rule.from_line, rules_str.splitlines()))
    predecessors = {}
    for rule in rules:
        predecessors.setdefault(rule.b, set()).add(rule.a)

    result = 0
    for row_str in items_str.splitlines():
        row = list(map(int, row_str.split(",")))

        if not all(rule.validate(row) for rule in rules):
            new_row = order(predecessors, set(row))
            result += new_row[len(new_row) // 2]
    return result


def order(predecessors: dict[int, set[int]], numbers: set[int]) -> list[int]:
    # find the earliest number until there are no items
    new_row = []
    while numbers:
        number = numbers.pop()
        numbers.add(number)
        while preds := predecessors.get(number, set()) & numbers:
            number = preds.pop()
        numbers.remove(number)
        new_row.append(number)
    return new_row


if __name__ == "__main__":
    main()
