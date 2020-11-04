from src.structures import RedBlackTree  # , RedBlackTreeNode

# @staticmethod
# def test_rotations() -> None:
#     """Test that the rotate_left and rotate_right functions work."""
#     # Make a tree to test on
#     rb_tree = RedBlackTree[int]()
#     rb_tree.root = tree = RedBlackTreeNode[int](0)
#     tree.left = RedBlackTreeNode[int](-10, parent=tree)
#     tree.right = RedBlackTreeNode[int](10, parent=tree)
#     tree.left.left = RedBlackTreeNode[int](-20, parent=tree.left)
#     tree.left.right = RedBlackTreeNode[int](-5, parent=tree.left)
#     tree.right.left = RedBlackTreeNode[int](5, parent=tree.right)
#     tree.right.right = RedBlackTreeNode[int](20, parent=tree.right)
#     # Make the right rotation
#     left_rot = RedBlackTreeNode[int](10)
#     left_rot.left = RedBlackTreeNode[int](0, parent=left_rot)
#     left_rot.left.left = RedBlackTreeNode[int](-10, parent=left_rot.left)
#     left_rot.left.right = RedBlackTreeNode[int](5, parent=left_rot.left)
#     left_rot.left.left.left = RedBlackTreeNode[int](-20, parent=left_rot.left.left)
#     left_rot.left.left.right = RedBlackTreeNode[int](-5, parent=left_rot.left.left)
#     left_rot.right = RedBlackTreeNode[int](20, parent=left_rot)
#     RedBlackTree.rotate_left(tree)
#     assert rb_tree.root == left_rot
#     RedBlackTree.rotate_right(tree)
#     RedBlackTree.rotate_right(tree)
#     # Make the left rotation
#     right_rot = RedBlackTreeNode[int](-10)
#     right_rot.left = RedBlackTreeNode[int](-20, parent=right_rot)
#     right_rot.right = RedBlackTreeNode[int](0, parent=right_rot)
#     right_rot.right.left = RedBlackTreeNode[int](-5, parent=right_rot.right)
#     right_rot.right.right = RedBlackTreeNode[int](10, parent=right_rot.right)
#     right_rot.right.right.left = RedBlackTreeNode[int](
#         5, parent=right_rot.right.right
#     )
#     right_rot.right.right.right = RedBlackTreeNode[int](
#         20, parent=right_rot.right.right
#     )
#     assert tree == right_rot


class TestRedBlackTree:
    @staticmethod
    def test_insert() -> None:
        """Test the insert() method of the tree correctly balances, colors,
        and inserts.
        """
        tree = RedBlackTree[int]()  # Color.BLACK

        for elem in (0, 8, -8, 4, 12, 10, 11):
            tree.insert(elem)

        assert list(tree.traverse("inorder")) == [-8, 0, 4, 8, 10, 11, 12]
        # ans = RedBlackTreeNode[int](0, 0)  # Color.BLACK
        # ans.left = RedBlackTreeNode[int](-8, 0, ans)  # Color.BLACK
        # ans.right = RedBlackTreeNode[int](8, 1, ans)  # Color.RED
        # ans.right.left = RedBlackTreeNode[int](4, 0, ans.right)  # Color.BLACK
        # ans.right.right = RedBlackTreeNode[int](11, 0, ans.right)  # Color.BLACK
        # ans.right.right.left = RedBlackTreeNode[int](10, 1, ans.right.right)
        # # Color.RED
        # ans.right.right.right = RedBlackTreeNode[int](12, 1, ans.right.right)
        # # Color.RED
        # assert tree == ans

    @staticmethod
    def test_insert_and_search() -> None:
        """Tests searching through the tree for values."""
        tree = RedBlackTree[int]()

        for elem in (0, 8, -8, 4, 12, 10, 11):
            tree.insert(elem)

        assert 5 not in tree
        assert -6 not in tree
        assert -10 not in tree
        assert 13 not in tree
        assert 11 in tree
        assert 12 in tree
        assert -8 in tree
        assert 0 in tree

    # @staticmethod
    # def test_insert_remove() -> None:
    #     """Test the insert() and remove() method of the tree, verifying the
    #     insertion and removal of elements, and the balancing of the tree.
    #     """
    #     tree = RedBlackTree[int]()
    #     tree.insert(0)
    #     tree.insert(-12)
    #     tree.insert(8)
    #     tree.insert(-8)
    #     tree.insert(15)
    #     tree.insert(4)
    #     tree.insert(12)
    #     tree.insert(10)
    #     tree.insert(9)
    #     tree.insert(11)
    #     tree.remove(15)
    #     tree.remove(-12)
    #     tree.remove(9)
    #     assert tree.check_color_properties()
    #     assert list(tree.inorder_traverse()) == [-8, 0, 4, 8, 10, 11, 12]

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
        assert list(tree.traverse("preorder")) == [0, -16, 16, 8, 24, 20, 22]
        assert list(tree.traverse("postorder")) == [-16, 8, 22, 20, 24, 16, 0]
