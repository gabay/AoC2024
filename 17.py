import dataclasses
import enum
import itertools
import os
import re
import sys


def main():
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


@dataclasses.dataclass
class Computer:
    a: int
    b: int
    c: int
    program: list[int]
    instruction_pointer: int = 0
    output: list[int] = dataclasses.field(default_factory=list)

    @classmethod
    def from_string(cls, s: str) -> "Computer":
        lines = s.splitlines()
        a = int(lines[0].split(": ")[1])
        b = int(lines[1].split(": ")[1])
        c = int(lines[2].split(": ")[1])
        program = list(map(int, lines[-1].split(": ")[1].split(",")))
        return cls(a, b, c, program)

    def reset(self, a: int):
        self.a = a
        self.b = self.c = 0
        self.instruction_pointer = 0
        self.output = []

    def run(self) -> list[int]:
        actions = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv,
        ]
        while self.instruction_pointer + 1 < len(self.program):
            opcode = self.program[self.instruction_pointer]
            operand = self.program[self.instruction_pointer + 1]
            actions[opcode](operand)
            self.instruction_pointer += 2
        return self.output

    def adv(self, operand: int):
        self.a = self.a // (2 ** self.combo(operand))

    def bxl(self, operand: int):
        self.b = self.b ^ operand

    def bst(self, operand: int):
        self.b = self.combo(operand) % 8

    def jnz(self, operand: int):
        if self.a != 0:
            self.instruction_pointer = operand - 2

    def bxc(self, operand: int):
        self.b = self.b ^ self.c

    def out(self, operand: int):
        self.output.append(self.combo(operand) % 8)

    def bdv(self, operand: int):
        self.b = self.a // (2 ** self.combo(operand))

    def cdv(self, operand: int):
        self.c = self.a // (2 ** self.combo(operand))

    def combo(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise ValueError(operand)

    def run_with_cache(self, a_to_output: dict[int, list[int]]) -> list[int]:
        actions = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv,
        ]
        initial_a = self.a
        while self.instruction_pointer + 1 < len(self.program):
            if self.instruction_pointer == 0 and self.a in a_to_output:
                self.output += a_to_output[self.a]
                break
            opcode = self.program[self.instruction_pointer]
            operand = self.program[self.instruction_pointer + 1]
            actions[opcode](operand)
            self.instruction_pointer += 2
        a_to_output[initial_a] = tuple(self.output)
        return self.output


def part_1(data: str) -> str:
    computer = Computer.from_string(data)
    return ",".join(map(str, computer.run()))


def part_2(data: str) -> int:
    computer = Computer.from_string(data)
    return solve(computer, 0, (len(computer.program) - 1) * 3) or -1


def solve(computer: Computer, n: int, next_bit: int) -> int | None:
    # pseudo code
    # b = (a % 8) ^ 5
    # c = a // 2**b
    # b = b ^ c
    # a = a // 8
    # b = b ^ 6
    # out b % 8
    # jnz 0
    if next_bit < 0:
        return n

    for i in range(8):
        new_n = n + (i << next_bit)
        computer.reset(new_n)
        output = computer.run()
        if len(output) != len(computer.program):
            continue

        suffix = next_bit // 3
        if output[suffix:] != computer.program[suffix:]:
            continue

        solution = solve(computer, new_n, next_bit - 3)
        if solution is not None:
            return solution

    return None


if __name__ == "__main__":
    main()
