from typing import List, Dict


def part_01() -> None:
    """Code for solving Part 1"""

    values: List[str]
    with open("p1.txt") as file:
        values = list(file.read().strip())

    tlt: int = 0
    map: Dict[str, int] = {"a": 0, "b": 1, "c": 3}

    for val in values:
        tlt += map[val.lower()]

    print(f"Part 01: {tlt}")


def part_02() -> None:
    """Code for solving Part 2"""

    values: List[str] = []
    with open("p2.txt") as file:
        line: str = file.read().strip().lower()

        for i in range(0, len(line), 2):
            values.append(line[i : i + 2])

        tlt: int = 0
        map: Dict[str, int] = {"a": 0, "b": 1, "c": 3, "d": 5}

        for val in values:
            if "x" in val:
                if x := val.replace("x", ""):
                    tlt += map[x]

            else:
                tlt += map[val[0]] + map[val[1]] + 2

        print(f"Part 02: {tlt}")


def part_03() -> None:
    """Code for solving Part 3"""

    values: List[str] = []
    with open("p3.txt") as file:
        line: str = file.read().strip().lower()

        for i in range(0, len(line), 3):
            values.append(line[i : i + 3])

        tlt: int = 0
        map: Dict[str, int] = {"a": 0, "b": 1, "c": 3, "d": 5}

        for val in values:
            t: str = val.replace("x", "")

            match len(t):
                case 3:
                    tlt += map[t[0]] + map[t[1]] + map[t[2]] + 6

                case 2:
                    tlt += map[t[0]] + map[t[1]] + 2

                case 1:
                    tlt += map[t]

        print(f"Part 03: {tlt}")


def main() -> None:
    """Entry point"""

    part_01()
    part_02()
    part_03()


if __name__ == "__main__":
    main()
