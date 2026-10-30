import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Self


@dataclass
class Quest:
    """Representation of a given quest."""

    id: int
    quest: int
    part: int
    time: int

    @classmethod
    def parse(cls, entry: str) -> Self:
        """Parse a given quest entry into a class."""
        values: list[int] = list(map(int, re.findall(r"\d+", entry)))
        return cls(*values)


class Solution:
    """Solution to the problem."""

    def __init__(self, data: list[Quest]):
        self.data: list[Quest] = data

    @classmethod
    def parse(cls, file: str) -> "Solution":
        """Parse the given input file and return an instance of `Solution` with the loaded data.

        Args:
            file (str): Input file to parse.

        Returns:
            Solution: Class instance with loaded data.
        """
        data: list[Quest] = []

        with open(file, "r") as f:
            for entry in f.readlines():
                data.append(Quest.parse(entry))

        return cls(data=data)

    def part01(self) -> None:
        """Solve Part 01."""
        cnter: dict[int, int] = defaultdict(int)

        for entry in self.data:
            cnter[entry.id] += entry.time

        tlt: int = sum(
            item[1] * i
            for i, item in enumerate(sorted(cnter.items(), key=lambda x: x[1]), start=1)
        )

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solve Part 02."""
        cnter: dict[int, tuple[int, int]] = {}

        for entry in self.data:
            if entry.id in cnter:
                tlt_time, num_quests = cnter[entry.id]
                cnter[entry.id] = (tlt_time + entry.time, num_quests + 1)

            else:
                cnter[entry.id] = (entry.time, 1)

        tlt: int = sum(
            item[1][0] * i
            for i, item in enumerate(
                sorted(cnter.items(), key=lambda x: (-x[1][1], x[1][0])), start=1
            )
        )

        print(f"Part 02: {tlt}")

    def group_entries_by_quest(self, entries: list[Quest]) -> dict[int, list[Quest]]:
        """Group the entries by their quest number."""
        grouped_quests = defaultdict(list)

        for entry in entries:
            grouped_quests[entry.quest].append(entry)

        return grouped_quests

    def group_entries_by_part(self, entries: list[Quest]) -> dict[int, list[Quest]]:
        """Group the entries by their part number."""
        grouped_quests = defaultdict(list)

        for entry in entries:
            grouped_quests[entry.part].append(entry)

        return grouped_quests

    def determine_rankings(
        self, entries: list[Quest], points_amount: int, history_times: dict[int, int]
    ) -> list[tuple[int, Quest]]:
        """Determine the rankings of the entries, assigning points to their finishing positions, ordering the entries by their current time and history of times. Tied placed get the same score."""
        rankings = []

        points: int = points_amount
        prev_tie_time: int = -1
        tie_streak: int = 0
        for entry in sorted(entries, key=lambda x: x.time + history_times.get(x.id, 0)):
            # if it is a tie, same points
            if entry.time + history_times.get(entry.id, 0) == prev_tie_time:
                rankings.append((max(points, 0), entry))
                tie_streak += 1
                continue

            # not time, update prev_tie_time and reset tie streak
            points -= 1 * tie_streak
            tie_streak = 1
            rankings.append((max(points, 0), entry))
            prev_tie_time = entry.time + history_times.get(entry.id, 0)

        return rankings

    def part03(self) -> None:
        """Solve Part 03."""

        overall_rankings: dict[int, int] = defaultdict(int)

        # group by quests
        for quest_num, e1 in sorted(
            self.group_entries_by_quest(self.data).items(), key=lambda x: x[0]
        ):
            history_times: dict[int, int] = defaultdict(int)

            # group by parts
            for part_num, e2 in sorted(
                self.group_entries_by_part(e1).items(), key=lambda x: x[0]
            ):
                # storing ranking scores
                points_amount: int = (50, 100, 150)[part_num - 1]
                for points, entry in self.determine_rankings(
                    e2, points_amount, history_times
                ):
                    overall_rankings[entry.id] += points
                    history_times[entry.id] += entry.time

        tlt: int = 0
        indx: int = 1
        prev_score: int = -1
        tie_streak: int = 0
        for _, score in sorted(overall_rankings.items(), key=lambda x: -x[1]):
            if score == prev_score:
                tlt += score * indx
                tie_streak += 1
                continue

            indx += 1 * tie_streak
            tie_streak = 1
            tlt += score * indx
            prev_score = score

        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2026/04/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2026/04/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2026/04/input_p03.txt")
    sol3.part03()
