from typing import Iterable
import dataclasses
import os
import sys


def main():
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


@dataclasses.dataclass(frozen=True)
class Environment:
    values: dict[str, int]
    expressions: dict[str, tuple[str, str, str]]

    def value(self, var: str) -> int:
        if var in self.values:
            return self.values[var]
        a, op, b = self.expressions[var]
        match op:
            case "AND":
                return self.value(a) & self.value(b)
            case "OR":
                return self.value(a) | self.value(b)
            case "XOR":
                return self.value(a) ^ self.value(b)
        raise ValueError(f"unknown operator: {op}")

    def get_and_of(self, a: str, b: str) -> str:
        return self.get_result_of(a, "AND", b)

    def get_or_of(self, a: str, b: str) -> str:
        return self.get_result_of(a, "OR", b)

    def get_xor_of(self, a: str, b: str) -> str:
        return self.get_result_of(a, "XOR", b)

    def get_result_of(self, a: str, op: str, b: str) -> str:
        ab = sorted([a, b])
        for v, (va, vop, vb) in self.expressions.items():
            if vop == op and ab == sorted([va, vb]):
                return v
        raise ValueError(a, op, b)

    def get_operands_of(self, v: str) -> tuple[str, str]:
        a, op, b = self.expressions[v]
        return a, b
    
    def get_other_operand_and_result_of(self, a: str, op: str) -> tuple[str, str]:
        for v, (va, vop, vb) in self.expressions.items():
            if op == vop and a in (va, vb):
                b = ({va, vb} - {a}).pop()
                return b, v
        raise ValueError(a, op)

    def swap(self, v1: str, v2: str) -> None:
        self.expressions[v1], self.expressions[v2] = (
            self.expressions[v2],
            self.expressions[v1],
        )


def get_values(values_str: str) -> dict[str, int]:
    values = {}
    for line in values_str.splitlines():
        var, value = line.split(": ")
        values[var] = int(value)
    return values


def get_expressions(expressions_str: str) -> dict[str, tuple[str, str, str]]:
    expressions = {}
    for line in expressions_str.splitlines():
        expression, var = line.split(" -> ")
        a, op, b = expression.split(" ")
        expressions[var] = (a, op, b)
    return expressions


def part_1(data: str) -> int:
    values_str, expressions_str = data.split("\n\n")
    values = get_values(values_str)
    expressions = get_expressions(expressions_str)

    env = Environment(values, expressions)
    result = 0
    for var in sorted(filter(lambda x: x[0] == "z", expressions), reverse=True):
        bit = env.value(var)
        result = result * 2 + bit
    return result


@dataclasses.dataclass(frozen=True)
class HalfAdder:
    env: Environment
    x: str
    y: str
    z: str

    def get_wrong_wirings(self) -> Iterable[str]:
        z = self.env.get_xor_of(self.x, self.y)
        if z != self.z:
            yield from [z, self.z]
            self.env.swap(z, self.z)

    @property
    def cout(self) -> str:
        return self.env.get_and_of(self.x, self.y)


@dataclasses.dataclass(frozen=True)
class FullAdder:
    env: Environment
    x: str
    y: str
    z: str
    cin: str

    def get_wrong_wirings(self) -> Iterable[str]:
        x_xor_y = self.env.get_xor_of(self.x, self.y)
        a, b = self.env.get_operands_of(self.z)
        mismatches = set([x_xor_y, self.cin]) ^ set([a, b])
        if len(mismatches) == 2:
            yield from mismatches
            self.env.swap(*mismatches)
            x_xor_y = self.env.get_xor_of(self.x, self.y)
        elif len(mismatches) == 4:
            z = self.env.get_xor_of(x_xor_y, self.cin)
            yield from [z, self.z]
            self.env.swap(z, self.z)
            a, b = self.env.get_operands_of(self.z)

        x_and_y = self.env.get_and_of(self.x, self.y)
        x_xor_y_and_cin = self.env.get_and_of(x_xor_y, self.cin)
        try:
            cout = self.env.get_or_of(x_and_y, x_xor_y_and_cin)
        except ValueError:
            # either x_and_y or x_xor_y_and_cin is wrong
            try:
                other_operand, cout = self.env.get_other_operand_and_result_of(x_and_y, "OR")
                yield from [x_xor_y_and_cin, other_operand]
                self.env.swap(x_xor_y_and_cin, other_operand)
            except ValueError:
                other_operand, cout = self.env.get_other_operand_and_result_of(x_xor_y_and_cin, "OR")
                yield from [x_and_y, other_operand]
                self.env.swap(x_and_y, other_operand)

    @property
    def cout(self) -> str:
        x_and_y = self.env.get_and_of(self.x, self.y)
        x_xor_y = self.env.get_xor_of(self.x, self.y)
        x_xor_y_and_cin = self.env.get_and_of(x_xor_y, self.cin)
        return self.env.get_or_of(x_and_y, x_xor_y_and_cin)


def part_2(data: str) -> str:
    values_str, expressions_str = data.split("\n\n")
    values = get_values(values_str)
    expressions = get_expressions(expressions_str)

    env = Environment(values, expressions)

    wrong = set()
    adder = HalfAdder(env, "x00", "y00", "z00")
    wrong.update(adder.get_wrong_wirings())
    for i in range(1, 45):
        next_adder = FullAdder(env, f"x{i:02}", f"y{i:02}", f"z{i:02}", adder.cout)
        wrong.update(next_adder.get_wrong_wirings())
        adder = next_adder
    return ",".join(sorted(wrong))


if __name__ == "__main__":
    main()
