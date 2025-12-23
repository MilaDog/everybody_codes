from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from math import prod

from src.python.common.dsu import UnionFind


@dataclass(frozen=True)
class DNA:
    """Representation of a DNA sequence in the solution."""

    id_: int
    dna: str

    def dissimilarity(self, other: "DNA") -> int:
        """Determine the dissimilarity between two DNA genes.

        Args:
            other (DNA): Other DNA to compare to.

        Returns:
            int: Dissimilarity score.
        """
        return sum(a != b for a, b in zip(self.dna, other.dna))

    def similarity(self, other: "DNA") -> int:
        """Determine the similarity between two DNA genes.

        Args:
            other (DNA): Other DNA to compare to.

        Returns:
            int: similarity score.
        """
        return sum(a == b for a, b in zip(self.dna, other.dna))

    def determine_if_potential_parents(self, parent1: "DNA", parent2: "DNA") -> bool:
        """Determine if the target DNA belows to the provided parent pair.

        Args:
            parent1 (DNA): Parent one DNA.
            parent2 (DNA): Parent two DNA.

        Returns:
            bool: Whether the target DNA is a child of the parent pair.
        """
        for a, x, y in zip(self.dna, parent1.dna, parent2.dna):
            if not (a == x or a == y):
                return False

        return True


class Solution:
    """Solution to the problem."""

    def __init__(self, data: list[DNA]):
        self.data: dict[int, DNA] = {dna.id_: dna for dna in data}

    @classmethod
    def parse(cls, file: str) -> "Solution":
        """Parse the given input file and return an instance of `Solution` with the loaded data.

        Args:
            file (str): Input file to parse.

        Returns:
            Solution: Class instance with loaded data.
        """
        data: list[DNA] = []

        with open(file, "r") as f:
            for line in f.readlines():
                parts: list[str] = line.strip().split(":")
                data.append(DNA(id_=int(parts[0]), dna=parts[1]))

        return cls(data=data)

    def determine_parent_children_relationships(
        self,
    ) -> dict[tuple[int, int], set[int]]:
        """Determine all the possible parent-children relationships.

        Returns:
            dict[tuple[int, int], set[int]]: The parent pairs and all their children.
        """
        res: dict[tuple[int, int], set[int]] = defaultdict(set)

        for child in self.data.values():
            for parent1, parent2 in combinations(self.data.values(), 2):
                if parent1 == child or parent2 == child:
                    continue

                if child.determine_if_potential_parents(
                    parent1=parent1, parent2=parent2
                ):
                    res[(parent1.id_, parent2.id_)].add(child.id_)

        return res

    def determine_parent_child_similarity_scores(self) -> int:
        """Determine the total similarity score for the parent-children groups.

        Returns:
            int: Total calculated similarity score.
        """
        relationships: dict[tuple[int, int], set[int]] = (
            self.determine_parent_children_relationships()
        )

        tlt: int = 0
        for (parent1_id, parent2_id), children in relationships.items():
            for child_id in children:
                tlt += self.data[parent1_id].similarity(
                    other=self.data[child_id]
                ) * self.data[parent2_id].similarity(other=self.data[child_id])

        return tlt

    def part01_naive(self) -> None:
        """Solve Part 01."""

        # this isn't the best approach, but works for the question.
        # an issue could be if the similarity of the child to both parents are the same.
        # this approach ignores that
        similarity_scores: set[int] = {
            gene1.similarity(other=gene2)
            for gene1, gene2 in combinations(self.data.values(), 2)
        }

        tlt: int = prod(sorted(similarity_scores, reverse=True)[:2])
        print(f"Part 01: {tlt}")

    def part01(self) -> None:
        """Solve Part 01."""
        tlt: int = self.determine_parent_child_similarity_scores()

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solve Part 02. correct 313670"""
        tlt: int = self.determine_parent_child_similarity_scores()

        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solve Part 03."""
        relationships: dict[tuple[int, int], set[int]] = (
            self.determine_parent_children_relationships()
        )

        dsu: UnionFind = UnionFind()

        for (parent1_id, parent2_id), children in relationships.items():
            dsu.union(x=parent1_id, y=parent2_id)

            for child_id in children:
                dsu.union(x=parent1_id, y=child_id)

        # group ducks
        families: dict[int, set[int]] = defaultdict(set)
        for duck_id in self.data.keys():
            families[dsu.find(x=duck_id)].add(duck_id)

        tlt: int = sum(max(families.values(), key=len))
        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/09/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2025/09/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2025/09/input_p03.txt")
    sol3.part03()
