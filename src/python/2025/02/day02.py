import itertools
import re
from dataclasses import dataclass


@dataclass
class ComplexNumber:
    """Representation of a complex number."""

    __slots__ = ("x", "y")
    x: int
    y: int

    def __iadd__(self, other: "ComplexNumber") -> "ComplexNumber":
        """Add two complex numbers."""
        x: int = self.x + other.x
        y: int = self.y + other.y

        self.x = x
        self.y = y
        return self

    def __imul__(self, other: "ComplexNumber") -> "ComplexNumber":
        """Multiply two complex numbers."""
        x: int = (self.x * other.x) - (self.y * other.y)
        y: int = (self.x * other.y) + (self.y * other.x)

        self.x = x
        self.y = y
        return self

    def __itruediv__(self, other: "ComplexNumber") -> "ComplexNumber":
        """True divide two complex numbers."""
        return self.__ifloordiv__(other)

    def __ifloordiv__(self, other: "ComplexNumber") -> "ComplexNumber":
        """Floor divide two complex numbers."""
        x: int = self._negative_divide(a=self.x, b=other.x)
        y: int = self._negative_divide(a=self.y, b=other.y)

        self.x = x
        self.y = y
        return self

    def __str__(self) -> str:
        """String representation of the complex number."""
        return f"[{self.x},{self.y}]"

    def __repr__(self) -> str:
        """String representation of the complex number."""
        return self.__str__()

    @staticmethod
    def _negative_divide(a: int, b: int) -> int:
        if a > 0:
            return a // b
        return (a + b - 1) // b

    def set(self, x: int, y: int) -> None:
        """Set the values of the complex number."""
        self.x, self.y = x, y


class Solution:
    """Solution to the problem."""

    def __init__(self, data: ComplexNumber):
        self.data: ComplexNumber = data

    @classmethod
    def parse(cls, file: str) -> "Solution":
        """Parse the given input file and return an instance of `Solution` with the loaded data.

        Args:
            file (str): Input file to parse.

        Returns:
            Solution: Class instance with loaded data.
        """
        data: ComplexNumber

        with open(file, "r") as f:
            match = re.match(r"A=\[([-0-9]+),([-0-9]+)]", f.read().strip())

            if not match:
                raise ValueError(
                    "Invalid input file. Expected structure: A=[number, number]"
                )

            data = ComplexNumber(x=int(match.group(1)), y=int(match.group(2)))

        return cls(data=data)

    def _is_invalid_point(self, complex_number: ComplexNumber) -> bool:
        """Whether the provided point is valid or not.

        Args:
            complex_number (ComplexNumber): Point to check.

        Returns:
            bool: Valid point or not.
        """
        return abs(complex_number.x) > 1000000 or abs(complex_number.y) > 1000000

    def _count_valid_points(self, x: int, y: int, step_count: int = 1) -> int:
        """Determine the numbr of valid points given a grid size of `x` by `y`.

        Args:
            x (int): Width of the grid.
            y (int): Height of the grid.
            step_count (int): Step count between points.

        Returns:
            int: Total number of valid points in the grid.
        """
        divide_amount: ComplexNumber = ComplexNumber(x=100000, y=100000)
        complex_number: ComplexNumber = ComplexNumber(x=0, y=0)
        target_point: ComplexNumber = ComplexNumber(x=0, y=0)

        tlt: int = 0
        for dx, dy in itertools.product(range(x), range(y)):
            complex_number.set(x=0, y=0)
            target_point.set(
                x=self.data.x + step_count * dx, y=self.data.y + step_count * dy
            )

            valid: bool = True
            for _ in range(100):
                complex_number *= complex_number
                complex_number /= divide_amount
                complex_number += target_point

                if self._is_invalid_point(complex_number=complex_number):
                    valid = False
                    break

            tlt += valid

        return tlt

    def part01(self) -> None:
        """Solve Part 01."""
        complex_number: ComplexNumber = ComplexNumber(x=0, y=0)
        divide_amount: ComplexNumber = ComplexNumber(x=10, y=10)

        for _ in range(3):
            complex_number *= complex_number
            complex_number /= divide_amount
            complex_number += self.data

        print(f"Part 01: {complex_number}")

    def part02(self) -> None:
        """Solve Part 02."""
        print(f"Part 02: {self._count_valid_points(x=101, y=101, step_count=10)}")

    def part03(self) -> None:
        """Solve Part 03."""
        print(f"Part 03: {self._count_valid_points(x=1001, y=1001)}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/02/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2025/02/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2025/02/input_p03.txt")
    sol3.part03()
