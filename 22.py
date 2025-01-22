import os
import sys


def main():
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


def get_secret_number_after(n: int, count: int) -> int:
    for _ in range(count):
        n = get_next_secret_number(n)
    return n


def mix(n: int, m: int) -> int:
    return n ^ m


def prune(n: int) -> int:
    return n % 16777216


def part_1(data: str) -> int:
    result = 0
    for line in data.splitlines():
        n = int(line)
        result += get_secret_number_after(n, 2000)
    return result


def get_next_secret_number(n: int) -> int:
    n = prune(mix(n, n * 64))
    n = prune(mix(n, n // 32))
    n = prune(mix(n, n * 2048))
    return n


def get_prices_and_deltas(n: int, count: int) -> tuple[list[int], list[int]]:
    secret_numbers = [n]
    for _ in range(count):
        secret_numbers.append(get_next_secret_number(secret_numbers[-1]))
    prices = [i % 10 for i in secret_numbers]
    deltas = [j - i for i, j in zip(prices, prices[1:])]
    return prices, deltas


def get_price_per_prefix(n: int, count: int) -> dict[tuple[int, int, int, int], int]:
    prices, deltas = get_prices_and_deltas(n, count)
    price_per_prefix = {}
    for i, price in enumerate(prices[4:], 4):
        prefix = tuple(deltas[i - 4 : i])
        if prefix not in price_per_prefix:
            price_per_prefix[prefix] = price
    return price_per_prefix
    


def part_2(data: str) -> int:
    prices_per_prefix = {}
    for line in data.splitlines():
        n = int(line)
        for prefix, price in get_price_per_prefix(n, 2000).items():
            prices_per_prefix[prefix] = price + prices_per_prefix.get(prefix, 0)
    return max(prices_per_prefix.values())


if __name__ == "__main__":
    main()
