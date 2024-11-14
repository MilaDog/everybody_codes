from typing import List


def part_01() -> None:
    """Solution to Part 1"""
    nails: List[int]

    with open("p1.txt") as file:
        nails = [int(x.strip()) for x in file.readlines()]

    tlt: int = sum(x - min(nails) for x in nails)

    print(f"Part 01: {tlt}")


def part_02() -> None:
    """Solution to Part 2"""
    nails: List[int]

    with open("p2.txt") as file:
        nails = [int(x.strip()) for x in file.readlines()]

    tlt: int = sum(x - min(nails) for x in nails)

    print(f"Part 02: {tlt}")


def part_03() -> None:
    """Solution to Part 3"""
    nails: List[int]

    with open("p3.txt") as file:
        nails = [int(x.strip()) for x in file.readlines()]

    values: List[int] = []

    for nail in nails:
        values.append(sum(abs(nail - x) for x in nails))

    print(f"Part 03: {min(values)}")


def main() -> None:
    """Entry point"""
    part_01()
    part_02()
    part_03()


if __name__ == "__main__":
    main()
