from typing import Dict, List

import pytest

from src.structures import SkipList


def test_insert() -> None:
    skip_list = SkipList[str, int]()
    skip_list.insert("Key1", 3)
    skip_list.insert("Key2", 12)
    skip_list.insert("Key3", 41)
    skip_list.insert("Key4", -19)

    node = skip_list.head
    all_values: Dict[str, int] = {}
    while node.level != 0:
        node = node.next[0]
        if node.value is not None:
            all_values[node.key] = node.value

    assert len(all_values) == 4
    assert all_values["Key1"] == 3
    assert all_values["Key2"] == 12
    assert all_values["Key3"] == 41
    assert all_values["Key4"] == -19


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

    node = skip_list.head
    all_values: Dict[str, int] = {}
    while node.level != 0:
        node = node.next[0]
        if node.value is not None:
            all_values[node.key] = node.value

    assert len(all_values) == 4
    assert all_values["Key1"] == 12
    assert all_values["Key7"] == 7
    assert all_values["Key5"] == 5
    assert all_values["Key10"] == 10


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


def test_deleting_item_from_empty_list_do_nothing() -> None:
    skip_list = SkipList[str, int]()
    skip_list.delete("Some key")

    assert len(skip_list.head.next) == 0

    skip_list.insert("Key1", 12)
    skip_list.insert("V", 13)
    skip_list.insert("X", 14)
    skip_list.insert("Key2", 15)

    skip_list.delete("V")
    skip_list.delete("Key2")
    for key in ("V", "Key2"):
        with pytest.raises(KeyError):
            _ = skip_list[key]


def test_delete_removes_only_given_key() -> None:
    skip_list = SkipList[str, int]()

    skip_list.insert("Key1", 12)
    skip_list.insert("V", 13)
    skip_list.insert("X", 14)
    skip_list.insert("Key2", 15)

    skip_list.delete("V")
    assert skip_list["X"] == 14
    assert skip_list["Key1"] == 12
    assert skip_list["Key2"] == 15

    skip_list.delete("X")
    assert skip_list["Key1"] == 12
    assert skip_list["Key2"] == 15

    skip_list.delete("Key1")
    for key in ("V", "X", "Key1"):
        with pytest.raises(KeyError):
            _ = skip_list[key]
    assert skip_list["Key2"] == 15

    skip_list.delete("Key2")
    for key in ("V", "X", "Key1", "Key2"):
        with pytest.raises(KeyError):
            _ = skip_list[key]


def test_delete_doesnt_leave_dead_nodes() -> None:
    skip_list = SkipList[str, int]()

    skip_list.insert("Key1", 12)
    skip_list.insert("V", 13)
    skip_list.insert("X", 142)
    skip_list.insert("Key2", 15)

    skip_list.delete("X")
    assert len(list(skip_list)) == 3


def test_iter_always_yields_sorted_values() -> None:
    def is_sorted(lst: List[int]) -> bool:
        for item, next_item in zip(lst, lst[1:]):
            if next_item < item:
                return False
        return True

    skip_list = SkipList[int, int]()
    for i in range(10):
        skip_list.insert(i, i)
    assert is_sorted(list(skip_list))
    skip_list.delete(5)
    skip_list.delete(8)
    skip_list.delete(2)
    assert is_sorted(list(skip_list))
    skip_list.insert(-12, -12)
    skip_list.insert(77, 77)
    assert is_sorted(list(skip_list))
