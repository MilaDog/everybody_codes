class Solution:
    """Solution to the problem."""

    def __init__(self, data: list[str]):
        self.data: list[str] = data

    @classmethod
    def parse(cls, file: str) -> "Solution":
        """Parse the given input file and return an instance of `Solution` with the loaded data.

        Args:
            file (str): Input file to parse.

        Returns:
            Solution: Class instance with loaded data.
        """
        data: list[str] = []

        with open(file, "r") as f:
            data = f.readlines()

        return cls(data=data)

    def part01(self) -> None:
        """Solve Part 01."""
        raise NotImplementedError

    def part02(self) -> None:
        """Solve Part 02."""
        raise NotImplementedError

    def part03(self) -> None:
        """Solve Part 03."""
        raise NotImplementedError


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/03/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2025/03/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2025/03/input_p03.txt")
    sol3.part03()
