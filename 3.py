import re


def main():
    # read input
    data = open("3").read()

    # count safe stuff
    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


def part_1(data):
    # catch all mul() instructions
    muls = re.findall(r"mul\((\d+),(\d+)\)", data)
    result = 0
    for a, b in muls:
        result += int(a) * int(b)
    return result


def part_2(data):
    # catch all mul() / do() / don't() instructions
    muls_and_ops = re.findall(r"mul\((\d+),(\d+)\)|(do)\(\)|(don't)\(\)", data)
    enabled = True
    result = 0
    for a, b, do, dont in muls_and_ops:
        if a and b and enabled:
            result += int(a) * int(b)
        if do:
            enabled = True
        if dont:
            enabled = False
    return result


if __name__ == "__main__":
    main()
