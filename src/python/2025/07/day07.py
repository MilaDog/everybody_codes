from collections import deque


class Solution:
    """Solution to the problem."""

    def __init__(self, names: list[str], rules: dict[str, list[str]]):
        self.names: list[str] = names
        self.rules: dict[str, list[str]] = rules

    @classmethod
    def parse(cls, file: str) -> "Solution":
        """Parse the given input file and return an instance of `Solution` with the loaded data.

        Args:
            file (str): Input file to parse.

        Returns:
            Solution: Class instance with loaded data.
        """
        names: list[str] = []
        rules: dict[str, list[str]] = dict()

        with open(file, "r") as f:
            raw_names, raw_rules = f.read().split("\n\n")

            names = list(raw_names.split(","))

            for raw_rule in raw_rules.split("\n"):
                target, allowed = raw_rule.strip().split(" > ")
                rules[target] = list(allowed.strip().split(","))

        return cls(names=names, rules=rules)

    def is_valid_prefix(self, prefix: str) -> bool:
        """Determine if the given prefix is valid according to the rules.

        Args:
            prefix (str): Prefix to validate.

        Returns:
            bool: Valid prefix or not.
        """
        for a, b in zip(prefix, prefix[1:]):
            if a not in self.rules or b not in self.rules[a]:
                return False
        return True

    def determine_potential_names_with_prefix(
        self, prefix: str, min_length: int, max_length: int
    ) -> set[str]:
        """Determine all the potential names that can be formed with the given `prefix` and within the target length.

        Args:
            prefix (str): Prefix of the name.
            min_length (int): Minimum length of the name.
            max_length (int): Maximum length of the name.

        Returns:
            set[str]: All potential names found.
        """
        res: set[str] = set()

        if not self.is_valid_prefix(prefix=prefix):
            return res

        q: deque[tuple[str, str]] = deque([(prefix[-1], prefix)])

        while q:
            curr_ltr, curr_name = q.popleft()

            if min_length <= len(curr_name) <= max_length:
                res.add(curr_name)

            if len(curr_name) >= max_length:
                continue

            if curr_ltr not in self.rules:
                continue

            for next_ltr in self.rules[curr_ltr]:
                q.append((next_ltr, curr_name + next_ltr))

        return res

    def part01(self) -> None:
        """Solve Part 01."""
        determined_name: str = "-"
        for name in self.names:
            if self.is_valid_prefix(prefix=name):
                determined_name = name
        print(f"Part 01: {determined_name}")

    def part02(self) -> None:
        """Solve Part 02."""
        tlt: int = sum(
            i
            for i, name in enumerate(self.names, 1)
            if self.is_valid_prefix(prefix=name)
        )
        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solve Part 03."""
        all_names: set[str] = set()
        for name in self.names:
            all_names.update(
                self.determine_potential_names_with_prefix(
                    prefix=name, min_length=7, max_length=11
                )
            )

        print(f"Part 03: {len(all_names)}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/07/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2025/07/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2025/07/input_p03.txt")
    sol3.part03()
