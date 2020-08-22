from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Generic, List, Optional, TypeVar

from src.algorithms.sort.comparable import Comparable

T = TypeVar("T", bound=Comparable)


@dataclass
class BinaryHeap(Generic[T]):
    """
    A generic Heap class, can be used as min or max by passing the key function
    accordingly.
    """

    def __init__(self, key: Callable[[T], T] = lambda x: x) -> None:
        self.heap: List[T] = []
        # Stores indexes of each item for supporting updates and deletion.
        self.pos_map: Dict[T, int] = {}
        # Stores current size of heap.
        self.size = 0
        # Stores function used to evaluate the score of an item on which basis
        # ordering will be done.
        self.key = key

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        return bool(self.heap)

    # def __contains__(self, v_id: V) -> bool:
    #     return v_id in self.heap

    # def __iter__(self) -> Iterator[V]:
    #     yield from self._graph

    def __repr__(self) -> str:
        return str(self.heap)

    def __getitem__(self, index: int) -> T:
        assert 0 <= index < self.size
        return self.heap[index]

    def _parent(self, i: int) -> Optional[int]:
        """Returns parent index of given index if exists else None"""
        return ((i - 1) // 2) if 0 < i < self.size else None

    def _left(self, i: int) -> Optional[int]:
        """Returns left-child-index of given index if exists else None"""
        left = int(2 * i + 1)
        return left if 0 < left < self.size else None

    def _right(self, i: int) -> Optional[int]:
        """Returns right-child-index of given index if exists else None"""
        right = int(2 * i + 2)
        return right if 0 < right < self.size else None

    def _swap(self, i: int, j: int) -> None:
        """Performs changes required for swapping two elements in the heap"""
        # First update the indexes of the items in index map.
        self.pos_map[self.heap[i]], self.pos_map[self.heap[j]] = (
            self.pos_map[self.heap[j]],
            self.pos_map[self.heap[i]],
        )
        # Then swap the items in the list.
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _cmp(self, i: int, j: int) -> bool:
        """Compares the two items using default comparison"""
        return self.key(self.heap[i]) < self.key(self.heap[j])

    def _get_valid_parent(self, i: int) -> int:
        """
        Returns index of valid parent as per desired ordering among given index and
        both it's children
        """
        left = self._left(i)
        right = self._right(i)
        valid_parent = i

        if left is not None and not self._cmp(left, valid_parent):
            valid_parent = left
        if right is not None and not self._cmp(right, valid_parent):
            valid_parent = right

        return valid_parent

    def _heapify_up(self, index: int) -> None:
        """Fixes the heap in upward direction of given index"""
        parent = self._parent(index)
        while parent is not None and not self._cmp(index, parent):
            self._swap(index, parent)
            index, parent = parent, self._parent(parent)

    def _heapify_down(self, index: int) -> None:
        """Fixes the heap in downward direction of given index"""
        valid_parent = self._get_valid_parent(index)
        while valid_parent != index:
            self._swap(index, valid_parent)
            index, valid_parent = valid_parent, self._get_valid_parent(valid_parent)

    def update(self, item: T, new_item: T) -> None:
        """Updates given item value in heap if present"""
        if item not in self.pos_map:
            raise KeyError("Item not found")
        index = self.pos_map[item]
        self.heap[index] = new_item
        self.pos_map[new_item] = index

        # Make sure heap is right in both up and down direction.
        # Ideally only one of them will make any change.
        self._heapify_up(index)
        self._heapify_down(index)

    def delete(self, item: T) -> None:
        """Deletes given item from heap if present"""
        if item not in self.pos_map:
            raise KeyError("Item not found")
        index = self.pos_map[item]
        del self.pos_map[item]
        self.heap[index] = self.heap[self.size - 1]
        self.pos_map[self.heap[self.size - 1]] = index
        self.size -= 1
        # Make sure heap is right in both up and down direction. Ideally, only one
        # of them will make any change, so no performance loss in calling both.
        if self.size > index:
            self._heapify_up(index)
            self._heapify_down(index)

    def insert(self, item: T) -> None:
        """Inserts given item with given value in heap"""
        new_node = item
        if len(self.heap) == self.size:
            self.heap.append(new_node)
        else:
            self.heap[self.size] = new_node
        self.pos_map[item] = self.size
        self.size += 1
        self._heapify_up(self.size - 1)

    def get_top(self) -> T:
        """Returns top item tuple (Calculated value, item) from heap if present"""
        if self.size == 0:
            raise ValueError("Heap is empty.")
        return self.heap[0]

    def extract_top(self) -> T:
        """
        Return top item tuple (Calculated value, item) from heap and removes it as well
        if present
        """
        top_item = self.get_top()
        self.delete(top_item)
        return top_item
