from collections.abc import Callable
from functools import lru_cache


class Solution:
    """Solution to the problem."""

    def __init__(self, data: list[int]):
        self.data: list[int] = data

    @classmethod
    def parse(cls, file: str) -> "Solution":
        """Parse the given input file and return an instance of `Solution` with the loaded data.

        Args:
            file (str): Input file to parse.

        Returns:
            Solution: Class instance with loaded data.
        """
        data: list[int] = []

        with open(file, "r") as f:
            for line in f.readlines():
                data += list(map(int, line.strip().split(",")))

        return cls(data=data)

    @lru_cache(maxsize=None)
    def determine_extra_pinecones_needed(
        self,
        current_pinecones: int,
        eval_func: Callable[[int], int],
        inc_amount: int,
        base_size: int,
    ) -> int:
        """Determine the number of extra pinecones needed.

        Taking the current number of found pinecones, the base formation size, a function to determine the total
        number of pinecones needed, determine the next formation size that is needed based on the number of current
        pinecones. Then determine the number of extra pinecones to collect to meet the target formation.

        Args:
            current_pinecones (int): Current number of pinecones.
            eval_func (Callable[[int], int]): Function to determine the total number of pinecones needed.
            inc_amount (int): Increment size for `eval_func`.
            base_size (int): Smallest possible size of `eval_func`.

        Returns:
            int: Number of extra pinecones to collect.
        """
        n = base_size
        while eval_func(n) < current_pinecones:
            n += inc_amount
        return eval_func(n) - current_pinecones

    def part01(self) -> None:
        """Solve Part 01."""
        res: int = sum(
            self.determine_extra_pinecones_needed(
                current_pinecones=x,
                eval_func=lambda val: val * val,
                inc_amount=1,
                base_size=1,
            )
            for x in self.data
        )

        print(f"Part 01: {res}")

    def part02(self) -> None:
        """Solve Part 02."""
        res: int = sum(
            self.determine_extra_pinecones_needed(
                current_pinecones=x,
                eval_func=lambda val: max(8, -(-val // 4) * 4),
                inc_amount=1,
                base_size=3,
            )
            for x in self.data
        )
        print(f"Part 02: {res}")

    def part03(self) -> None:
        """Solve Part 03."""
        res: int = sum(
            self.determine_extra_pinecones_needed(
                current_pinecones=x,
                eval_func=lambda val: val * val - 1,
                inc_amount=2,
                base_size=3,
            )
            for x in self.data
        )
        print(f"Part 03: {res}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2026/01/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2026/01/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2026/01/input_p03.txt")
    sol3.part03()
