from timeit import timeit

from src.timing import Timing

import re


def part_01() -> None:
    """Solution to Part 1"""
    with open("q01_p01.in") as file:
        contents: list[list[int]] = [list(map(int, re.findall(r"\d+", line))) for line in file.readlines()]

    def __eni(n: int, exp: int, mod: int) -> int:
        res: list[int] = []
        score: int = 1

        for _ in range(exp):
            score = (score * n) % mod
            res.append(score)

        return int("".join(map(str, res[::-1])))

    all_scores: list[int] = [__eni(a,x,m) + __eni(b,y,m) + __eni(c,z,m) for a,b,c,x,y,z,m in contents]
    tlt: int = max(all_scores)
    print(f"Part 01: {tlt}")

def part_02() -> None:
    """Solution to Part 2"""
    with open("q01_p02.in") as file:
        contents: list[list[int]] = [list(map(int, re.findall(r"\d+", line))) for line in file.readlines()]

    def __eni(n: int, exp: int, mod: int) -> int:
        res: list[int] = []
        score: int = 1

        if exp > 20:
            score = pow(n, exp-20, mod)
            exp = 20

        for _ in range(exp):
            score = (score * n) % mod
            res.append(score)

        return int("".join(map(str, res[-5:][::-1])))

    all_scores: list[int] = [__eni(a,x,m) + __eni(b,y,m) + __eni(c,z,m) for a,b,c,x,y,z,m in contents]
    tlt: int = max(all_scores)
    print(f"Part 02: {tlt}")


def part_03() -> None:
    """Solution to Part 3"""
    with open("q01_p03.in") as file:
        contents: list[list[int]] = [list(map(int, re.findall(r"\d+", line))) for line in file.readlines()]

    def __eni(n: int, exp: int, mod: int) -> int:
        res: int = 0
        score: int = 1

        cnt: int = 0
        SEEN: dict[int, tuple[int, int]] = {} # score: (cnt, res)

        while cnt < exp:
            score = (score * n) % mod
            res += score
            cnt += 1

            # Checking for a cycle
            if score in SEEN:
                # now can jump forward, getting closer to the number of loops that we have to do
                # change in count and sum of scores
                dcnt: int = cnt - SEEN[score][0]
                dres: int = res - SEEN[score][1]

                # the total sum gathered in this cycle
                amt: int = (exp-cnt)//dcnt

                # move forward
                res += dres*amt
                cnt += dcnt*amt

            SEEN[score] = (cnt, res)

        return res

    all_scores: list[int] = [__eni(a,x,m) + __eni(b,y,m) + __eni(c,z,m) for a,b,c,x,y,z,m in contents]
    tlt: int = max(all_scores)
    print(f"Part 03: {tlt}")


def main() -> None:
    """Entry point"""

    print(Timing(timeit(part_01, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_02, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_03, number=1)).microseconds, "μs\n")


if __name__ == "__main__":
    main()
