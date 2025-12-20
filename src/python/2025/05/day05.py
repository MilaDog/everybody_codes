from dataclasses import dataclass, field


@dataclass
class FishboneInstructions:
    """Representation of the instructions for the construction of a fishbone."""

    id_: int
    bones: list[int]
    fishbone: dict[int, list[int]]
    _determined_score: bool = field(default=False)

    def __lt__(self, other):
        return self.compare_swords(other=other)

    def __repr__(self):
        return f"id={self.id_}"

    def get_sword_score(self) -> int:
        return int(
            "".join(str(x) if x != -1 else "" for _, x, _ in self.fishbone.values())
        )

    def determine_fishbone_sword_score(self) -> int:
        """Construct the fishbone to make the sword, returning the score of the constructed sword.

        Returns:
            int: Score of the constructed fishbone sword.
        """
        if self._determined_score:
            return self.get_sword_score()

        self.fishbone[0][1] = self.bones[0]

        for bone in self.bones[1:]:
            indx: int = 0

            while True:
                a, b, c = self.fishbone[indx]

                if a == -1 and bone < b:
                    self.fishbone[indx][0] = bone
                    break

                elif c == -1 and bone > b:
                    self.fishbone[indx][-1] = bone
                    break

                else:
                    # check for a next row
                    if indx + 1 in self.fishbone.keys():
                        indx += 1

                    else:
                        self.fishbone[indx + 1] = [-1, bone, -1]
                        break

        self._determined_score = True
        return self.get_sword_score()

    def compute_level_scores(self) -> dict[int, int]:
        """Determine the level scores for each level of the fishbone sword.

        Returns:
            dict[int, int]: Scores for each level of the fishbone sword.
        """
        return {
            k + 1: int("".join(str(x) if x != -1 else "" for x in v))
            for k, v in self.fishbone.items()
        }

    def compare_swords(self, other: "FishboneInstructions") -> bool:
        """Compare two fishbone swords to determine which one is better. True for the given sword, else false.

        Args:
            other (FishboneInstructions): Fishbone sword to be compared to.

        Returns:
            bool: Which fishbone sword is better.
        """
        if self.get_sword_score() != other.get_sword_score():
            return other.get_sword_score() <= self.get_sword_score()

        # comparing levels
        for f1, f2 in zip(
            self.compute_level_scores().values(), other.compute_level_scores().values()
        ):
            if f1 != f2:
                return f2 < f1

        return other.id_ < self.id_


class Solution:
    """Solution to the problem."""

    def __init__(self, data: list[FishboneInstructions]):
        self.data: list[FishboneInstructions] = data

    @classmethod
    def parse(cls, file: str) -> "Solution":
        """Parse the given input file and return an instance of `Solution` with the loaded data.

        Args:
            file (str): Input file to parse.

        Returns:
            Solution: Class instance with loaded data.
        """
        data: list[FishboneInstructions] = []

        with open(file, "r") as f:
            for line in f.readlines():
                p1, p2 = line.strip().split(":")
                data.append(
                    FishboneInstructions(
                        id_=int(p1),
                        bones=list(map(int, p2.strip().split(","))),
                        fishbone={0: [-1, -1, -1]},
                    )
                )

        return cls(data=data)

    def part01(self) -> None:
        """Solve Part 01."""
        tlt: int = self.data[0].determine_fishbone_sword_score()

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solve Part 02."""
        sword_scores: list[int] = [
            x.determine_fishbone_sword_score() for x in self.data
        ]
        tlt: int = max(sword_scores) - min(sword_scores)

        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solve Part 03."""
        for sword in self.data:
            sword.determine_fishbone_sword_score()

        self.data.sort()

        tlt: int = sum(x.id_ * i for i, x in enumerate(self.data, 1))
        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/05/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2025/05/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2025/05/input_p03.txt")
    sol3.part03()
