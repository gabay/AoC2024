import os
import sys


def main():
    input_file = os.path.splitext(sys.argv[0])[0]
    data = open(input_file).read()

    print("part 1:")
    print(part_1(data))

    print("part 2:")
    print(part_2(data))


def get_connections(data: str) -> dict[str, set[str]]:
    connections = {}
    for line in data.splitlines():
        a, b = line.split("-")
        connections.setdefault(a, set()).add(b)
        connections.setdefault(b, set()).add(a)
    return connections


def part_1(data: str) -> int:
    connections = get_connections(data)

    threes = []
    for a, a_adj in connections.items():
        for b in filter(lambda x: x > a, a_adj):
            b_adj = connections[b]
            for c in filter(lambda x: x > b, a_adj & b_adj):
                threes.append((a, b, c))
    threes_with_t = [(a, b, c) for a, b, c in threes if "t" in (a[0], b[0], c[0])]
    return len(threes_with_t)


def part_2(data: str) -> str:
    connections = get_connections(data)

    unseen_elements = set(connections.keys())
    biggest_clique = set()
    while unseen_elements:
        element = unseen_elements.pop()
        clique = {element}
        for neighbor in connections[element]:
            if connections[neighbor].issuperset(clique):
                clique.add(neighbor)
        if len(biggest_clique) < len(clique):
            biggest_clique = clique
        unseen_elements -= clique
    return ",".join(sorted(biggest_clique))


if __name__ == "__main__":
    main()
