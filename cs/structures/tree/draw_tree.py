from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto, unique
from typing import Any

from cs.structures.tree.binary_search_tree import BinaryTreeNode

MAX_HEIGHT = 1000
INFINITY = 1 << 8  # ~1 million


@unique
class ParentDirection(Enum):
    LEFT, ROOT, RIGHT = auto(), auto(), auto()


@dataclass
class AsciiNode:
    left: AsciiNode | None = None
    right: AsciiNode | None = None
    edge_length: int = 0  # length of the edge from this node to its children
    height: int = 0
    parent_dir: ParentDirection = ParentDirection.ROOT
    label: str = ""  # max supported unit32 in dec, 10 digits max


def build_ascii_tree_recursive(
    t: BinaryTreeNode[Any] | None, direction: ParentDirection = ParentDirection.ROOT
) -> AsciiNode | None:
    if t is None:
        return None

    left_side = build_ascii_tree_recursive(t.left, ParentDirection.LEFT)
    right_side = build_ascii_tree_recursive(t.right, ParentDirection.RIGHT)
    return AsciiNode(
        left=left_side, right=right_side, parent_dir=direction, label=str(t.data)
    )


def compute_profile(
    node: AsciiNode | None,
    lprofile: list[int],
    rprofile: list[int],
    xy: tuple[int, int] = (0, 0),
    left_side: bool = True,
) -> None:
    """
    Fills in the lprofile array for the given tree. It assumes that the center of
    the label of the root of this tree is located at a position (x,y) and assumes
    that the edge_length fields have been computed for this tree.
    """
    if node is None:
        return

    x, y = xy
    if left_side:
        isleft = int(node.parent_dir is ParentDirection.LEFT)
        lprofile[y] = min(lprofile[y], x - ((len(node.label) - isleft) // 2))
    else:
        notleft = int(node.parent_dir is not ParentDirection.LEFT)
        rprofile[y] = max(rprofile[y], x + ((len(node.label) - notleft) // 2))

    if (node.left if left_side else node.right) is not None:
        for i in range(1, min(node.edge_length + 1, MAX_HEIGHT - y)):
            if left_side:
                lprofile[y + i] = min(lprofile[y + i], x - i)
            else:
                rprofile[y + i] = max(rprofile[y + i], x + i)

    compute_profile(
        node.left,
        lprofile,
        rprofile,
        (x - node.edge_length - 1, y + node.edge_length + 1),
        left_side,
    )
    compute_profile(
        node.right,
        lprofile,
        rprofile,
        (x + node.edge_length + 1, y + node.edge_length + 1),
        left_side,
    )


def compute_edge_lengths(
    node: AsciiNode | None, lprofile: list[int], rprofile: list[int]
) -> None:
    """
    This function fills in the edge_length and height fields of the specified tree.
    """
    if node is None:
        return
    compute_edge_lengths(node.left, lprofile, rprofile)
    compute_edge_lengths(node.right, lprofile, rprofile)

    # first fill in the edge_length of node
    if node.left is None and node.right is None:
        node.edge_length = 0
    else:
        hmin = 0
        if node.left is not None:
            for i in range(min(node.left.height, MAX_HEIGHT)):
                rprofile[i] = -INFINITY
            compute_profile(node.left, lprofile, rprofile, left_side=False)
            hmin = node.left.height

        if node.right is not None:
            for i in range(min(node.right.height, MAX_HEIGHT)):
                lprofile[i] = INFINITY
            compute_profile(node.right, lprofile, rprofile, left_side=True)
            # If left is None then this value is 0.
            hmin = min(node.right.height, hmin)

        delta = max([4] + [4 + rprofile[i] - lprofile[i] for i in range(hmin)])
        # If the node has two children of height 1, then we allow the
        # two leaves to be within 1, instead of 2
        if (
            (node.left is not None and node.left.height == 1)
            or (node.right is not None and node.right.height == 1)
        ) and delta > 4:
            delta -= 1
        node.edge_length = ((delta + 1) // 2) - 1

    # now fill in the height of node
    h = 1
    if node.left is not None:
        h = max(node.left.height + node.edge_length + 1, h)
    if node.right is not None:
        h = max(node.right.height + node.edge_length + 1, h)
    node.height = h


def print_level(
    node: AsciiNode | None, x: int, level: int, result: list[str], print_next: int = 0
) -> int:
    """
    This function prints the given level of the given tree, assuming that the node
    has the given x coordinate. print_next is the x coordinate of the next char
    printed, used for printing the next node in the same level.
    """
    if node is None:
        return print_next

    if level == 0:
        isleft = int(node.parent_dir == ParentDirection.LEFT)
        spaces = x - print_next - ((len(node.label) - isleft) // 2)
        print_next += spaces + len(node.label)
        result.append(f"{' ' * spaces}{node.label}")

    elif node.edge_length >= level:
        if node.left is not None:
            spaces = x - print_next - level
            print_next += spaces + 1
            result.append(f"{' ' * spaces}/")
        if node.right is not None:
            spaces = x - print_next + level
            print_next += spaces + 1
            result.append(f"{' ' * spaces}\\")

    else:
        print_next = print_level(
            node.left,
            x - node.edge_length - 1,
            level - node.edge_length - 1,
            result,
            print_next,
        )
        print_next = print_level(
            node.right,
            x + node.edge_length + 1,
            level - node.edge_length - 1,
            result,
            print_next,
        )
    return print_next


def draw_tree(t: BinaryTreeNode[Any] | None) -> str:
    if t is None:
        return ""
    proot = build_ascii_tree_recursive(t)
    assert proot is not None

    lprofile = [0] * MAX_HEIGHT
    rprofile = [0] * MAX_HEIGHT

    compute_edge_lengths(proot, lprofile, rprofile)
    if proot.height >= MAX_HEIGHT:
        raise RuntimeWarning(
            f"This tree is taller than {MAX_HEIGHT}, and may be drawn incorrectly."
        )

    for i in range(min(proot.height, MAX_HEIGHT)):
        lprofile[i] = INFINITY

    compute_profile(proot, lprofile, rprofile, left_side=True)
    xmin = min([0] + [lprofile[i] for i in range(min(proot.height, MAX_HEIGHT))])

    result: list[str] = []
    for i in range(proot.height):
        print_level(proot, -xmin, i, result)
        result.append("\n")

    return "".join(result)
