from cs.structures import RedBlackTree


class TestDrawTree:
    @staticmethod
    def test_empty_tree() -> None:
        t = RedBlackTree[int]()
        assert str(t).split("\n") == [""]

    @staticmethod
    def test_small_tree() -> None:
        t = RedBlackTree[int]()
        t.insert(17)
        assert str(t).split("\n") == ["17", ""]

        t.insert(14)
        assert str(t).split("\n") == [
            " 17",
            " /",
            "14",
            "",
        ]

        for i in range(0, 10, 2):
            t.insert(i)
        assert str(t).split("\n") == [
            "   14",
            "   / \\",
            "  2  17",
            " / \\",
            "0   6",
            "   / \\",
            "  4   8",
            "",
        ]

    @staticmethod
    def test_large_tree() -> None:
        t = RedBlackTree[int]()
        t.insert(17)
        t.insert(14)
        for i in range(0, 10, 2):
            t.insert(i)
        for i in range(1, 10, 2):
            t.insert(i)

        assert str(t).split("\n") == [
            "          6",
            "         / \\",
            "        /   \\",
            "       /     \\",
            "      /       \\",
            "     /         \\",
            "    2          14",
            "   / \\         / \\",
            "  /   \\       8  17",
            " /     \\     / \\",
            "0       4   7   9",
            " \\     / \\",
            "  1   3   5",
            "",
        ]

        for i in range(100, 10, -6):
            t.insert(i)

        assert str(t).split("\n") == [
            "                     58",
            "                     / \\",
            "                    /   \\",
            "                   /     \\",
            "                  /       \\",
            "                 /         \\",
            "                /           \\",
            "               /             \\",
            "              /               \\",
            "             /                 \\",
            "            6                  82",
            "           / \\                 / \\",
            "          /   \\               /   \\",
            "         /     \\             /     \\",
            "        /       \\           /       \\",
            "       /         \\         70       94",
            "      /           \\       / \\       / \\",
            "     /             \\     /   \\     /   \\",
            "    2              34   64   76   88   100",
            "   / \\             / \\",
            "  /   \\           /   \\",
            " /     \\         /     \\",
            "0       4       /       \\",
            " \\     / \\     14       46",
            "  1   3   5   / \\       / \\",
            "             /   \\     /   \\",
            "            /     \\   40   52",
            "           8      22",
            "          / \\     / \\",
            "         7   9   /   \\",
            "                17   28",
            "               /",
            "              16",
            "",
        ]
