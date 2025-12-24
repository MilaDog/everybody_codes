class DuckFormation:
    """Representation of the Duck Formation for the problem."""

    def __init__(self, initial_columns: list[int]):
        self.data: list[int] = initial_columns

    def _perform_phase_one(
        self, previous_formation: list[int]
    ) -> tuple[bool, list[int]]:
        """Perform the first phase of movements.

        Args:
            previous_formation (list[int]): Previous flock formation.

        Returns:
            tuple[bool, list[int]]: New formation if a change was made, else the previous formation.
        """
        new_formation: list[int] = previous_formation[::]

        moved: bool = False
        for i in range(len(new_formation) - 1):
            if new_formation[i + 1] < new_formation[i]:
                moved = True
                new_formation[i] -= 1
                new_formation[i + 1] += 1

        if moved:
            return True, new_formation

        return False, previous_formation

    def _perform_phase_two(
        self, previous_formation: list[int]
    ) -> tuple[bool, list[int]]:
        """Perform the second phase of movements.

        Args:
            previous_formation (list[int]): Previous flock formation.

        Returns:
            tuple[bool, list[int]]: New formation if a change was made, else the previous formation.
        """
        new_formation: list[int] = previous_formation[::]

        moved: bool = False
        for i in range(len(new_formation) - 1):
            if new_formation[i + 1] > new_formation[i]:
                moved = True
                new_formation[i] += 1
                new_formation[i + 1] -= 1

        if moved:
            return True, new_formation

        return False, previous_formation

    def perform_phases(self, check_end) -> tuple[int, list[int]]:
        """Perform the movement phases of the Ducks."""
        current_formation: list[int] = self.data[::]
        phase_id: int = 0

        # First Phase
        while True:
            phase_id += 1
            updated, new_formation = self._perform_phase_one(
                previous_formation=current_formation
            )

            if not updated:
                break
            current_formation = new_formation

            if check_end(phase_id, current_formation):
                return phase_id, current_formation

        # Second Phase
        while True:
            phase_id += 1
            updated, new_formation = self._perform_phase_two(
                previous_formation=current_formation
            )

            if not updated:
                break
            current_formation = new_formation

            if check_end(phase_id, current_formation):
                return phase_id, current_formation

        return phase_id, current_formation

    def calculate_flock_checksum(self, formation: list[int]) -> int:
        """Calculate the checksum of the given flock formation.

        Args:
            formation (list[int]): Target flock formation.

        Returns:
            int: Calculated checksum of the target flock formation.
        """
        return sum(i * v for i, v in enumerate(formation, 1))


class Solution:
    """Solution to the problem."""

    def __init__(self, data: list[int]):
        self.data: list[int] = data
        self.flock: DuckFormation = DuckFormation(initial_columns=data)

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
            data = list(map(int, f.readlines()))

        return cls(data=data)

    def check_end_by_phase(
        self, phase_id: int | None = None, formation: list[int] | None = None
    ) -> bool:
        return phase_id == 11

    def check_end_by_balanced_formation(
        self, phase_id: int, formation: list[int]
    ) -> bool:
        return len(set(formation)) == 1

    def part01(self) -> None:
        """Solve Part 01."""
        _, formation = self.flock.perform_phases(check_end=self.check_end_by_phase)
        tlt: int = self.flock.calculate_flock_checksum(formation=formation)

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solve Part 02."""
        phase_id, _ = self.flock.perform_phases(
            check_end=self.check_end_by_balanced_formation
        )

        print(f"Part 02: {phase_id - 1}")

    def part03(self) -> None:
        """Solve Part 03.


        A neat trick can be used for this part. See reddit post for insight:
        https://www.reddit.com/r/everybodycodes/comments/1ozvbnq/2025_q11_solution_spotlight/"""
        mean: float = sum(self.data) / len(self.data)
        tlt: float = sum((mean - x if x < mean else 0) for x in self.data)

        print(f"Part 03: {int(tlt)}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/11/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2025/11/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2025/11/input_p03.txt")
    sol3.part03()
