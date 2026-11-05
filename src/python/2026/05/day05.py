from collections import deque
from copy import copy


class Solution:
    """Solution to the problem."""

    def __init__(self, data: list[list[str]]):
        self.data: list[list[str]] = data
        self._height: int = len(self.data)
        self._width: int = len(self.data[0])
        self._mid: tuple[int, int] = (self._height // 2, self._width // 2)

    @classmethod
    def parse(cls, file: str) -> "Solution":
        """Parse the given input file and return an instance of `Solution` with the loaded data.

        Args:
            file (str): Input file to parse.

        Returns:
            Solution: Class instance with loaded data.
        """
        data: list[list[str]] = []

        with open(file, "r") as f:
            for line in f.readlines():
                data.append(list(line.strip()))

        return cls(data=data)

    def display_grid(self, grid: list[list[str]]):
        for x, row in enumerate(self.data):
            for y, col in enumerate(row):
                print(col, end="")
            print()

    def is_within_grid(self, x: int, y: int) -> bool:
        """Whether the position falls within the grid."""
        return 0 <= x < self._height and 0 <= y < self._width

    def get_neighbours(
        self, x: int, y: int, ignore_out_of_bounds: bool = True
    ) -> list[tuple[int, int]]:
        """Get a list of neighbouring cells, adhering to grid constraints."""
        neighbours: list[tuple[int, int]] = []

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0:
                    continue

                new_position: tuple[int, int] = (x + dx, y + dy)
                if not ignore_out_of_bounds:
                    neighbours.append(new_position)
                elif self.is_within_grid(*new_position):
                    neighbours.append(new_position)

        return neighbours

    def set_sea_water(self, grid: list[list[str]]) -> list[list[str]]:
        local_grid = copy(grid)
        for x, row in enumerate(grid):
            for y, col in enumerate(row):
                if col != "#":
                    local_grid[x][y] = "."

        return local_grid

    def can_reconstruct_land(self, x: int, y: int, grid: list[list[str]]) -> bool:
        tlt: int = 0
        for new_x, new_y in self.get_neighbours(x, y):
            if grid[new_x][new_y] in "#1":
                tlt += 1

        return tlt >= 5

    def can_reconstruct_shoreline(self, x: int, y: int, grid: list[list[str]]) -> bool:
        tlt: int = 0
        for new_x, new_y in self.get_neighbours(x, y, ignore_out_of_bounds=False):
            try:
                if grid[new_x][new_y] in "=":
                    tlt += 1
            except IndexError:
                tlt += 1

        return tlt >= 5

    def reconstruct_land(self) -> list[list[str]]:
        q = deque([self._mid])
        seen: set[tuple[int, int]] = set()
        local_grid = copy(self.data)

        while q:
            curr_pos = q.popleft()

            if curr_pos in seen:
                continue
            seen.add(curr_pos)

            for neighbour in self.get_neighbours(*curr_pos):
                if self.can_reconstruct_land(*neighbour, grid=local_grid):
                    local_grid[neighbour[0]][neighbour[1]] = "#"
                    q.append(neighbour)

        return local_grid

    def reconstruct_shoreline(self, grid: list[list[str]]) -> list[list[str]]:
        local_grid = copy(grid)

        for x, row in enumerate(local_grid):
            for y, col in enumerate(row):
                if local_grid[x][y] == "#" and any(
                    local_grid[nx][ny] == "." for nx, ny in self.get_neighbours(x, y)
                ):
                    local_grid[x][y] = "="

        while True:
            made_change: bool = False

            for x, row in enumerate(local_grid):
                for y, col in enumerate(row):
                    if local_grid[x][y] == "#" and self.can_reconstruct_shoreline(
                        x, y, grid=local_grid
                    ):
                        local_grid[x][y] = "="
                        made_change = True

            if not made_change:
                break

        return local_grid

    def part01(self) -> None:
        """Solve Part 01."""
        tlt: int = sum(c == "#" for r in self.reconstruct_land() for c in r)
        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solve Part 02."""
        grid: list[list[str]] = self.reconstruct_land()
        grid = self.set_sea_water(grid)
        grid = self.reconstruct_shoreline(grid)

        tlt: int = sum(c == "=" for r in grid for c in r)
        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solve Part 03."""
        # TODO - finish
        grid: list[list[str]] = self.reconstruct_land()
        grid = self.set_sea_water(grid)
        grid = self.reconstruct_shoreline(grid)

        tlt: int = sum(c == "=" for r in grid for c in r)
        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2026/05/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2026/05/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2026/05/input_p03.txt")
    sol3.part03()
