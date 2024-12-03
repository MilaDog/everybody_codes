from timeit import timeit
from typing import List, Tuple

from utils.timing import Timing


def parse_input(file_name: str) -> List[List[int]]:
    """
    Parse the input data.

    Args:
        file_name (str):
            Name of the input data file.

    Returns:
        List[List[int]]:
            Parsed input data.

    """
    with open(f"{file_name}.txt", "r") as file:
        grid: List[List[int]] = [
            list(map(int, list(x.strip())))
            for x in file.read().replace("#", "1").replace(".", "0").splitlines()
        ]
    return grid


def valid_block_to_dig(
    grid: List[List[int]], coords: Tuple[int, int], include_diagonals: bool = False
) -> bool:
    """
    Check if the block at the given coordinates is valid to dig. Include diagonals checking is by default False.
    A block is valid to mine if its adjacent block values are greater-than or equal to the value of the block at the given coordinate.

    Args:
        grid (List[List[int]]):
            Grid to be checked against.
        coords (Tuple[int, int]):
            Coordinates in grid to check.
        include_diagonals (bool):
            If adjacent diagonals should be checked.

    Returns:
        bool:
            If the block is valid to mine.

    """
    offsets: List[Tuple[int, int]] = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    if include_diagonals:
        offsets += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    x: int
    y: int
    x, y = coords

    # Ignore 0
    if grid[x][y] == 0:
        return False

    for dx, dy in offsets:
        if x + dx < 0 or x + dx >= len(grid) or y + dy < 0 or y + dy >= len(grid[0]):
            return False

        if grid[x + dx][y + dy] < grid[x][y]:
            return False

    return True


def solve(file_name: str) -> int:
    """
    Solve the problem.

    Args:
        file_name (str):
            Name of the input data file to use.

    Returns:
        int:
            Sum of all the earth blocks that can be removed.

    """
    grid: List[List[int]] = parse_input(file_name=file_name)
    include_diagonals: bool = file_name == "p3"

    has_changed: bool = True
    while has_changed:
        has_changed = False

        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if valid_block_to_dig(
                    grid=grid, coords=(x, y), include_diagonals=include_diagonals
                ):
                    grid[x][y] += 1
                    has_changed = True

    return sum(sum(x) for x in grid)


def display(grid: List[List[int]]) -> None:
    for row in grid:
        print("".join(map(str, row)).replace("0", "."))
    print()


def part_01() -> None:
    """Solution to Part 1"""
    tlt: int = solve(file_name="p1")
    print(f"Part 01: {tlt}")


def part_02() -> None:
    """Solution to Part 2"""
    tlt: int = solve(file_name="p2")
    print(f"Part 02: {tlt}")


def part_03() -> None:
    """Solution to Part 3"""
    tlt: int = solve(file_name="p3")
    print(f"Part 03: {tlt}")


def main() -> None:
    """Entry point"""

    print(Timing(timeit(part_01, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_02, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_03, number=1)).microseconds, "μs\n")


if __name__ == "__main__":
    main()
