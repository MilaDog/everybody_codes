from collections import defaultdict
from timeit import timeit
from typing import DefaultDict, List, Tuple, Dict

from utils.timing import Timing


def part_01() -> None:
    """Solution to Part 1"""
    ESSENCE_ACTIONS: Dict[str, int] = {"+": 1, "-": -1, "=": 0}

    devices: DefaultDict[str, List[str]] = defaultdict(list)
    with open("p1.txt") as file:
        for line in file.readlines():
            device, actions = line.strip().split(":")
            devices[device] += actions.split(",")

    results: List[Tuple[str, int]] = []
    for device, actions in devices.items():
        tlt: int = 0
        val: int = 10
        size: int = len(actions)

        for i in range(10):
            val += ESSENCE_ACTIONS[actions[i % size]]
            tlt += val

        results.append((device, tlt))

    results.sort(key=lambda x: x[1], reverse=True)

    res: str = "".join(x[0] for x in results)
    print(f"Part 01: {res}")


def part_02() -> None:
    """Solution to Part 2"""
    RACE_TRACK_ACTIONS: List[str] = []
    with open("p22.txt") as file:
        lines: List[List[str]] = [list(x.strip()) for x in file.readlines()]

        n: List[str] = lines[0][1:-1]
        s: List[str] = lines[-1][1:-1][::-1]

        lines[:] = list(zip(*lines))

        e: List[str] = list(lines[-1])
        w: List[str] = list(lines[0])[::-1]

        RACE_TRACK_ACTIONS += n + e + s + w

    # RACE_LENGTH = len(RACE_TRACK_ACTIONS)

    ESSENCE_ACTIONS: Dict[str, int] = {"+": 1, "-": -1, "=": 0, "S": 0}

    devices: DefaultDict[str, List[str]] = defaultdict(list)
    with open("p2.txt") as file:
        for line in file.readlines():
            device, actions = line.strip().split(":")
            devices[device] += actions.split(",")

    results: List[Tuple[str, int]] = []
    for device, actions in devices.items():
        tlt: int = 0
        val: int = 10
        size: int = len(actions)

        for _ in range(10):
            for i, race_action in enumerate(RACE_TRACK_ACTIONS):
                device_action: str = actions[i % size]

                val += ESSENCE_ACTIONS[
                    device_action if race_action not in "-+" else race_action
                ]
                tlt += val

        results.append((device, tlt))

    results.sort(key=lambda x: x[1], reverse=True)
    print(results)
    res: str = "".join(x[0] for x in results)
    print(f"Part 02: {res}")

    # {336985: 'K', 340621: 'C', 324729: 'B', 325088: 'H', 337549: 'A', 309265: 'I', 350640: 'F', 320573: 'J', 336405: 'E'}
    # FCAKEHBJI


def part_03() -> None:
    """Solution to Part 3"""
    # with open("p3.txt") as file:
    #     pass

    tlt: int = 0
    print(f"Part 03: {tlt}")


def main() -> None:
    """Entry point"""

    print(Timing(timeit(part_01, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_02, number=1)).microseconds, "μs\n")
    # print(Timing(timeit(part_03, number=1)).microseconds, "μs\n")


if __name__ == "__main__":
    main()
