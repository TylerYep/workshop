from cs.structures import RedBlackTree, RedBlackTreeNode
from cs.structures.tree.red_black_tree import Color


class TestRedBlackTree:
    @staticmethod
    def test_rotations() -> None:
        """Test that the rotate_left and rotate_right functions work."""
        # Make a tree to test on
        tree = RedBlackTreeNode[int](0)
        tree.left = RedBlackTreeNode[int](-10, parent=tree)
        tree.right = RedBlackTreeNode[int](10, parent=tree)
        tree.left.left = RedBlackTreeNode[int](-20, parent=tree.left)
        tree.left.right = RedBlackTreeNode[int](-5, parent=tree.left)
        tree.right.left = RedBlackTreeNode[int](5, parent=tree.right)
        tree.right.right = RedBlackTreeNode[int](20, parent=tree.right)

        # Make the left rotation
        left_rot = RedBlackTreeNode[int](10)
        left_rot.left = RedBlackTreeNode[int](0, parent=left_rot)
        left_rot.left.left = RedBlackTreeNode[int](-10, parent=left_rot.left)
        left_rot.left.right = RedBlackTreeNode[int](5, parent=left_rot.left)
        left_rot.left.left.left = RedBlackTreeNode[int](-20, parent=left_rot.left.left)
        left_rot.left.left.right = RedBlackTreeNode[int](-5, parent=left_rot.left.left)
        left_rot.right = RedBlackTreeNode[int](20, parent=left_rot)

        tree = RedBlackTree.rotate_left(tree)

        assert tree == left_rot

        tree = RedBlackTree.rotate_right(tree)
        tree = RedBlackTree.rotate_right(tree)

        # Make the right rotation
        right_rot = RedBlackTreeNode[int](-10)
        right_rot.left = RedBlackTreeNode[int](-20, parent=right_rot)
        right_rot.right = RedBlackTreeNode[int](0, parent=right_rot)
        right_rot.right.left = RedBlackTreeNode[int](-5, parent=right_rot.right)
        right_rot.right.right = RedBlackTreeNode[int](10, parent=right_rot.right)
        right_rot.right.right.left = RedBlackTreeNode[int](
            5, parent=right_rot.right.right
        )
        right_rot.right.right.right = RedBlackTreeNode[int](
            20, parent=right_rot.right.right
        )

        assert tree == right_rot

    @staticmethod
    def test_insert() -> None:
        """Test the insert() method of the tree correctly balances, colors,
        and inserts.
        """
        tree = RedBlackTree[int]()

        for elem in (0, 8, -8, 4, 12, 10, 11):
            tree.insert(elem)

        assert list(tree.traverse("inorder")) == [-8, 0, 4, 8, 10, 11, 12]

        ans = RedBlackTreeNode[int](0, color=Color.BLACK)
        ans.left = RedBlackTreeNode[int](-8, parent=ans)
        ans.right = RedBlackTreeNode[int](8, parent=ans, color=Color.RED)
        ans.right.left = RedBlackTreeNode[int](4, parent=ans.right)
        ans.right.right = RedBlackTreeNode[int](11, parent=ans.right)
        ans.right.right.left = RedBlackTreeNode[int](
            10, parent=ans.right.right, color=Color.RED
        )
        ans.right.right.right = RedBlackTreeNode[int](
            12, parent=ans.right.right, color=Color.RED
        )
        assert tree.root == ans

    @staticmethod
    def test_search() -> None:
        """Tests searching through the tree for values."""
        tree = RedBlackTree[int]()

        for elem in (0, 8, -8, 4, 12, 10, 11):
            tree.insert(elem)

        for elem in (5, -6, -10, 13):
            assert elem not in tree
        for elem in (11, 12, -8, 0):
            assert elem in tree

    @staticmethod
    def test_remove() -> None:
        """
        Test the insert() and remove() method of the tree, verifying the
        insertion and removal of elements, and the balancing of the tree.
        """
        tree = RedBlackTree[int]()

        for elem in (0, -12, 8, -8, 15, 4, 12, 10, 9, 11):
            tree.insert(elem)
        for elem in (15, -12, 9):
            tree.remove(elem)

        # assert tree.check_correctness()
        assert list(tree.traverse("inorder")) == [-8, 0, 4, 8, 10, 11, 12]

    # @staticmethod
    # def test_floor_ceil() -> None:
    #     """Tests the floor and ceiling functions in the tree."""
    #     tree = RedBlackTree[int]()

    #     for elem in (0, -16, 16, 8, 24, 20, 22):
    #         tree.insert(elem)

    #     tuples = [(-20, None, -16), (-10, -16, 0), (8, 8, 8), (50, 24, None)]
    #     for val, floor, ceil in tuples:
    #         assert tree.floor(val) == floor or tree.ceil(val) != ceil

    @staticmethod
    def test_min_max() -> None:
        """Tests the min and max functions in the tree."""
        tree = RedBlackTree[int]()

        for elem in (0, -16, 16, 8, 24, 20, 22):
            tree.insert(elem)

        assert tree.max_element() == 24
        assert tree.min_element() == -16

    @staticmethod
    def test_tree_traversal() -> None:
        """Tests the three different tree traversal functions."""
        tree = RedBlackTree[int]()

        for elem in (0, -16, 16, 8, 24, 20, 22):
            tree.insert(elem)

        assert list(tree.traverse("inorder")) == [-16, 0, 8, 16, 20, 22, 24]
        assert list(tree.traverse("preorder")) == [0, -16, 16, 8, 22, 20, 24]
        assert list(tree.traverse("postorder")) == [-16, 8, 20, 24, 22, 16, 0]

    @staticmethod
    def test_print_tree() -> None:
        tree = RedBlackTree[int]()
        for elem in (8, 6, 1, 73, 11):
            tree.insert(elem)

        assert repr(tree) == (
            "RedBlackTree(root=RedBlackTreeNode(\n"
            "    data=6,\n"
            "    left=RedBlackTreeNode(data=1),\n"
            "    right=RedBlackTreeNode(\n"
            "        data=11,\n"
            "        left=RedBlackTreeNode(data=8),\n"
            "        right=RedBlackTreeNode(data=73)\n"
            "    )\n"
            "), size=5)"
        )
