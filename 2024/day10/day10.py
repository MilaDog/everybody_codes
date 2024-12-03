from timeit import timeit
from typing import Set, List

from utils.timing import Timing


def s(grid):
    res = ""
    for x in range(2, len(grid) - 2):
        for y in range(2, len(grid[0]) - 2):
            res += grid[x][y]

    return res


def determine_runic_word(grid) -> str:
    res: str = ""
    for x in range(2, len(grid) - 2):
        for y in range(2, len(grid[0]) - 2):
            res += grid[x][y]
    return res


def ff(grid, fix=False):
    for x in range(2, len(grid) - 2):
        for y in range(2, len(grid[0]) - 2):
            try:
                if not fix:
                    possible_values = list(
                        set(grid[x]) & set(list(zip(*grid))[y]) - {".", "?"}
                    )
                    if len(possible_values) == 1:
                        grid[x][y] = possible_values[0]

                else:
                    if grid[x][y] == ".":
                        c = set(list(zip(*grid))[y])
                        cc = set(list(zip(*grid))[y][2:7])
                        r = set(grid[x])
                        rr = set(grid[x][2:7])
                        rev = {"?", "."}

                        possible_values = list(c - cc - rev) + list(r - rr - rev)
                        if len(possible_values) != 1:
                            continue

                        missing_sym = possible_values[0]
                        grid[x][y] = missing_sym

                        for i in range(8):
                            if grid[i][y] == "?":
                                grid[i][y] = missing_sym

                            if grid[x][i] == "?":
                                grid[x][i] = missing_sym

            except Exception:
                pass

    return grid


def display(grid):
    for g in grid:
        print("".join(g))
    print()


def solve_grid(grid):
    for x in range(2, len(grid) - 2):
        for y in range(2, len(grid[0]) - 2):
            if grid[x][y] != ".":
                continue

            # Determine potential value
            remove_values: Set[str] = set(".?")
            row_values: Set[str] = set(grid[x]) - remove_values
            col_values: Set[str] = set(list(zip(*grid))[y]) - remove_values
            common_values: Set[str] = row_values & col_values

            if len(common_values) == 1:
                grid[x][y] = common_values.pop()


def resolve_question_marks(grid):
    for x in range(2, len(grid) - 2):
        for y in range(2, len(grid[0]) - 2):
            if grid[x][y] != ".":
                continue

            # Determine question mark value
            remove_values: Set[str] = set(".")
            row_values: Set[str] = set(grid[x][2:-2]) - remove_values
            edge_row_values: Set[str] = set(grid[x]) - remove_values
            col_values: Set[str] = set(list(zip(*grid))[y][2:-2]) - remove_values
            edge_col_values: Set[str] = set(list(zip(*grid))[y]) - remove_values
            # print()
            # print(row_values, edge_row_values)
            # print(col_values, edge_col_values)
            # print()

            if "?" in edge_row_values:
                missing_values: Set[str] = (
                    edge_col_values - col_values
                ) - edge_row_values

                if len(missing_values) == 1:
                    # Replace at index and the question mark
                    value: str = missing_values.pop()

                else:
                    edge_values: List[str] = list(list(zip(*grid))[y])
                    value = edge_values[:2][x - 2] if x < 4 else edge_values[-2:][x - 4]

                grid[x][y] = value
                grid[x] = list("".join(grid[x]).replace("?", value))

                # else:
                # print("in row")
                # print(missing_values)
                # print("col", col_values, edge_col_values)
                # print("row", row_values, edge_row_values)
                # print()

            elif "?" in edge_col_values:
                missing_values: Set[str] = (
                    edge_row_values - row_values
                ) - edge_col_values

                if len(missing_values) == 1:
                    # Replace at index and the question mark
                    value: str = missing_values.pop()

                else:
                    print(y, grid[x][:2], grid[x][-2:])
                    value = grid[x][:2][y - 2] if y < 4 else grid[x][-2:][y - 4]

                grid[x][y] = value

                for i in range(8):
                    if grid[i][y] == "?":
                        grid[i][y] = value

                # else:
                # print("in col")
                # print(missing_values)
                # print("col", col_values, edge_col_values)
                # print("row", row_values, edge_row_values)
                # print()


def determine_runic_word_value(runic_word: str) -> int:
    ltrs: str = ".abcdefghijklmnopqrstuvwxyz".upper()

    tlt: int = 0
    for i, x in enumerate(runic_word, start=1):
        tlt += i * ltrs.index(x)

    return tlt


# def part_01() -> None:
#     """Solution to Part 1"""
#     with open("p1.txt") as file:
#         grid = [list(x.strip()) for x in file.readlines()]
#
#     res = ""
#     for x in range(2, len(grid) - 2):
#         for y in range(2, len(grid[0]) - 2):
#             res += list(set(grid[x]) & set(list(zip(*grid))[y]) - {"."})[0]
#
#     print(f"Part 01: {res}")


# def part_02() -> None:
#     """Solution to Part 2"""
#     with open("p2.txt") as file:
#         grids = []
#         lines = [line.strip() for line in file.readlines()]
#
#         for i in range(0, len(lines), 9):
#             grid_lines = [line.split(" ") for line in lines[i:i + 8]]
#             grids += list(zip(*grid_lines))
#
#     wrds = [f(grid) for grid in grids]
#     ltrs = " abcdefghijklmnopqrstuvwxyz".upper()
#     tlt: int = 0
#
#     for w in wrds:
#         for i, x in enumerate(w, start=1):
#             tlt += i * ltrs.index(x)
#
#     print(f"Part 02: {tlt}")


def part_03() -> None:
    """Solution to Part 3"""
    # with open("p3.txt") as file:
    #     lines = file.readlines()

    with open("p3.txt") as file:
        lines = [line.strip() for line in file.readlines()]

        grids = []
        t = []
        for i in range(0, len(lines) - 2, 6):
            t.append(lines[i : i + 8])

        for x in t:
            lines = ["".join(x) for x in list(zip(*x))]

            for i in range(0, len(lines) - 2, 6):
                grids.append([list(x) for x in list(zip(*lines[i : i + 8]))])

    num_in_row = len(grids) // len(t)
    sections = [grids[i : i + num_in_row] for i in range(0, len(grids), num_in_row)]

    tlt: int = 0

    for q, section in enumerate(sections):
        for i, grid in enumerate(section):
            prev_runic_word: str = "NOT"
            runic_word: str = ""

            while prev_runic_word != runic_word:
                solve_grid(grid)
                resolve_question_marks(grid)

                # fix the next grid in the row
                if i < len(sections[0]) - 1:
                    # copy right side to next grid
                    for ii, r in enumerate(grid):
                        section[i + 1][ii][:2] = r[-2:]

                if i > 0:
                    # copy left side to previous grid
                    for ii, r in enumerate(grid):
                        section[i - 1][ii][-2:] = r[:2]

                # if q < len(sections) - 1:
                #     # copy bottom to top of below grid
                #     sections[q + 1][i][:2] = grid[-2:]

                # if q > 0:
                #     # copy top to bottom of above grid
                #     sections[q - 1][i][-2:] = grid[:2]

                prev_runic_word = runic_word
                runic_word = determine_runic_word(grid)

            if "." not in runic_word:
                tlt += determine_runic_word_value(runic_word)

            # display(grid)

    print(f"Part 03: {tlt}")


def main() -> None:
    """Entry point"""

    # print(Timing(timeit(part_01, number=1)).microseconds, "μs\n")
    # print(Timing(timeit(part_02, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_03, number=1)).microseconds, "μs\n")


if __name__ == "__main__":
    main()
