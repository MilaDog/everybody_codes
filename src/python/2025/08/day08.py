import math
from dataclasses import dataclass
from itertools import pairwise


@dataclass
class Point:
    """Representation of a Point in 2D space."""

    id_: int
    x: float
    y: float

    def __repr__(self):
        return f"Point[id_={self.id_}, x={self.x}, y={self.y}]"

    def as_tuple(self) -> tuple[float, float]:
        """Get coordinates as a tuple."""
        return self.x, self.y


@dataclass
class Line:
    """Representation of a line."""

    def __init__(self, point1: Point, point2: Point):
        self.id_: str = f"{point1.id_}-{point2.id_}"
        self.point1: Point = point1
        self.point2: Point = point2

    def __repr__(self):
        return f"Line[point1={self.point1}, point2={self.point2}]"

    def as_tuple(self) -> tuple[tuple[float, float], tuple[float, float]]:
        """Get coordinates as a tuple."""
        return self.point1.as_tuple(), self.point2.as_tuple()

    def intersects(self, target: "Line") -> bool:
        """Determine if the line intersects with the target line.

        Args:
            target (Line): Line to check for an intersection with.

        Returns:
            bool: If there is an intersection or not.
        """
        # Check if segments share an endpoint - these don't count as intersections
        if (
            self.point1.id_ == target.point1.id_
            or self.point1.id_ == target.point2.id_
            or self.point2.id_ == target.point1.id_
            or self.point2.id_ == target.point2.id_
        ):
            return False

        a, b, c, d = self.point1, self.point2, target.point1, target.point2

        def ccw(A, B, C) -> bool:
            return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

        return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)

    # def intersects(self, target: "Line") -> bool:
    #     """Determine if the line intersects with the target line.
    #
    #     Args:
    #         target (Line): Line to check for an intersection with.
    #
    #     Returns:
    #         bool: If there is an intersection or not.
    #     """
    #     # Check if segments share an endpoint - these don't count as intersections
    #     if (
    #             self.point1.id_ == target.point1.id_
    #             or self.point1.id_ == target.point2.id_
    #             or self.point2.id_ == target.point1.id_
    #             or self.point2.id_ == target.point2.id_
    #     ):
    #         return False
    #
    #     x_diffs: tuple[float, float] = (
    #         self.point1.x - self.point2.x,
    #         target.point1.x - target.point2.x,
    #     )
    #     y_diffs: tuple[float, float] = (
    #         self.point1.y - self.point2.y,
    #         target.point1.y - target.point2.y,
    #     )
    #
    #     def determinant(a: tuple[float, float], b: tuple[float, float]) -> float:
    #         return a[0] * b[1] - a[1] * b[0]
    #
    #     div_by: float = determinant(x_diffs, y_diffs)
    #
    #     if div_by == 0:
    #         return False
    #
    #     d = (determinant(*self.as_tuple()), determinant(*target.as_tuple()))
    #
    #     t = determinant(d, x_diffs) / div_by
    #     u = determinant(d, y_diffs) / div_by
    #
    #     return 0 <= t <= 1 and 0 <= u <= 1


class Circle:
    """Representation of a line in the circle."""

    def __init__(self):
        self.plotted_points: list[Point] = []
        self.constructed_chords: list[Line] = []

    def plot_points(self, number_points: int) -> None:
        """Given the number of points, plot them around the center (0, 0), being equally spaced apart.

        Args:
            number_points (int): Number of points to plot.
        """
        angle_step: float = 2 * math.pi / number_points

        for i in range(number_points):
            angle: float = i * angle_step

            target_x: float = math.cos(angle)
            target_y: float = math.sin(angle)

            self.plotted_points.append(Point(id_=i + 1, x=target_x, y=target_y))

    def construct_chords(self, points: list[int]) -> None:
        """With the given points, construct the pairwise chords of the points within the circle.

        Args:
            points (list[int]): Points to join together.
        """
        if not self.plotted_points:
            raise ValueError("No points have been plotted within the circle yet.")

        self.constructed_chords = [
            Line(point1=self.plotted_points[a - 1], point2=self.plotted_points[b - 1])
            for a, b in pairwise(points)
        ]


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
            data = list(map(int, f.read().strip().split(",")))

        return cls(data=data)

    def part01(self) -> None:
        """Solve Part 01."""
        tlt: int = sum(
            abs(a - b) == max(self.data) // 2 for a, b in pairwise(self.data)
        )

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solve Part 02."""
        circle: Circle = Circle()
        circle.plot_points(number_points=max(self.data))
        circle.construct_chords(points=self.data)

        plotted_lines: list[Line] = []

        tlt: int = 0

        for i, line in enumerate(circle.constructed_chords):
            for plotted_line in plotted_lines:
                if line.intersects(target=plotted_line):
                    tlt += 1
            plotted_lines.append(line)

        print(f"\nPart 02: {tlt}")

    def part03(self) -> None:
        """Solve Part 03."""
        circle: Circle = Circle()
        circle.plot_points(number_points=max(self.data))
        circle.construct_chords(points=self.data)

        tlt: int = 0

        p = sorted(circle.plotted_points, key=lambda x: x.id_)
        line: Line = Line(point1=Point(0, 0, 0), point2=Point(0, 0, 0))
        for p1 in range(max(self.data)):
            for p2 in range(1, max(self.data)):
                line.point1 = p[p1]
                line.point2 = p[p2]
                val: int = sum(
                    line.intersects(target=plotted_line)
                    for plotted_line in circle.constructed_chords
                )
                tlt = max(val, tlt)

        print(f"\nPart 03: {tlt}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/08/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2025/08/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2025/08/input_p03.txt")
    sol3.part03()
