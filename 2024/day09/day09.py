import math
from timeit import timeit
from typing import List

from src.timing import Timing


def determine_minimum_beetles_for_brightness(stamps: List[int], target: int) -> int:
    """
    Given a `target` and the brightness `stamps`, determine the minimum number of stamps needed to reach the target brightness.

    Args:
        stamps (List[int]):
            Available brightness stamps to chose from.
        target (int):
            Target value to meet.

    Returns:
        int: Minimum number of brightness stamps needed to reach the target.

    """
    table: List[List[float]] = [
        [math.inf - 1] * (target + 1) for _ in range(len(stamps) + 1)
    ]

    for i, stamp in enumerate(stamps, start=1):
        table[i][0] = 0

        for j in range(1, len(table[0])):
            if stamp > j:
                # Take from above
                table[i][j] = table[i - 1][j]

            else:
                # Get minimum between above value and value needed when can be split into stamp value
                # i.e: index cannot have stamp value removed from it.
                table[i][j] = min(table[i - 1][j], 1 + table[i][j - stamp])

    return int(table[-1][-1])


def minimum_beetles_for_brightness(stamps: List[int], target: int) -> List[float]:
    """
    Same method as above, but using a 1D approach.
    Returns all the minimum beetles needed for brightness up to the given `target` + 1. Any value used to index the result will return the minimum beetles needed.

    Args:
        stamps (List[int]):
            Available brightness stamps to be used.
        target (int):
            Value up to where the minimum number of beetles needed should be calculated.

    Returns:
        List[float]
            All the calculated minimum values

    """
    table: List[float] = [math.inf] * (target + 1)
    table[0] = 0

    for stamp in stamps:
        for i in range(stamp, target + 1):
            if table[i - stamp] != math.inf:
                table[i] = min(table[i], 1 + table[i - stamp])

    return table


def part_01() -> None:
    """Solution to Part 1"""
    with open("p1.txt") as file:
        values: List[int] = list(map(int, file.readlines()))

    stamps: List[int] = [1, 3, 5, 10]
    beetles: List[int] = [
        determine_minimum_beetles_for_brightness(stamps, val) for val in values
    ]

    tlt: int = sum(beetles)
    print(f"Part 01: {tlt}")


def part_02() -> None:
    """Solution to Part 2"""
    with open("p2.txt") as file:
        values: List[int] = list(map(int, file.readlines()))

    stamps: List[int] = [1, 3, 5, 10, 15, 16, 20, 24, 25, 30]
    beetles: List[int] = [
        determine_minimum_beetles_for_brightness(stamps, val) for val in values
    ]

    tlt: int = sum(beetles)
    print(f"Part 02: {tlt}")


def part_03() -> None:
    """Solution to Part 3"""
    with open("p3.txt") as file:
        values: List[int] = list(map(int, file.readlines()))

    stamps: List[int] = [
        1,
        3,
        5,
        10,
        15,
        16,
        20,
        24,
        25,
        30,
        37,
        38,
        49,
        50,
        74,
        75,
        100,
        101,
    ]

    minimum_beetles: List[float] = minimum_beetles_for_brightness(stamps, max(values))

    tlt: int = 0
    for val in values:
        mid: int = val // 2
        max_: float = math.inf

        for x in range(mid - 200, mid + 200):
            y: int = val - x

            if abs(x - y) <= 100:
                res: float = minimum_beetles[x] + minimum_beetles[y]
                if res < max_:
                    max_ = res

        tlt += int(max_)

    print(f"Part 03: {tlt}")


def main() -> None:
    """Entry point"""

    print(Timing(timeit(part_01, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_02, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_03, number=1)).microseconds, "μs\n")


if __name__ == "__main__":
    main()
