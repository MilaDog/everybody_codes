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
            data = list(f.read().strip())

        return cls(data=data)

    def determine_number_mentors_novice_pairs(self, novice: str, mentor: str) -> int:
        """Determine the number of mentors available for the given novice.
        Args:
            novice (str): Novice to check for.
            mentor (str): Mentor to check for.

        Returns:
            int: number of mentors available for the novices.
        """
        tlt: int = 0

        seen: int = 0
        for char in self.data:
            if char == mentor:
                seen += 1
                continue

            if char == novice:
                tlt += seen
                continue

        return tlt

    def part01(self) -> None:
        """Solve Part 01."""
        tlt: int = self.determine_number_mentors_novice_pairs(novice="a", mentor="A")

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solve Part 02."""
        tlt: int = 0

        for char in set([x.lower() for x in self.data]):
            tlt += self.determine_number_mentors_novice_pairs(
                novice=char.lower(), mentor=char.upper()
            )

        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solve Part 03. A very slow implementation."""
        tlt: int = 0

        look_distance: int = 1000
        repeats: int = 1000
        lngth: int = len(self.data)

        if look_distance >= lngth * repeats:
            for ltr in ("a", "b", "c"):
                novices: list[int] = [int(c == ltr) for c in self.data] * repeats
                mentors: list[int] = [
                    int(c == ltr.upper()) for c in self.data
                ] * repeats

                for i, mentor in enumerate(mentors):
                    if mentor == 1:
                        lowerbound: int = max(0, i - look_distance)
                        upperbound: int = min(i + 1 + look_distance, len(novices))
                        tlt += sum(novices[lowerbound:upperbound])

        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/06/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2025/06/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2025/06/input_p03.txt")
    sol3.part03()
