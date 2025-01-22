def main():
    # read input
    data = open("2").read()
    rows = data.splitlines()

    # create list of lists
    matrix = []
    for row in rows:
        numbers_strings = row.split()
        numbers = [int(number_string) for number_string in numbers_strings]
        matrix.append(numbers)

    # count safe stuff
    print("part 1:")
    almost_safe_count = 0
    for numbers in matrix:
        if is_safe(numbers):
            almost_safe_count += 1
    print(almost_safe_count)

    # count almost safe stuff
    print("part 2:")
    almost_safe_count = 0
    for numbers in matrix:
        if is_almost_safe(numbers):
            almost_safe_count += 1
    print(almost_safe_count)


def is_safe(numbers: list[int]) -> bool:
    # check that all deltas are between either 1-3 or (-1)-(-3)
    deltas = [a - b for a, b in zip(numbers, numbers[1:])]
    if all(1 <= d <= 3 for d in deltas) or all(-3 <= d <= -1 for d in deltas):
        return True

    return False


def is_almost_safe(numbers: list[int]) -> bool:
    # for each number in numbers, check if it is safe without that number
    for i in range(len(numbers)):
        numbers_without_i = numbers[:i] + numbers[i + 1 :]
        if is_safe(numbers_without_i):
            return True
    return False


if __name__ == "__main__":
    main()
