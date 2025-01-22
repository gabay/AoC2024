import itertools
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


def part_1(data):
    rows = data.splitlines()
    width = len(rows[0])
    word = "XMAS"
    result = 0
    # find "XMAS" in rows
    for row in rows:
        result += row.count(word) + row.count(word[::-1])
    # find "XMAS" in cols
    for i in range(width):
        col = "".join(row[i] for row in rows)
        result += col.count(word) + col.count(word[::-1])
    # find "XMAS" in diags
    for i in range(-width, width):
        diag = "".join(row[i + j] for j, row in enumerate(rows) if 0 <= i + j < width)
        result += diag.count(word) + diag.count(word[::-1])
    for i in range(width * 2):
        diag2 = "".join(row[i - j] for j, row in enumerate(rows) if 0 <= i - j < width)
        result += diag2.count(word) + diag2.count(word[::-1])
    return result


def part_2(data):
    rows = data.splitlines()
    height = len(rows)
    width = len(rows[0])
    result = 0
    for i, j in itertools.product(range(height - 2), range(width - 2)):
        if (
            rows[i + 1][j + 1] == "A"
            and rows[i][j] + rows[i + 2][j + 2] in ("MS", "SM")
            and rows[i + 2][j] + rows[i][j + 2] in ("MS", "SM")
        ):
            result += 1
    return result


if __name__ == "__main__":
    main()
