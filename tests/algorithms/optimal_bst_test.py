from cs.algorithms import build_optimal_bst
from cs.structures import BinarySearchTree, BinaryTreeNode


def test_build_optimal_bst() -> None:
    nodes = {
        12: BinaryTreeNode(12, hits=8),
        10: BinaryTreeNode(10, hits=34),
        20: BinaryTreeNode(20, hits=50),
        42: BinaryTreeNode(42, hits=3),
        25: BinaryTreeNode(25, hits=40),
        37: BinaryTreeNode(37, hits=30),
    }

    tree, cost = build_optimal_bst(list(nodes.values()))

    assert cost == 324

    expected_tree = BinarySearchTree[int]()

    expected_tree.root = nodes[20]
    nodes[20].left = nodes[10]
    nodes[20].right = nodes[25]
    nodes[10].right = nodes[12]
    nodes[25].right = nodes[37]
    nodes[37].right = nodes[42]
    expected_tree.size = len(nodes)

    assert tree == expected_tree
