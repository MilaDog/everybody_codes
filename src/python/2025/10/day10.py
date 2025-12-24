from dataclasses import dataclass
from enum import Enum
from typing import Any


class SheepStateEnum(Enum):
    ALIVE = 1
    EATEN = 2
    HIDDEN = 3
    SAFE = 4


@dataclass
class Sheep:
    """Representation of a sheep in the Dragon Chess game."""

    x: int
    y: int
    status: SheepStateEnum


class DragonBoard:
    """Dragon Chess Board representation of the problem."""

    def __init__(self, board: list[list[str]]):
        self.board: list[list[str]] = board
        self.sheep: list[Sheep] = self._parse_sheep()
        self.dragon: tuple[int, int] = self._determine_dragon_position()
        self.dragon_movements: list[tuple[int, int]] = [
            (-2, -1),
            (-2, 1),
            (2, -1),
            (2, 1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
        ]

        self.height: int = len(self.board)
        self.width: int = len(self.board[0])

        self.memo: dict[Any, int] = {}

    def _determine_dragon_position(self) -> tuple[int, int]:
        """Get the starting position of the dragon in the grid.

        Returns:
            tuple[int, int]: Position of the Dragon in the grid.
        """
        for x, c1 in enumerate(self.board):
            for y, c2 in enumerate(c1):
                if c2.upper() == "D":
                    return x, y

        raise ValueError("No starting Dragon position found on the board.")

    def _parse_sheep(self) -> list[Sheep]:
        """Get a list of all the sheep positions on the board.

        Returns:
            list[Sheep]: All found Sheep on the board.
        """
        res: list[Sheep] = []

        for x, c1 in enumerate(self.board):
            for y, c2 in enumerate(c1):
                if c2.upper() == "S":
                    res.append(Sheep(x=x, y=y, status=SheepStateEnum.ALIVE))

        return res

    def is_valid_move(self, x: int, y: int) -> bool:
        """Determine if the move is valid; the move is within the bounds of the board.

        Args:
            x (int): X position.
            y (int): Y position.

        Returns:
            bool: If the move is within the bounds of the game board.
        """
        return 0 <= x < self.height and 0 <= y < self.width

    def get_potential_dragon_movement_positions(
        self, position: tuple[int, int]
    ) -> set[tuple[int, int]]:
        """Get all the valid positions that the Dragon can move to from the target position.

        Returns:
            set[tuple[int, int]]: Set of all valid moveable positions for the Dragon.
        """
        res: set[tuple[int, int]] = set()

        for dx, dy in self.dragon_movements:
            new_x: int = dx + position[0]
            new_y: int = dy + position[1]

            if self.is_valid_move(x=new_x, y=new_y):
                res.add((new_x, new_y))

        return res

    def count_number_sheep_eaten(self, positions: set[tuple[int, int]]) -> int:
        """Count how many sheep on the board have been eaten by the Dragon. Does not update the Sheep.

        Args:
            positions (set[tuple[int, int]]): Positions the Dragon has moved to.

        Returns:
            int: Positions of the Dragon.
        """
        return sum(self.board[x][y].upper() == "S" for x, y in positions)

    def perform_game_move(
        self, positions: set[tuple[int, int]]
    ) -> set[tuple[int, int]]:
        """Perform a game move. This determines the 1) new positions of the Dragon, then 2) updates the positions and details of the Sheep on the board.

        Args:
            positions (set[tuple[int, int]]): List of the positions of the Dragon to update.

        Returns:
            set[tuple[int, int]]: Set of all new positions that the Dragon can move to.
        """
        res: set[tuple[int, int]] = set()

        # move Dragon
        for position in positions:
            for dx, dy in self.dragon_movements:
                new_x: int = dx + position[0]
                new_y: int = dy + position[1]

                if self.is_valid_move(x=new_x, y=new_y):
                    res.add((new_x, new_y))

        # update Sheep
        for sheep in self.sheep:
            # Cannot process eaten sheep
            if sheep.status == SheepStateEnum.EATEN:
                continue

            if (sheep.x, sheep.y) in res and sheep.status == SheepStateEnum.ALIVE:
                sheep.status = SheepStateEnum.EATEN
                continue

            sheep.x += 1
            sheep.status = SheepStateEnum.ALIVE

            if sheep.x >= self.height:
                sheep.status = SheepStateEnum.SAFE
                continue

            if self.board[sheep.x][sheep.y].upper() == "#":
                sheep.status = SheepStateEnum.HIDDEN
                continue

            if (sheep.x, sheep.y) in res and sheep.status == SheepStateEnum.ALIVE:
                sheep.status = SheepStateEnum.EATEN
                continue

        return res

    def count_eaten_sheep(self) -> int:
        """Count how many of the Sheep have been eaten.

        Returns:
            int: Number of Sheep eaten.
        """
        return sum(sheep.status == SheepStateEnum.EATEN for sheep in self.sheep)

    def determine_moves_to_eat_all_sheep(
        self,
        dragon_position: tuple[int, int],
        sheep: frozenset,
        is_sheep_turn: bool,
        move_sequence: str,
    ) -> int:
        """Determine the number of sequences of moves that can be made in order for the Dragon to eat all Sheep.

        Returns:
            int: Total number of sequences that result in all Sheep eaten.
        """
        if (dragon_position, sheep, is_sheep_turn) in self.memo:
            return self.memo[(dragon_position, sheep, is_sheep_turn)]

        if len(sheep) == 0:
            return 1

        cnt: int = 0
        possible_move: bool = False

        if is_sheep_turn:
            for x, y in sheep:
                new_x: int = x + 1

                if new_x >= self.height:
                    possible_move = True
                    pass

                elif (new_x, y) != dragon_position or self.board[new_x][y] == "#":
                    new_sheep: set[tuple[int, int]] = set(sheep)
                    new_sheep.remove((x, y))
                    new_sheep.add((new_x, y))
                    new_move_sequence: str = (
                        move_sequence + f"S>{chr(ord('A') + y)}{new_x + 1}"
                    )

                    cnt += self.determine_moves_to_eat_all_sheep(
                        dragon_position=dragon_position,
                        sheep=frozenset(new_sheep),
                        is_sheep_turn=False,
                        move_sequence=new_move_sequence,
                    )
                    possible_move = True

            if not possible_move:
                cnt += self.determine_moves_to_eat_all_sheep(
                    dragon_position=dragon_position,
                    sheep=sheep,
                    is_sheep_turn=False,
                    move_sequence=move_sequence,
                )

        else:
            for dx, dy in self.dragon_movements:
                new_x, new_y = dragon_position[0] + dx, dragon_position[1] + dy

                if self.is_valid_move(x=new_x, y=new_y):
                    new_move_sequence: str = (
                        move_sequence + f"D>{chr(ord('A') + new_y)}{new_x + 1}"
                    )

                    if (new_x, new_y) in sheep and self.board[new_x][new_y] != "#":
                        new_sheep: set[tuple[int, int]] = set(sheep)
                        new_sheep.remove((new_x, new_y))
                        cnt += self.determine_moves_to_eat_all_sheep(
                            dragon_position=(new_x, new_y),
                            sheep=frozenset(new_sheep),
                            is_sheep_turn=True,
                            move_sequence=new_move_sequence,
                        )

                    else:
                        cnt += self.determine_moves_to_eat_all_sheep(
                            dragon_position=(new_x, new_y),
                            sheep=sheep,
                            is_sheep_turn=True,
                            move_sequence=new_move_sequence,
                        )

        self.memo[(dragon_position, sheep, is_sheep_turn)] = cnt

        return cnt


class Solution:
    """Solution to the problem."""

    def __init__(self, data: list[list[str]]):
        self.data: list[list[str]] = data
        self.board: DragonBoard = DragonBoard(board=data)

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
            data = [list(line.strip()) for line in f.readlines()]

        return cls(data=data)

    def count_sheep_eaten(self, positions: set[tuple[int, int]]) -> int:
        return sum(self.data[x][y].upper() == "S" for x, y in positions)

    def part01(self) -> None:
        """Solve Part 01."""
        res: set[tuple[int, int]] = {self.board.dragon}

        for _ in range(4):
            new_positions: set[tuple[int, int]] = set()
            for position in res:
                new_positions.update(
                    self.board.get_potential_dragon_movement_positions(
                        position=position
                    )
                )

            res.update(new_positions)

        tlt: int = self.board.count_number_sheep_eaten(positions=res)

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solve Part 02."""

        positions: set[tuple[int, int]] = {self.board.dragon}
        for _ in range(20):
            positions = self.board.perform_game_move(positions=positions)

        tlt: int = self.board.count_eaten_sheep()

        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solve Part 03."""
        sheep: set[tuple[int, int]] = set([(s.x, s.y) for s in self.board.sheep])

        tlt: int = self.board.determine_moves_to_eat_all_sheep(
            dragon_position=self.board.dragon,
            sheep=frozenset(sheep),
            is_sheep_turn=True,
            move_sequence="",
        )

        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol1: Solution = Solution.parse("./inputs/everybody_codes/2025/10/input_p01.txt")
    sol1.part01()

    sol2: Solution = Solution.parse("./inputs/everybody_codes/2025/10/input_p02.txt")
    sol2.part02()

    sol3: Solution = Solution.parse("./inputs/everybody_codes/2025/10/input_p03.txt")
    sol3.part03()
