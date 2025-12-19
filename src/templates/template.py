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

        with open(file, 'r') as file:
            data = file.readlines()

        return cls(data=data)


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/%%YEAR%%/%%DAY%%/input_p01.txt")
    sol2: Solution = Solution.parse("./inputs/everybody_codes/%%YEAR%%/%%DAY%%/input_p02.txt")
    sol3: Solution = Solution.parse("./inputs/everybody_codes/%%YEAR%%/%%DAY%%/input_p03.txt")
