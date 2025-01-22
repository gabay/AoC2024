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


def part_1(data: str) -> int:
    layout = Layout.from_line(data)
    layout.compact()
    return layout.checksum()


@dataclasses.dataclass
class Layout:
    layout: list[int]

    @classmethod
    def from_line(cls, line: str) -> "Layout":
        layout = []
        for index, length in enumerate(line.strip()):
            file_id = index // 2 if index % 2 == 0 else -1
            layout += [file_id] * int(length)
        return cls(layout)

    def compact(self):
        left = 0
        right = len(self.layout) - 1
        while left < right:
            if self.layout[left] != -1:
                left += 1
            elif self.layout[right] == -1:
                right -= 1
            else:
                self.layout[left] = self.layout[right]
                self.layout[right] = -1
                left += 1
                right -= 1

    def checksum(self) -> int:
        csum = 0
        for index, file_id in enumerate(self.layout):
            if file_id > 0:
                csum += index * file_id
        return csum


def part_2(data: str) -> int:
    layout2 = Layout2.from_line(data)
    layout2.compact()
    return layout2.checksum()


@dataclasses.dataclass
class Place:
    id: int
    offset: int
    length: int


@dataclasses.dataclass
class Layout2:
    places: list[Place]

    @classmethod
    def from_line(cls, line: str) -> "Layout2":
        places = []
        offset = 0
        for index, length_str in enumerate(line.strip()):
            length = int(length_str)
            id = index // 2 if index % 2 == 0 else -1
            places.append(Place(id, offset, length))
            offset += length
        return cls(places)

    def compact(self):
        for place in filter(lambda p: p.id > 0, reversed(self.places)):
            if place.id < 0:
                continue
            for space in filter(lambda p: p.id == -1, self.places):
                if space.offset >= place.offset:
                    break
                if space.length >= place.length:
                    place.offset = space.offset
                    space.offset += place.length
                    space.length -= place.length
                    break

    def checksum(self) -> int:
        csum = 0
        for place in self.places:
            if place.id > 0:
                for i in range(place.length):
                    csum += (place.offset + i) * place.id
        return csum


if __name__ == "__main__":
    main()
