class Solution:
    """Solution to the problem."""

    def __init__(self, names: list[str], moves: list[int]):
        self.names: list[str] = names
        self.moves: list[int] = moves

    @classmethod
    def parse(cls, file: str) -> "Solution":
        """Parse the given input file and return an instance of `Solution` with the loaded data.

        Args:
            file (str): Input file to parse.

        Returns:
            Solution: Class instance with loaded data.
        """
        names: list[str] = []
        moves: list[int] = []

        with open(file, 'r') as file:
            p1, p2 = file.read().split("\n\n")

            names = list(p1.strip().split(","))
            moves = [int(move.replace("L", "-").replace("R", "")) for move in p2.strip().split(",")]

        return cls(names=names, moves=moves)

    def _perform_moves(self, starting_index: int = 0, allow_wrapping: bool = False) -> str:
        """Perform the moves on the data, returning the final name.

        Args:
            starting_index (int): Starting index. Default is `0`.
            allow_wrapping (bool): Whether to wrap around. Default is FALSE.

        Returns:
            str: Target person name.
        """
        if allow_wrapping:
            return self.names[sum(self.moves) % len(self.names)]

        for move in self.moves:
            starting_index += move

            if starting_index < 0:
                starting_index = 0
            elif starting_index > len(self.names) - 1:
                starting_index = len(self.names) - 1

        return self.names[starting_index]

    def _perform_moves_with_swapping(self) -> str:
        """Perform the moves, swapping the names around."""
        len_: int = len(self.names)
        names: list[str] = self.names[:]

        for move in self.moves:
            target_index: int = move % len_
            names[0], names[target_index] = names[target_index], names[0]

        return names[0]

    def part01(self) -> None:
        """Solve Part 01."""
        print(f"Part 01: {self._perform_moves()}")

    def part02(self) -> None:
        """Solve Part 02."""
        print(f"Part 02: {self._perform_moves(allow_wrapping=True)}")

    def part03(self) -> None:
        """Solve Part 03."""
        print(f"Part 03: {self._perform_moves_with_swapping()}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/01/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2025/01/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2025/01/input_p03.txt")
    sol3.part03()
