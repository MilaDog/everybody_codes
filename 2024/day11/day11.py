from collections import Counter
from timeit import timeit
from typing import List, Dict, Counter as Counter_

from utils.timing import Timing


def solve(values: Dict[str, List[str]], days: int, start: str) -> int:
    """
    Solve problem for Parts 1 and 2.

    Args:
        values (Dict[str, List[str]]):
            Parsed input data.
        days (int):
            How many days to calculate.
        start (str):
            Where to start from when solving the problem.

    Returns:
        int:
            Total population count after the specified number of days.

    """

    c1: Counter_[str] = Counter([start])
    for _ in range(days):
        c2: Counter_[str] = Counter()

        for k, v in c1.items():
            c3: Counter_[str] = Counter(values[k])

            for kk in c3.keys():
                c3[kk] *= v

            c2.update(c3)

        c1.clear()
        c1 = c2

    return sum(c1.values())


def part_01() -> None:
    """Solution to Part 1"""
    with open("p1.txt") as file:
        values: Dict[str, List[str]] = {}

        for line in file.readlines():
            k, v = line.strip().split(":")
            values[k] = v.split(",")

    tlt: int = solve(values=values, days=4, start="A")
    print(f"Part 01: {tlt}")


def part_02() -> None:
    """Solution to Part 2"""
    with open("p2.txt") as file:
        values: Dict[str, List[str]] = {}

        for line in file.readlines():
            k, v = line.strip().split(":")
            values[k] = v.split(",")

    tlt: int = solve(values=values, days=10, start="Z")
    print(f"Part 02: {tlt}")


def part_03() -> None:
    """Solution to Part 3"""
    with open("p3.txt") as file:
        values: Dict[str, List[str]] = {}

        for line in file.readlines():
            k, v = line.strip().split(":")
            values[k] = v.split(",")

    population: List[int] = []

    for val in values.keys():
        c1: Counter_[str] = Counter([val])

        for _ in range(20):
            c2: Counter_[str] = Counter()

            for k, v in c1.items():
                c3: Counter_[str] = Counter(values[k])

                for kk in c3.keys():
                    c3[kk] *= v

                c2.update(c3)

            c1.clear()
            c1 = c2

        population.append(sum(c1.values()))

    tlt: int = max(population) - min(population)
    print(f"Part 03: {tlt}")


def main() -> None:
    """Entry point"""

    print(Timing(timeit(part_01, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_02, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_03, number=1)).microseconds, "μs\n")


if __name__ == "__main__":
    main()
