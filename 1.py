def main():
    data = open('1').read().splitlines()
    left = [int(i.split()[0]) for i in data]
    right = [int(i.split()[1]) for i in data]
    left.sort()
    right.sort()

    print('part 1:')
    print(sum(abs(l - r) for l, r in zip(left, right)))

    print('part 2:')
    result = 0
    for number in left:
        count = right.count(number)
        result += number * count
    print(result)


if __name__ == '__main__':
    main()
