from collections import defaultdict, deque

from cp_utils.grids import Grid


class Solution:
    """Solution to the problem."""

    def __init__(self, data: Grid[int]):
        self._explosion_memo: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(
            set
        )
        self.grid: Grid[int] = data

    @classmethod
    def parse(cls, file: str) -> "Solution":
        """Parse the given input file and return an instance of `Solution` with the loaded data.

        Args:
            file (str): Input file to parse.

        Returns:
            Solution: Class instance with loaded data.
        """
        grid: Grid[int] = Grid.parse_file(file=file, converter=int)
        return cls(data=grid)

    def determine_number_barrels_exploded(
        self,
        start: tuple[int, int],
    ) -> set[tuple[int, int]]:
        """Get an iterable of all barrels that exploded when exploding the barrel found at `start`."""
        if start in self._explosion_memo:
            return self._explosion_memo[start]

        seen: set[tuple[int, int]] = set()

        q: deque[tuple[int, int]] = deque([start])

        while q:
            curr_pos: tuple[int, int] = q.popleft()

            if curr_pos in seen:
                continue
            seen.add(curr_pos)

            x, y = curr_pos
            curr_value: int = self.grid.get(*curr_pos)
            for neighbour in self.grid.get_neighbours(row=x, col=y):
                if self.grid.get(*neighbour) <= curr_value:
                    q.append(neighbour)

        self._explosion_memo[start] = seen
        return seen

    def part01(self) -> None:
        """Solve Part 01."""
        tlt: int = len(self.determine_number_barrels_exploded(start=(0, 0)))
        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solve Part 02."""
        barrels: set[tuple[int, int]] = self.determine_number_barrels_exploded(
            start=(0, 0)
        )

        end_x, end_y = self.grid.dimensions()
        barrels.update(
            self.determine_number_barrels_exploded(start=(end_x - 1, end_y - 1))
        )

        tlt: int = len(barrels)
        print(f"Part 02: {tlt}")

    # def solve_greedy_triple_fireball(self):
    #     """
    #     Greedy approach to find 3 barrels to ignite simultaneously.
    #     Returns the total number of barrels destroyed.
    #     """
    #     # Track which barrels are still available
    #     remaining_barrels = set()
    #     height, width = self.grid.dimensions()
    #     for row in range(height):
    #         for col in range(width):
    #             remaining_barrels.add((row, col))

    #     selected_barrels = []

    #     # Find 3 barrels using greedy approach
    #     for _ in range(3):
    #         best_barrel = None
    #         max_destroyed = 0

    #         # Try each remaining barrel
    #         for barrel in remaining_barrels:
    #             # Get all barrels that would be destroyed
    #             destroyed = self.determine_number_barrels_exploded(barrel)
    #             # Only count barrels that are still remaining
    #             valid_destroyed = destroyed & remaining_barrels

    #             if len(valid_destroyed) > max_destroyed:
    #                 max_destroyed = len(valid_destroyed)
    #                 best_barrel = barrel

    #         if best_barrel is None:
    #             break

    #         # Select this barrel
    #         selected_barrels.append(best_barrel)

    #         # Remove all barrels that would be destroyed by this explosion
    #         destroyed = self.determine_number_barrels_exploded(best_barrel)
    #         remaining_barrels -= destroyed

    #     # Now simulate setting all 3 selected barrels on fire simultaneously
    #     total_destroyed = set()
    #     for barrel in selected_barrels:
    #         destroyed = self.determine_number_barrels_exploded(barrel)
    #         total_destroyed |= destroyed

    #     return len(total_destroyed)

    # def part03(self) -> None:
    #     """Solve Part 03."""
    #     tlt: int = self.solve_greedy_triple_fireball()

    #     print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/12/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2025/12/input_p02.txt")
    sol2.part02()

    # sol3: Solution = Solution.parse("./inputs/everybody_codes/2025/12/input_p03.txt")
    # sol3.part03()
