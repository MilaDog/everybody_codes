class Solution:
    """Solution to the problem."""

    def __init__(self, data: list[list[int]]):
        self.data: list[list[int]] = data

    @classmethod
    def parse(cls, file: str) -> "Solution":
        """Parse the given input file and return an instance of `Solution` with the loaded data.

        Args:
            file (str): Input file to parse.

        Returns:
            Solution: Class instance with loaded data.
        """
        data: list[list[int]] = []

        with open(file, "r") as f:
            for line in f.readlines():
                data.append(list(map(int, line.strip().split("|"))))

        return cls(data=data)

    def part01(self) -> None:
        """Solve Part 01."""
        tlt: int = round(self.data[0][0] / self.data[-1][0] * 2025)

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solve Part 02."""
        tlt: int = round(self.data[-1][0] / self.data[0][0] * 10000000000000)

        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solve Part 03."""
        tlt: float = 1

        for pair1, pair2 in zip(self.data, self.data[1:]):
            tlt *= pair1[-1] / pair2[0]

        print(f"Part 03: {round(tlt * 100)}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/04/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2025/04/input_p02.txt")
    sol2.part02()

    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/04/input_p03.txt")
    sol1.part03()
