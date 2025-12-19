from collections import defaultdict, deque, Counter
from timeit import timeit
from typing import List, Dict, Set, Deque, Counter as Counter_

from src.timing import Timing


def parse_input(file_name: str) -> Dict[str, List[str]]:
    """
    Parse the given problem input and return.

    Args:
        file_name (str):
            Name of the input file to parse.

    Returns:
        dict(str, list(str)):
            All the paths of graph from the input file.

    """
    tree: Dict[str, List[str]] = defaultdict()

    with open(f"{file_name}.txt", "r") as file:
        for line in file.readlines():
            k, v = line.strip().split(":")
            tree[k] = v.split(",")

    return tree


def traverse(
    tree: Dict[str, List[str]],
    dq: Deque[str],
    current_path: List[str],
    tree_paths: List[str],
    seen: Set[str],
    truncate: bool = False,
) -> None:
    """
    Depth-First Search to determine all the paths of the tree.

    Args:
        tree (Dict[str, List[str]]):
             Tree to be traversed.
        dq (Deque(str)):
            Stack to be used to keep track of when has to be explored.
        current_path (List[str]):
            Stores the nodes that have been visited in the current traversal.
        tree_paths (List[str]):
            List of all the traversed tree paths.
        seen (Set[str]):
            Set of all visited nodes.
        truncate (bool):
            Whether the node's name should be truncated to just the first character. Default is False.

    Returns:
        None
    """
    if not dq:
        return

    curr = dq.popleft()

    # Look up
    if tree.get(curr):
        r = current_path[:]
        r.append(curr)

        if curr not in seen:
            seen.add(curr)

            for child in tree[curr]:
                if child == "@":
                    if not truncate:
                        tree_paths.append("".join(r) + "@")

                    else:
                        tree_paths.append("".join([x[0] for x in r]) + "@")

                    return

                dq.appendleft(child)
                traverse(
                    tree=tree,
                    dq=dq,
                    current_path=r,
                    tree_paths=tree_paths,
                    seen=seen,
                    truncate=truncate,
                )


def solve(file_name: str) -> str:
    """
    Solve the problems.

    Args:
        file_name (str):
            Name of the text file that has the problem data.

    Returns:
        str:
            Determined answer for the problem.

    """
    tree: Dict[str, List[str]] = parse_input(file_name)
    dq: Deque[str] = deque(["RR"])
    tree_paths: List[str] = []
    current_path: List[str] = []
    seen: Set[str] = set()
    should_truncate: bool = file_name != "p1"

    traverse(
        tree=tree,
        dq=dq,
        current_path=current_path,
        tree_paths=tree_paths,
        seen=seen,
        truncate=should_truncate,
    )
    tree_path_lengths: Counter_[int] = Counter(map(len, tree_paths))
    smallest_length: int = [k for k, v in tree_path_lengths.items() if v == 1][0]
    return [x for x in tree_paths if len(x) == smallest_length][0]


def part_01() -> None:
    """Solution to Part 1"""
    tlt: str = solve("p1")
    print(f"Part 01: {tlt}")


def part_02() -> None:
    """Solution to Part 2"""
    tlt: str = solve("p2")
    print(f"Part 02: {tlt}")


def part_03() -> None:
    """Solution to Part 3"""
    tlt: str = solve("p3")
    print(f"Part 03: {tlt}")


def main() -> None:
    """Entry point"""

    print(Timing(timeit(part_01, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_02, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_03, number=1)).microseconds, "μs\n")


if __name__ == "__main__":
    main()
