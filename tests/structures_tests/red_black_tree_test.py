from src.structures import RedBlackTree


"""
Code for testing the various
functions of the red-black tree.
"""


def test_rotations() -> None:
    """Test that the rotate_left and rotate_right functions work."""
    # Make a tree to test on
    tree = RedBlackTree[int](0)
    tree.left = RedBlackTree[int](-10, parent=tree)
    tree.right = RedBlackTree[int](10, parent=tree)
    tree.left.left = RedBlackTree[int](-20, parent=tree.left)
    tree.left.right = RedBlackTree[int](-5, parent=tree.left)
    tree.right.left = RedBlackTree[int](5, parent=tree.right)
    tree.right.right = RedBlackTree[int](20, parent=tree.right)
    # Make the right rotation
    left_rot = RedBlackTree[int](10)
    left_rot.left = RedBlackTree[int](0, parent=left_rot)
    left_rot.left.left = RedBlackTree[int](-10, parent=left_rot.left)
    left_rot.left.right = RedBlackTree[int](5, parent=left_rot.left)
    left_rot.left.left.left = RedBlackTree[int](-20, parent=left_rot.left.left)
    left_rot.left.left.right = RedBlackTree[int](-5, parent=left_rot.left.left)
    left_rot.right = RedBlackTree[int](20, parent=left_rot)
    tree = tree.rotate_left()
    assert tree == left_rot
    tree = tree.rotate_right()
    tree = tree.rotate_right()
    # Make the left rotation
    right_rot = RedBlackTree[int](-10)
    right_rot.left = RedBlackTree[int](-20, parent=right_rot)
    right_rot.right = RedBlackTree[int](0, parent=right_rot)
    right_rot.right.left = RedBlackTree[int](-5, parent=right_rot.right)
    right_rot.right.right = RedBlackTree[int](10, parent=right_rot.right)
    right_rot.right.right.left = RedBlackTree[int](5, parent=right_rot.right.right)
    right_rot.right.right.right = RedBlackTree[int](20, parent=right_rot.right.right)
    assert tree == right_rot


def test_insert() -> None:
    """Test the insert() method of the tree correctly balances, colors,
    and inserts.
    """
    tree = RedBlackTree[int](0)
    tree.insert(8)
    tree.insert(-8)
    tree.insert(4)
    tree.insert(12)
    tree.insert(10)
    tree.insert(11)
    ans = RedBlackTree[int](0, 0)
    ans.left = RedBlackTree[int](-8, 0, ans)
    ans.right = RedBlackTree[int](8, 1, ans)
    ans.right.left = RedBlackTree[int](4, 0, ans.right)
    ans.right.right = RedBlackTree[int](11, 0, ans.right)
    ans.right.right.left = RedBlackTree[int](10, 1, ans.right.right)
    ans.right.right.right = RedBlackTree[int](12, 1, ans.right.right)
    assert tree == ans


def test_insert_and_search() -> None:
    """Tests searching through the tree for values."""
    tree = RedBlackTree[int](0)
    tree.insert(8)
    tree.insert(-8)
    tree.insert(4)
    tree.insert(12)
    tree.insert(10)
    tree.insert(11)
    assert 5 not in tree
    assert -6 not in tree
    assert -10 not in tree
    assert 13 not in tree
    assert 11 in tree
    assert 12 in tree
    assert -8 in tree
    assert 0 in tree


def test_insert_delete() -> None:
    """Test the insert() and delete() method of the tree, verifying the
    insertion and removal of elements, and the balancing of the tree.
    """
    tree = RedBlackTree[int](0)
    tree = tree.insert(-12)
    tree = tree.insert(8)
    tree = tree.insert(-8)
    tree = tree.insert(15)
    tree = tree.insert(4)
    tree = tree.insert(12)
    tree = tree.insert(10)
    tree = tree.insert(9)
    tree = tree.insert(11)
    tree = tree.remove(15)
    tree = tree.remove(-12)
    tree = tree.remove(9)
    assert tree.check_color_properties()
    assert list(tree.inorder_traverse()) == [-8, 0, 4, 8, 10, 11, 12]


def test_floor_ceil() -> None:
    """Tests the floor and ceiling functions in the tree."""
    tree = RedBlackTree[int](0)
    tree.insert(-16)
    tree.insert(16)
    tree.insert(8)
    tree.insert(24)
    tree.insert(20)
    tree.insert(22)
    tuples = [(-20, None, -16), (-10, -16, 0), (8, 8, 8), (50, 24, None)]
    for val, floor, ceil in tuples:
        assert tree.floor(val) == floor or tree.ceil(val) != ceil


def test_min_max() -> None:
    """Tests the min and max functions in the tree."""
    tree = RedBlackTree[int](0)
    tree.insert(-16)
    tree.insert(16)
    tree.insert(8)
    tree.insert(24)
    tree.insert(20)
    tree.insert(22)
    assert tree.get_max() == 24
    assert tree.get_min() == -16


def test_tree_traversal() -> None:
    """Tests the three different tree traversal functions."""
    tree = RedBlackTree[int](0)
    tree = tree.insert(-16)
    tree.insert(16)
    tree.insert(8)
    tree.insert(24)
    tree.insert(20)
    tree.insert(22)
    assert list(tree.inorder_traverse()) == [-16, 0, 8, 16, 20, 22, 24]
    assert list(tree.preorder_traverse()) == [0, -16, 16, 8, 22, 20, 24]
    assert list(tree.postorder_traverse()) == [-16, 8, 20, 24, 22, 16, 0]


def test_tree_chaining() -> None:
    """Tests the three different tree chaining functions."""
    tree = RedBlackTree[int](0)
    tree = tree.insert(-16).insert(16).insert(8).insert(24).insert(20).insert(22)
    assert list(tree.inorder_traverse()) == [-16, 0, 8, 16, 20, 22, 24]
    assert list(tree.preorder_traverse()) == [0, -16, 16, 8, 22, 20, 24]
    assert list(tree.postorder_traverse()) == [-16, 8, 20, 24, 22, 16, 0]
