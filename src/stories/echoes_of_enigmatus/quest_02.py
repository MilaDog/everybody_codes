from __future__ import annotations

import itertools
from collections import defaultdict, deque
from dataclasses import dataclass
from timeit import timeit

from src.timing import Timing

import re


class Node:
    """Node for the tree."""

    def __init__(self, value: str, rank: int):
        self.value: str = value
        self.rank: int = rank
        self.left: Node | None = None
        self.right: Node | None = None
        self.parent: Node | None = None

    def __repr__(self) -> str:
        """String representation of the node."""
        return f"Node(value={self.value}, rank={self.rank}, left={self.left}, right={self.right})"


class Tree:
    """B-Tree for the Problem"""

    def __init__(self, root: Node | None = None):
        self.root: Node | None = root

    def add_node(self, data: tuple[int, str]) -> None:
        """Add to the tree."""
        if self.root is None:
            self.root = Node(value=data[1], rank=data[0])
            return

        current: Node = self.root

        while True:
            next_node: Node | None = (
                current.left if data[0] < current.rank else current.right
            )

            if next_node is None:
                new_node = Node(value=data[1], rank=data[0])
                new_node.parent = current

                if data[0] < current.rank:
                    current.left = new_node
                else:
                    current.right = new_node

                break

            else:
                current = next_node

    def get_node(self, rank: int, value: str) -> Node | None:
        """Get the Node with the given rank and value."""
        nodes: dict[int, list[Node]] = self.traverse_tree()

        if nodes:
            flattened: list[Node] = list(itertools.chain(*nodes.values()))
            return next(
                (x for x in flattened if (x.rank, x.value) == (rank, value)), None
            )

        return None

    @staticmethod
    def tree_has_node(tree_root: Node, node: Node) -> bool:
        """Whether the given tree contains the given node or not."""
        if not tree_root:
            return False

        if tree_root == node:
            return True

        return Tree.tree_has_node(tree_root.left, node) or Tree.tree_has_node(
            tree_root.right, node
        )

    @staticmethod
    def swap_nodes(node_a: Node, node_b: Node) -> None:
        """Swap to Node's values around."""
        node_a.rank, node_a.value, node_b.rank, node_b.value = (
            node_b.rank,
            node_b.value,
            node_a.rank,
            node_a.value,
        )

    @staticmethod
    def swap_branches(
        tree_left: Tree, tree_right: Tree, node_a: Node, node_b: Node
    ) -> (Tree, Tree):
        """Swap the branches of the Nodes."""
        parent_a: Node | None = node_a.parent
        parent_b: Node | None = node_b.parent
        is_left_child_a: bool = parent_a and parent_a.left == node_a
        is_left_child_b: bool = parent_b and parent_b.left == node_b

        # Getting the trees
        tree_with_node_a: Tree = (
            tree_left if Tree.tree_has_node(tree_left.root, node_a) else tree_right
        )
        tree_with_node_b: Tree = (
            tree_left if Tree.tree_has_node(tree_left.root, node_b) else tree_right
        )

        # Detaching the nodes
        Tree.detach_node(tree_with_node_a, node_a)
        Tree.detach_node(tree_with_node_b, node_b)

        # Attaching the nodes
        Tree.attach_node(tree_with_node_a, node_b, parent_a, is_left_child_a)
        Tree.attach_node(tree_with_node_b, node_a, parent_b, is_left_child_b)

        return tree_left, tree_right

    @staticmethod
    def detach_node(tree: Tree, node: Node) -> Tree:
        """Detach the node from the tree, returning a new tree with the detached node."""
        if node.parent is None:
            if tree.root == node:
                tree.root = None
            return Tree(node)

        else:
            if node.parent.left == node:
                node.parent.left = None

            else:
                node.parent.right = None

            node.parent = None
            return Tree(node)

    @staticmethod
    def attach_node(tree: Tree, node: Node, parent: Node, is_left_child: bool) -> None:
        """Attach the given node to the given tree."""
        if parent is None:
            tree.root = node
            node.parent = None

        else:
            if is_left_child:
                parent.left = node
            else:
                parent.right = node
            node.parent = parent

    def traverse_tree(self) -> dict[int, list[Node]]:
        """BFS on the tree."""
        if self.root is None:
            return {}

        res: dict[int, list[Node]] = defaultdict(list)
        q: deque[tuple[int, Node]] = deque([(0, self.root)])

        while q:
            level, current = q.popleft()

            if current not in res[level]:
                res[level].append(current)

            if current.left:
                q.append((level + 1, current.left))

            if current.right:
                q.append((level + 1, current.right))

        return res


@dataclass
class InputData:
    """Problem input data."""

    idd: int
    left: tuple[int, str]
    right: tuple[int, str]


def parse_input(
    filename: str, tree_left: Tree, tree_right: Tree, p3: bool = False
) -> None:
    """Parse the given input data and return."""
    data: dict[str, list[tuple[int, str]]] = defaultdict(list)

    for line in open(filename).readlines():
        if line.startswith("ADD"):
            matched = re.match(
                r"ADD id=(\d+) left=\[(\d+),(.+)\] right=\[(\d+),(.+)\]", line
            )

            if len(matched.groups()) == 5:
                idd, lr, lv, rr, rv = matched.groups()
                tree_left.add_node(data=(int(lr), lv))
                tree_right.add_node(data=(int(rr), rv))
                data[idd] += [(int(lr), lv), (int(rr), rv)]

        elif line.startswith("SWAP"):
            idd: str = line.strip().replace("SWAP ", "")
            target_nodes: list[tuple[int, str]] = data.get(idd)

            if target_nodes:
                found_nodes: list[Node] = [
                    x
                    for x in (
                        tree_left.get_node(
                            rank=target_nodes[0][0], value=target_nodes[0][1]
                        ),
                        tree_left.get_node(
                            rank=target_nodes[1][0], value=target_nodes[1][1]
                        ),
                        tree_right.get_node(
                            rank=target_nodes[0][0], value=target_nodes[0][1]
                        ),
                        tree_right.get_node(
                            rank=target_nodes[1][0], value=target_nodes[1][1]
                        ),
                    )
                    if x is not None
                ]

                if not p3:
                    Tree.swap_nodes(*found_nodes)
                else:
                    tree_left, tree_right = Tree.swap_branches(
                        tree_left, tree_right, *found_nodes
                    )


def part_01() -> None:
    """Solution to Part 1"""
    tree_left: Tree = Tree()
    tree_right: Tree = Tree()
    parse_input("q02_p01.in", tree_left=tree_left, tree_right=tree_right)

    tree_left_results: str = "".join(
        [n.value for n in max(tree_left.traverse_tree().values(), key=len)]
    )
    tree_right_results: str = "".join(
        [n.value for n in max(tree_right.traverse_tree().values(), key=len)]
    )

    print(f"Part 01: {tree_left_results + tree_right_results}")


def part_02() -> None:
    """Solution to Part 2"""
    tree_left: Tree = Tree()
    tree_right: Tree = Tree()
    parse_input("q02_p02.in", tree_left=tree_left, tree_right=tree_right)

    tree_left_results: str = "".join(
        [n.value for n in max(tree_left.traverse_tree().values(), key=len)]
    )
    tree_right_results: str = "".join(
        [n.value for n in max(tree_right.traverse_tree().values(), key=len)]
    )
    print(f"Part 02: {tree_left_results + tree_right_results}")


def part_03() -> None:
    """Solution to Part 3"""
    tree_left: Tree = Tree()
    tree_right: Tree = Tree()
    parse_input("q02_p03.in", tree_left=tree_left, tree_right=tree_right, p3=True)

    tree_left_results: str = "".join(
        [n.value for n in max(tree_left.traverse_tree().values(), key=len)]
    )
    tree_right_results: str = "".join(
        [n.value for n in max(tree_right.traverse_tree().values(), key=len)]
    )
    print(f"Part 03: {tree_left_results + tree_right_results}")


def main() -> None:
    """Entry point"""

    print(Timing(timeit(part_01, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_02, number=1)).microseconds, "μs\n")
    print(Timing(timeit(part_03, number=1)).microseconds, "μs\n")


if __name__ == "__main__":
    main()
