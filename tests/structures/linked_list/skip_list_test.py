import pytest

from cs.structures import SkipList


class TestSkipList:
    @staticmethod
    def test_insert() -> None:
        skip_list = SkipList[str, int]()
        skip_list.insert("Key1", 3)
        skip_list.insert("Key2", 12)
        skip_list.insert("Key3", 41)
        skip_list.insert("Key4", -19)

        node = skip_list
        all_values: dict[str, int] = {}
        while len(node.next) != 0:
            node = node.next[0]
            if node.key is not None and node.value is not None:
                all_values[node.key] = node.value

        assert len(all_values) == 4
        assert all_values["Key1"] == 3
        assert all_values["Key2"] == 12
        assert all_values["Key3"] == 41
        assert all_values["Key4"] == -19

    @staticmethod
    def test_insert_overrides_existing_value() -> None:
        skip_list = SkipList[str, int]()
        skip_list.insert("Key1", 10)
        skip_list.insert("Key1", 12)

        skip_list.insert("Key5", 7)
        skip_list.insert("Key7", 10)
        skip_list.insert("Key10", 5)

        skip_list.insert("Key7", 7)
        skip_list.insert("Key5", 5)
        skip_list.insert("Key10", 10)

        node = skip_list
        all_values: dict[str, int] = {}
        while len(node.next) != 0:
            node = node.next[0]
            if node.key is not None and node.value is not None:
                all_values[node.key] = node.value

        assert len(all_values) == 4
        assert all_values["Key1"] == 12
        assert all_values["Key7"] == 7
        assert all_values["Key5"] == 5
        assert all_values["Key10"] == 10

    @staticmethod
    def test_search() -> None:
        skip_list = SkipList[str, int]()
        with pytest.raises(KeyError):
            _ = skip_list["Some key"]

        skip_list.insert("Key2", 20)
        assert skip_list["Key2"] == 20

        skip_list.insert("Some Key", 10)
        skip_list.insert("Key2", 8)
        skip_list.insert("V", 13)

        assert skip_list["Key2"] == 8
        assert skip_list["Some Key"] == 10
        assert skip_list["V"] == 13

    @staticmethod
    def test_deleting_item_from_empty_list_raises_error() -> None:
        skip_list = SkipList[str, int]()
        with pytest.raises(KeyError):
            skip_list.remove("Some key")

        assert len(skip_list.next) == 0

        skip_list.insert("Key1", 12)
        skip_list.insert("V", 13)
        skip_list.insert("X", 14)
        skip_list.insert("Key2", 15)

        skip_list.remove("V")
        skip_list.remove("Key2")
        for key in ("V", "Key2"):
            with pytest.raises(KeyError):
                _ = skip_list[key]

    @staticmethod
    def test_delete_removes_only_given_key() -> None:
        skip_list = SkipList[str, int]()

        skip_list.insert("Key1", 12)
        skip_list.insert("V", 13)
        skip_list.insert("X", 14)
        skip_list.insert("Key2", 15)

        skip_list.remove("V")
        assert skip_list["X"] == 14
        assert skip_list["Key1"] == 12
        assert skip_list["Key2"] == 15

        skip_list.remove("X")
        assert skip_list["Key1"] == 12
        assert skip_list["Key2"] == 15

        skip_list.remove("Key1")
        for key in ("V", "X", "Key1"):
            with pytest.raises(KeyError):
                _ = skip_list[key]
        assert skip_list["Key2"] == 15

        skip_list.remove("Key2")
        for key in ("V", "X", "Key1", "Key2"):
            with pytest.raises(KeyError):
                _ = skip_list[key]

    @staticmethod
    def test_delete_doesnt_leave_dead_nodes() -> None:
        skip_list = SkipList[str, int]()

        skip_list.insert("Key1", 12)
        skip_list.insert("V", 13)
        skip_list.insert("X", 142)
        skip_list.insert("Key2", 15)

        skip_list.remove("X")
        assert len(list(skip_list)) == 3

    @staticmethod
    def test_iter_always_yields_sorted_values() -> None:
        def is_sorted(lst: list[int]) -> bool:
            return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))

        skip_list = SkipList[int, int]()
        for i in range(10):
            skip_list.insert(i, i)
        assert is_sorted(list(skip_list))
        skip_list.remove(5)
        skip_list.remove(8)
        skip_list.remove(2)
        assert is_sorted(list(skip_list))
        skip_list.insert(-12, -12)
        skip_list.insert(77, 77)
        assert is_sorted(list(skip_list))

    @staticmethod
    def test_repr() -> None:
        skip_list = SkipList[str, int]()

        assert repr(skip_list) == (
            "SkipList(key=None, value=None, next=[], p=0.5, max_level=16, level=0)"
        )

        skip_list.insert("A", 12)
        skip_list.insert("B", 13)
        skip_list.insert("C", 142)
        skip_list.insert("Hello", 142)

        assert str(skip_list) == (
            "______SkipList(level=3)______\n"
            "[root]---*     *     *     \n"
            "         |     |     |     \n"
            "[A]------A     |     |    \n"
            "         |     |     |     \n"
            "[B]------B     |     |    \n"
            "         |     |     |     \n"
            "[C]------C     C     C    \n"
            "         |     |     |     \n"
            "[Hello]--Hello Hello |    \n"
            "         |     |     |     \n"
            "None     *     *     *     "
        )
