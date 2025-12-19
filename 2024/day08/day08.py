from collections import deque
from math import sqrt, ceil
from timeit import timeit
from typing import Tuple, Deque

from src.timing import Timing


def part_01() -> None:
    """Solution to Part 1"""
    num_blocks: int

    with open("p1.txt") as file:
        num_blocks = int(file.read().strip())

    missing_blocks: int = (int(ceil(sqrt(num_blocks))) ** 2) - num_blocks
    tlt_blocks: int = num_blocks + missing_blocks

    # A = 0.5wh
    # w = 2A/h
    width: int = 2 * tlt_blocks // int(sqrt(tlt_blocks))
    if width % 2 == 0:
        width -= 1

    tlt: int = missing_blocks * width

    print(f"Part 01: {tlt}")


def part_02() -> None:
    """Solution to Part 2"""
    num_priests: int
    num_acolytes: int = 1111

    with open("p2.txt") as file:
        num_priests = int(file.read().strip())

    tlt_blocks_available: int = 20_240_000
    tlt_blocks_used: int = 0

    # Thickness: (prev_thickness * num_priests) % 1111
    thickness: int = 1
    tlt_layers: int = 0

    flag_initial: bool = False
    while tlt_blocks_used < tlt_blocks_available:
        if not flag_initial:
            tlt_layers += 1
            flag_initial = True

        else:
            # Determine next thickness
            thickness = (thickness * num_priests) % num_acolytes
            tlt_layers += 1

        # Determine number of blocks used
        tlt_blocks_used += (tlt_layers * 2 - 1) * thickness

    needed_blocks: int = abs(tlt_blocks_available - tlt_blocks_used)

    tlt: int = needed_blocks * (tlt_layers * 2 - 1)

    print(f"Part 02: {tlt}")


def part_03() -> None:
    """Solution to Part 3"""
    num_priests: int
    num_acolytes: int = 10

    with open("p3.txt") as file:
        num_priests = int(file.read().strip())

    tlt_blocks_available: int = 202_400_000
    tlt_blocks_used: int = 0

    # Thickness: (prev_thickness * num_priests) % num_acolytes
    thickness: int = 1
    tlt_layers: int = 0
    dq: Deque[Tuple[int, int]] = deque()

    flag_initial: bool = False
    while tlt_blocks_used < tlt_blocks_available:
        if not flag_initial:
            tlt_layers += 1
            flag_initial = True

        else:
            # Determine next thickness
            thickness = ((thickness * num_priests) % num_acolytes) + num_acolytes
            tlt_layers += 1

        # Determine number of blocks used
        dq.append((tlt_layers, thickness))
        tlt_blocks_used += (tlt_layers * 2 - 1) * thickness

    max_layer, prev_height = dq.pop()
    max_width: int = max_layer * 2 - 1

    while dq:
        curr: Tuple[int, int] = dq.pop()
        prev_height += curr[1]
        to_remove: int = (num_priests * max_width) * prev_height % num_acolytes
        tlt_blocks_used -= to_remove * ((curr[0] != 1) + 1)

    tlt: int = abs(tlt_blocks_available - tlt_blocks_used)

    print(f"Part 03: {tlt}")


def main() -> None:
    """Entry point"""

    print(Timing(timeit(part_01, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_02, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_03, number=1)).microseconds, "μs\n")


if __name__ == "__main__":
    main()
