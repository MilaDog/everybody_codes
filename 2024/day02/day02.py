import re
from typing import List, Set

import regex


def part_01() -> None:
    """Solution to Part 1"""
    runic_words: Set[str]
    sentence: str

    with open("p1.txt") as file:
        lines: List[str] = [x.strip() for x in file.readlines()]

        runic_words = set(lines[0].replace("WORDS:", "").split(","))
        sentence = lines[-1]

    tlt: int = 0
    for wrd in runic_words:
        tlt += len(re.findall(wrd, sentence))

    print(f"Part 01: {tlt}")


def part_02() -> None:
    """Solution to Part 2"""
    runic_words: Set[str]
    sentences: List[str]

    with open("p2.txt") as file:
        lines: list[str] = [x.strip() for x in file.readlines()]

        words = lines[0].replace("WORDS:", "").split(",")
        words += [x[::-1] for x in words]
        runic_words = set(words)
        sentences = lines[2:]

    tlt: int = 0
    for sentence in sentences:
        t = [0] * len(sentence)

        for wrd in runic_words:
            for m in regex.finditer(wrd, sentence, overlapped=True):
                s, e = m.span()
                for i in range(s, e):
                    t[i] = 1

        tlt += sum(t)

    print(f"Part 02: {tlt}")


def part_03() -> None:
    """Solution to Part 3"""
    runic_words: List[str]
    grid: List[str]

    with open("p3.txt") as file:
        lines: List[str] = [x.strip() for x in file.readlines()]

        runic_words = lines[0].replace("WORDS:", "").split(",")
        runic_words += [x[::-1] for x in runic_words]
        grid = lines[2:]

    # Scanning rows
    seen_rows: List[List[int]] = []
    for row in [x * 2 for x in grid]:
        t: List[int] = [0] * (len(row) // 2)
        for wrd in runic_words:
            for m in regex.finditer(wrd, row, overlapped=True):
                s, e = m.span()
                for i in range(s, e):
                    if i >= len(row) // 2:
                        t[i - len(row)] = 1
                        continue

                    t[i] = 1

        seen_rows.append(t)

    # Scanning cols
    seen_cols: List[List[int]] = []
    for col in ["".join(x) for x in zip(*grid)]:
        t: List[int] = [0] * (len(col))
        for wrd in runic_words:
            for m in regex.finditer(wrd, col, overlapped=True):
                s, e = m.span()
                for i in range(s, e):
                    t[i] = 1

        seen_cols.append(t)

    # Counting
    for i, v in enumerate([x for x in zip(*seen_cols)]):
        for j in range(len(v)):
            if v[j] == 1:
                seen_rows[i][j] = 1

    tlt: int = sum(sum(x) for x in seen_rows)
    print(f"Part 03: {tlt}")


def main() -> None:
    """Entry point"""

    part_01()
    part_02()
    part_03()


if __name__ == "__main__":
    main()
