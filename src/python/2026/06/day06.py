from collections import defaultdict, deque


class Solution:
    """Solution to the problem."""

    def __init__(self, data: dict[str, list[str]]):
        self.data: dict[str, list[str]] = data

    @classmethod
    def parse(cls, file: str) -> "Solution":
        """Parse the given input file and return an instance of `Solution` with the loaded data.

        Args:
            file (str): Input file to parse.

        Returns:
            Solution: Class instance with loaded data.
        """
        data: dict[str, list[str]] = defaultdict(list)

        with open(file, "r") as f:
            for line in f.readlines():
                a, bs = line.strip().split(":")
                data[a] += bs.split(",")

        return cls(data=data)

    def get_products(
        self, all_products: dict[str, list[str]], start: str = "NULL"
    ) -> set[str]:
        """With the given `start` product, get all other products needed for it.

        Args:
            all_products (dict[str, list[str]]): Map of all products and their ingredients.
            start (str): Starting position within the map.

        Returns:
            set[str]: All products/ingredients used for `start`.
        """
        q = deque([start])
        seen: set[str] = set()

        while q:
            curr = q.popleft()

            if curr in seen:
                continue
            seen.add(curr)

            for p in all_products.get(curr, []):
                q.append(p)

        return seen

    def part01(self) -> None:
        """Solve Part 01."""

        print(f"Part 01: {len(self.get_products(self.data)) - 1}")

    def part02(self) -> None:
        """Solve Part 02."""
        reversed_data: dict[str, list[str]] = defaultdict(list)

        for k, v in self.data.items():
            for p in v:
                reversed_data[p].append(k)

        print(f"Part 02: {len(self.get_products(reversed_data)) - 1}")

    def part03(self) -> None:
        """Solve Part 03."""
        tlt: int = 0
        for k in self.data.keys():
            tlt += (
                sum(
                    x in ("NULLv1", "NULLv2", "NULLv3")
                    for x in self.get_products(all_products=self.data, start=k)
                )
                >= 2
            )

        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2026/06/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2026/06/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2026/06/input_p03.txt")
    sol3.part03()
