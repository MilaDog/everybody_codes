from collections import defaultdict, deque


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
                alloys: list[str] = line.strip().split()
                data.append(alloys)

        return cls(data=data)

    @classmethod
    def normalise_comparison(cls, comparison: str) -> tuple[int, int]:
        """Normalise the given alloy comparison string into a tuple (winner, loser)."""
        a, cmp, b = list(comparison.strip())

        if cmp == ">":
            return int(a), int(b)
        return int(b), int(a)

    @classmethod
    def determine_checksum(cls, cnter: dict[int, int]) -> str:
        """Determine the checksum - hardest to weakest alloys."""
        return "".join(
            [str(x) for x, y in sorted(cnter.items(), reverse=True, key=lambda x: x[1])]
        )

    def kahns_algorithm(self, alloys) -> int:
        """Solve the problem using Kahn's Algorithm- Topological sorting using BFS."""
        adjacents = defaultdict(set)
        nodes = set()
        indegrees = defaultdict(int)

        for alloy in alloys:
            winner, loser = Solution.normalise_comparison(alloy)

            nodes |= {winner, loser}
            if loser not in adjacents[winner]:
                adjacents[winner].add(loser)
                indegrees[loser] += 1

        q = deque(n for n in nodes if indegrees[n] == 0)
        order = []

        while q:
            n = q.popleft()
            order.append(n)

            for m in adjacents[n]:
                indegrees[m] -= 1
                if indegrees[m] == 0:
                    q.append(m)

        return int("".join(map(str, order)))

    def part01_original(self) -> None:
        """Solve Part 01."""
        tlt: int = 0

        for alloys in self.data:
            cnts: dict[int, int] = defaultdict(int)

            # Count winners
            for alloy in alloys:
                winner, loser = Solution.normalise_comparison(alloy)
                cnts[winner] += 1
                cnts[loser] += 0

            # Determine group checksum
            tlt += int(Solution.determine_checksum(cnts))

        print(f"Part 01: {tlt}")

    def part02_original(self) -> None:
        """Solve Part 02."""
        tlt: int = 0

        for alloys in self.data:
            cnts: dict[int, int] = defaultdict(int)

            # Count winners
            for alloy in alloys:
                winner, loser = Solution.normalise_comparison(alloy)
                cnts[winner] += 1
                cnts[loser] += -1

            tlt += int(Solution.determine_checksum(cnts))

        print(f"Part 02: {tlt}")

    def solve(self, part: str) -> None:
        """Solve all Parts."""
        # Kahn's Algorithm
        tlt: int = sum(self.kahns_algorithm(alloys=alloys) for alloys in self.data)
        print(f"Part {part}: {tlt}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2026/02/input_p01.txt")
    sol1.solve(part="01")

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2026/02/input_p02.txt")
    sol2.solve(part="02")

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2026/02/input_p03.txt")
    sol3.solve(part="03")
