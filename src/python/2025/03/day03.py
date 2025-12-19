import re


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
            data = list(map(int, re.findall(r"(\d+)", f.read())))

        return cls(data=data)

    def part01(self) -> None:
        """Solve Part 01."""
        tlt: int = sum(set(self.data))

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solve Part 02."""
        tlt: int = sum(sorted(list(set(self.data)))[:20])

        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solve Part 03."""
        box_sets: dict[int, set[int]] = {0: set()}

        for box in sorted(self.data, reverse=True):
            indx: int = 0

            if box not in box_sets[indx]:
                box_sets[indx].add(box)
                continue

            while True:
                if (indx + 1) in box_sets.keys():
                    if box not in box_sets[indx + 1]:
                        box_sets[indx + 1].add(box)
                        break

                else:
                    box_sets[indx + 1] = {box}
                    break

                indx += 1

        print(f"Part 03: {len(box_sets.keys())}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/03/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2025/03/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2025/03/input_p03.txt")
    sol3.part03()
