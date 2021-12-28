from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

from cs.structures import BinarySearchTree, BinaryTreeNode, Graph
from cs.util import Comparable

T = TypeVar("T", bound=Comparable)


def build_optimal_bst(
    nodes: Sequence[BinaryTreeNode[T]],
) -> tuple[BinarySearchTree[T], float]:
    """
    This function implements an optimal binary search tree-building dynamic programming
    algorithm that delivers O(n^2) performance.

    The goal of the optimal BST problem is to build a low-cost BST for a given set of
    nodes, each with its own key and frequency. The frequency of the node is defined as
    how many times the node is being searched. The search cost of binary search tree is
    given by the formula:

    cost(1, n) = sum_{i=1}^n [node_i_freq * (depth(node_i) + 1)]

    where n is number of nodes in the BST. The characteristic of low-cost BSTs is having
    a faster overall search time than other implementations. The reason for their fast
    search time is that the nodes with high frequencies will be placed near the root of
    the tree, while nodes with low frequencies will be placed near the leaves of the
    tree, thus reducing search time in the most frequent instances.
    """

    def _build_tree(
        cost_table: list[list[int]],
        orig_nodes: list[BinaryTreeNode[T]],
        i: int,
        j: int,
        parent: BinaryTreeNode[T] | None = None,
    ) -> BinaryTreeNode[T] | None:
        if i > j or i < 0 or j > len(cost_table) - 1:
            return None

        node = cost_table[i][j]
        tree_node = orig_nodes[node]
        tree_node.parent = parent
        tree_node.left = _build_tree(cost_table, orig_nodes, i, node - 1, tree_node)
        tree_node.right = _build_tree(cost_table, orig_nodes, node + 1, j, tree_node)
        return tree_node

    sorted_nodes = sorted(nodes, key=lambda node: node.data)
    n = len(sorted_nodes)
    freqs = [sorted_nodes[i].hits for i in range(n)]

    # dp stores the overall minimized tree cost. For each key, cost = frequency of key.
    # sums stores the sum of frequencies of nodes between i and j, inclusive.
    # root stores tree roots that will be used for constructing binary search tree.
    dp = [[freqs[i] if i == j else 0 for j in range(n)] for i in range(n)]
    sums = [list(d) for d in dp]
    root = [[i if i == j else 0 for j in range(n)] for i in range(n)]

    for interval_length in range(2, n + 1):
        for i in range(n - interval_length + 1):
            j = i + interval_length - 1
            dp[i][j] = Graph.INT_INFINITY
            sums[i][j] = sums[i][j - 1] + freqs[j]

            # Apply Knuth's optimization (without optimizing: for r in range(i, j + 1))
            for r in range(root[i][j - 1], root[i + 1][j] + 1):  # r is a root
                optimal_left_cost = dp[i][r - 1] if r != i else 0
                optimal_right_cost = dp[r + 1][j] if r != j else 0
                cost = optimal_left_cost + sums[i][j] + optimal_right_cost
                if dp[i][j] > cost:
                    dp[i][j] = cost
                    root[i][j] = r

    tree = BinarySearchTree[T]()
    tree.root = _build_tree(root, sorted_nodes, 0, n - 1)
    tree.size = n
    return tree, dp[0][n - 1]
