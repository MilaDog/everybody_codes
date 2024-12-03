from timeit import timeit
from typing import List, Dict, Set

from utils.timing import Timing


def part_01() -> None:
    """Solution to Part 1"""

    with open("p1.txt") as file:
        lines: List[List[int]] = [
            list(x)
            for x in (zip(*[list(map(int, x.split(" "))) for x in file.readlines()]))
        ]

    curr_row: int = 0
    cnter: int = 0
    called_numbers: List[str] = []

    while cnter < 10:
        target_person: int = lines[curr_row].pop(0)
        curr_row += 1

        # Wrap around check
        curr_row %= len(lines)

        # Determining where the person is placed
        row_size: int = len(lines[curr_row])
        if target_person <= row_size:
            # Goes on the left
            lines[curr_row].insert(target_person - 1, target_person)

        else:
            # Goes on the right
            lines[curr_row].insert(
                row_size - (target_person - row_size) + 1, target_person
            )

        called_numbers.append("".join(map(str, [x[0] for x in lines])))
        cnter += 1

    tlt: str = called_numbers[-1]
    print(f"Part 01: {tlt}")


def part_02() -> None:
    """Solution to Part 2"""
    with open("p2.txt") as file:
        lines: List[List[int]] = [
            list(x)
            for x in (zip(*[list(map(int, x.split(" "))) for x in file.readlines()]))
        ]

    curr_row: int = 0
    cnter: int = 0
    seen: Dict[str, int] = {}
    tlt: int = 0

    while True:
        cnter += 1
        target_person: int = lines[curr_row].pop(0)
        curr_row += 1

        # Wrap around check
        curr_row %= len(lines)

        # Determining where the person is placed
        row_size: int = len(lines[curr_row])
        if target_person <= row_size:
            # Goes on the left
            lines[curr_row].insert(target_person - 1, target_person)

        else:
            # Goes on the right
            lines[curr_row].insert(
                row_size - (target_person - row_size) + 1, target_person
            )

        called_number: str = "".join(map(str, [x[0] for x in lines]))

        if not seen.get(called_number):
            seen[called_number] = 1

        else:
            seen[called_number] += 1

            if seen[called_number] == 2024:
                tlt += int(called_number) * cnter
                break

    print(f"Part 02: {tlt}")


def part_03() -> None:
    """Solution to Part 3"""
    with open("p3.txt") as file:
        lines: List[List[int]] = [
            list(x)
            for x in (zip(*[list(map(int, x.split(" "))) for x in file.readlines()]))
        ]

    curr_row: int = 0
    cnter: int = 0
    seen: Set[int] = set()
    best: int = 0

    while True:
        cnter += 1
        target_person: int = lines[curr_row].pop(0)
        curr_row += 1

        # Wrap around check
        curr_row %= len(lines)

        # Determining where the person is placed
        row_size: int = len(lines[curr_row])
        if target_person <= row_size:
            # Goes on the left
            lines[curr_row].insert(target_person - 1, target_person)

        else:
            # Goes on the right
            lines[curr_row].insert(
                row_size - (target_person - row_size) + 1, target_person
            )

        called_number: int = int("".join(map(str, [x[0] for x in lines])))

        if called_number in seen and called_number > best:
            best = called_number
            print(best)

        else:
            seen.add(called_number)

    tlt: int = max(map(int, seen.keys()))
    print(f"Part 03: {tlt}")
    # 6296100210021002


def main() -> None:
    """Entry point"""

    print(Timing(timeit(part_01, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_02, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_03, number=1)).microseconds, "μs\n")


if __name__ == "__main__":
    main()
