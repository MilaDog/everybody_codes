from functools import lru_cache


class Solution:
    """Solution to the problem."""

    def __init__(self, data: list[list[str]]):
        self.data: list[list[str]] = data

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
                data.append(line.strip().replace("-", " ").split())

        return cls(data=data)

    def normalise_codes(self, code1: str, code2: str) -> tuple[str, str]:
        """Normalise the given codes to be the same length, according to `code2` length."""
        lc1, lc2 = len(code1), len(code2)

        if lc1 == lc2:
            return code1, code2

        if lc1 < lc2:
            expand_by: int = lc2 // lc1 + 1
            return (code1 * expand_by)[-lc2:], code2

        return code1[-lc2:], code2

    def determine_iso_score(self, code1: str, code2: str) -> int:
        """Determine the decimal value for the given ISO code."""
        score: int = 0
        len_n1: int = len(code1)
        len_n2: int = len(code2)
        for i in range(max(len_n1, len_n2)):
            score += int(code1[i]) ** (len_n1 - 1 - i) * int(code2[i])

        return score

    @lru_cache(maxsize=None)
    def determine_valid_iso(self, code1: str, code2: str) -> int:
        """Determine is the ISO2 is valid or not. Valid if there exists a `code2` smaller than the given `code2` that results in the same decimal value."""
        current_score: int = self.determine_iso_score(
            *self.normalise_codes(code1, code2)
        )

        for new_code2 in range(int(code2)):
            new_current_score: int = self.determine_iso_score(
                *self.normalise_codes(code1, str(new_code2))
            )

            if new_current_score == current_score:
                return 0

        return current_score

    def part01(self) -> None:
        """Solve Part 01."""
        tlt: int = sum(
            self.determine_iso_score(code1, code2) for _, code1, code2 in self.data
        )
        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solve Part 02."""
        tlt: int = sum(
            self.determine_iso_score(*self.normalise_codes(code1, code2))
            for _, code1, code2 in self.data
        )
        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solve Part 03."""
        tlt: int = sum(
            self.determine_valid_iso(code1, code2) for _, code1, code2 in self.data
        )
        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2026/03/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2026/03/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2026/03/input_p03.txt")
    sol3.part03()
