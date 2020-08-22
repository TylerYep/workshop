"""
Based on "Skip Lists: A Probabilistic Alternative to Balanced Trees" by William Pugh
https://epaperpress.com/sortsearch/download/skiplist.pdf
"""
from __future__ import annotations

from dataclasses import dataclass, field
from random import random
from typing import Generic, Iterator, List, Optional, Tuple, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")
# TODO delete should raise an error if the key does not exist


@dataclass
class SkipListNode(Generic[KT, VT]):
    key: KT
    value: VT
    next: List[SkipListNode[KT, VT]] = field(default_factory=list)

    @property
    def level(self) -> int:
        """
        :return: Number of forward references

        >>> node = SkipListNode("Key", 2)
        >>> node.level
        0
        >>> node.next.append(SkipListNode("Key2", 4))
        >>> node.level
        1
        >>> node.next.append(SkipListNode("Key3", 6))
        >>> node.level
        2
        """
        return len(self.next)


@dataclass
class SkipList(Generic[KT, VT]):
    def __init__(self, p: float = 0.5, max_level: int = 16) -> None:
        # TODO This self.head is a big problem for the type-checker.
        self.head = SkipListNode(None, None)
        self.level = 0
        self.p = p
        self.max_level = max_level

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

        label_size = max(max((len(str(item)) for item in items), default=4), 4) + 4
        node = self.head
        forwards = node.next.copy()
        lines = [
            f"[{'root' if node.key is None else node.key}]".ljust(label_size, "-")
            + "* " * len(forwards),
            " " * label_size + "| " * len(forwards),
        ]

        while len(node.next) != 0:
            node = node.next[0]
            lines += [
                f"[{node.key}]".ljust(label_size, "-")
                + " ".join(str(n.key) if n.key == node.key else "|" for n in forwards),
                " " * label_size + "| " * len(forwards),
            ]
            forwards[: node.level] = node.next

        lines.append("None".ljust(label_size) + "* " * len(forwards))
        return f"SkipList(level={self.level})\n" + "\n".join(lines)

    def __iter__(self) -> Iterator[KT]:
        node = self.head
        while len(node.next) != 0:
            yield node.next[0].key  # type: ignore
            node = node.next[0]

    def random_level(self) -> int:
        """
        :return: Random level from [1, self.max_level] interval.
                 Higher values are less likely.
        """
        level = 1
        while random() < self.p and level < self.max_level:
            level += 1
        return level

    def _locate_node(
        self, key: KT
    ) -> Tuple[Optional[SkipListNode[KT, VT]], List[SkipListNode[KT, VT]]]:
        """
        :param key: Searched key,
        :return: Tuple with searched node (or None if given key is not present)
                 and list of nodes that refer (if key is present) of should refer to
                 given node.
        """
        # SkipListNodes with refer or should refer to output node
        update_vector = []
        node = self.head

        for i in reversed(range(self.level)):
            # i < node.level - When node level is lesser than `i` decrement `i`.
            # node.next[i].key < key - Jumping to node with key value higher
            #                             or equal to searched key would result
            #                             in skipping searched key.
            while i < node.level and node.next[i].key < key:  # type: ignore
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
            return node.next[0], update_vector  # type: ignore
        return None, update_vector  # type: ignore

    def delete(self, key: KT) -> None:
        """
        :param key: Key to remove from list.

        >>> skip_list = SkipList()
        >>> skip_list.insert(2, "Two")
        >>> skip_list.insert(1, "One")
        >>> skip_list.insert(3, "Three")
        >>> list(skip_list)
        [1, 2, 3]
        >>> skip_list.delete(2)
        >>> list(skip_list)
        [1, 3]
        """
        node, update_vector = self._locate_node(key)
        if node is not None:
            for i, update_node in enumerate(update_vector):
                # Remove or replace all references to removed node.
                if update_node.level > i and update_node.next[i].key == key:
                    if node.level > i:
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
            for i in range(self.level - 1, level):
                update_vector.append(self.head)  # type: ignore
            self.level = level

        new_node = SkipListNode(key, value)
        for i, update_node in enumerate(update_vector[:level]):
            # Change references to pass through new node.
            if update_node.level > i:
                new_node.next.append(update_node.next[i])
            if update_node.level < i + 1:
                update_node.next.append(new_node)
            else:
                update_node.next[i] = new_node

    def __getitem__(self, key: KT) -> VT:
        node, _ = self._locate_node(key)
        if node is None:
            raise KeyError
        return node.value

    def __contains__(self, key: KT) -> bool:
        """
        :param key: Search key.
        :return: Value associated with given key or None if given key is not present.

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
        if node is None:
            return False
        return True
