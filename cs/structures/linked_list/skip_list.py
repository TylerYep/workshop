"""
Based on "Skip Lists: A Probabilistic Alternative to Balanced Trees" by William Pugh
https://epaperpress.com/sortsearch/download/skiplist.pdf
"""
from __future__ import annotations

import random
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Generic, TypeVar, cast

from cs.util import Comparable

KT = TypeVar("KT", bound=Comparable)
VT = TypeVar("VT")


@dataclass
class SkipList(Generic[KT, VT]):
    key: KT | None = None
    value: VT | None = None
    next: list[SkipList[KT, VT]] = field(default_factory=list)
    p: float = 0.5
    max_level: int = 16
    level: int = 0

    def __str__(self) -> str:
        """
        :return: Visual representation of SkipList

        >>> skip_list = SkipList()
        >>> print(skip_list)
        SkipList(level=0)
        >>> skip_list.insert("Key1", "Value")
        >>> print(skip_list) # doctest: +ELLIPSIS
        SkipList(level=...
        [root]--...
        [Key1]--Key1...
        None    *...
        >>> skip_list.insert("Key2", "OtherValue")
        >>> print(skip_list) # doctest: +ELLIPSIS
        SkipList(level=...
        [root]--...
        [Key1]--Key1...
        [Key2]--Key2...
        None    *...
        """
        items = list(self)
        if len(items) == 0:
            return f"SkipList(level={self.level})"

        key_size = max(len(str(item)) for item in items)
        label_size = max(max((len(str(item)) for item in items), default=4), 4) + 4
        node = self
        forwards = node.next.copy()
        lines = [
            f"[{node.key or 'root'}]".ljust(label_size, "-")
            + f"*{' ' * key_size}" * len(forwards),
            " " * label_size + f"|{' ' * key_size}" * len(forwards),
        ]

        while len(node.next) != 0:
            node = node.next[0]
            lines += [
                f"[{node.key}]".ljust(label_size, "-")
                + " ".join(
                    (str(n.key) if n.key == node.key else "|").ljust(key_size, " ")
                    for n in forwards
                ),
                " " * label_size + f"|{' ' * key_size}" * len(forwards),
            ]
            forwards[: len(node.next)] = node.next

        lines.append("None".ljust(label_size) + f"*{' ' * key_size}" * len(forwards))
        return f"______SkipList(level={self.level})______\n" + "\n".join(lines)

    def __iter__(self) -> Iterator[KT]:
        node = self
        while len(node.next) != 0:
            yield cast(KT, node.next[0].key)
            node = node.next[0]

    def __getitem__(self, key: KT) -> VT:
        node, _ = self._locate_node(key)
        if node is None or node.value is None:
            raise KeyError
        return node.value

    def __contains__(self, key: KT) -> bool:
        """
        :param key: Search key.
        :return: Value associated with given key
            or None if given key is not present.

        >>> skip_list = SkipList()
        >>> 2 in skip_list
        False
        >>> skip_list.insert(2, "Two")
        >>> 2 in skip_list
        True
        >>> skip_list[2]
        'Two'
        >>> skip_list.insert(2, "Three")
        >>> skip_list[2]
        'Three'
        """
        node, _ = self._locate_node(key)
        return node is not None

    def random_level(self) -> int:
        """
        :return: Random level from [1, self.max_level] interval.
                 Higher values are less likely.
        """
        level = 1
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level

    def remove(self, key: KT) -> None:
        """
        :param key: Key to remove from list.

        >>> skip_list = SkipList()
        >>> skip_list.insert(2, "Two")
        >>> skip_list.insert(1, "One")
        >>> skip_list.insert(3, "Three")
        >>> list(skip_list)
        [1, 2, 3]
        >>> skip_list.remove(2)
        >>> list(skip_list)
        [1, 3]
        """
        node, update_vector = self._locate_node(key)
        if node is None:
            raise KeyError(f"List does not contain: {key}")

        for i, update_node in enumerate(update_vector):
            # Remove or replace all references to removed node.
            if len(update_node.next) > i and update_node.next[i].key == key:
                if len(node.next) > i:
                    update_node.next[i] = node.next[i]
                else:
                    update_node.next = update_node.next[:i]

    def insert(self, key: KT, value: VT) -> None:
        """
        :param key: Key to insert.
        :param value: Value associated with given key.

        >>> skip_list = SkipList()
        >>> skip_list.insert(2, "Two")
        >>> skip_list[2]
        'Two'
        >>> list(skip_list)
        [2]
        """
        node, update_vector = self._locate_node(key)
        if node is not None:
            node.value = value
            return

        level = self.random_level()
        if level > self.level:
            # After level increase we have to add additional nodes to head.
            for _ in range(self.level - 1, level):
                update_vector.append(self)
            self.level = level

        new_node = SkipList(key, value)
        for i, update_node in enumerate(update_vector[:level]):
            # Change references to pass through new node.
            if len(update_node.next) > i:
                new_node.next.append(update_node.next[i])
            if len(update_node.next) < i + 1:
                update_node.next.append(new_node)
            else:
                update_node.next[i] = new_node

    def _locate_node(
        self, key: KT
    ) -> tuple[SkipList[KT, VT] | None, list[SkipList[KT, VT]]]:
        """
        :param key: Searched key,
        :return: Tuple with searched node (or None if given key is not present)
                 and list of nodes that refer (if key is present) of should refer to
                 given node.
        """
        # SkipListNodes with refer or should refer to output node
        update_vector = []
        node = self

        for i in reversed(range(self.level)):
            # i < node.level - When node level is lesser than `i` decrement `i`.
            # node.next[i].key < key - Jumping to node with key value higher
            #                             or equal to searched key would result
            #                             in skipping searched key.
            while (
                i < len(node.next) and node.next[i].key < key  # type: ignore[operator]
            ):
                node = node.next[i]
            # Each leftmost node (relative to searched node) will potentially have to
            # be updated.
            update_vector.append(node)

        update_vector.reverse()  # Note that we were inserting values in reverse order.

        # len(node.next) != 0 - If current node doesn't contain any further
        #                          references then searched key is not present.
        # node.next[0].key == key - Next node key should be equal to search key
        #                              if key is present.
        if len(node.next) != 0 and node.next[0].key == key:
            return node.next[0], update_vector
        return None, update_vector
