from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

from cs.util import Comparable

T = TypeVar("T", bound=Comparable)


@dataclass(init=False)
class BinaryHeap(Generic[T]):
    """
    A generic Heap class, represented using an array. We use an array
    rather than a binary tree because heaps grow in a balanced manner, which
    means that the data fits in contiguous memory and no array space is wasted.

    Can be used as min or max heap by passing the according key function.
    """

    _heap: list[T]

    def __init__(self, *, key: Callable[[T], T] = lambda x: x) -> None:
        self._heap = []
        self.elem_to_index: dict[T, int] = {}
        self.size = 0
        self.key = key

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        return bool(self._heap)

    def __contains__(self, item: T) -> bool:
        return item in self.elem_to_index

    def __iter__(self) -> Iterator[T]:
        yield from self._heap

    def __getitem__(self, index: int) -> T:
        if not 0 <= index < self.size:
            raise KeyError(f"Invalid index: {index}")
        return self._heap[index]

    def update(self, item: T, new_item: T) -> None:
        """Updates given item value in heap if present."""
        if item not in self.elem_to_index:
            raise KeyError("Item not found")
        index = self.elem_to_index[item]
        self._heap[index] = new_item
        self.elem_to_index[new_item] = index

        # Make sure heap is right in both up and down direction.
        # Ideally only one of them will make any change.
        self._heapify_up(index)
        self._heapify_down(index)

    def dequeue(self, item: T) -> None:
        """Deletes given item from heap if present."""
        if item not in self.elem_to_index:
            raise KeyError("Item not found")
        index = self.elem_to_index[item]
        del self.elem_to_index[item]
        self._heap[index] = self._heap[self.size - 1]
        self.elem_to_index[self._heap[self.size - 1]] = index
        self.size -= 1
        # Make sure heap is right in both up and down direction. Ideally, only one
        # of them will make any change, so no performance loss in calling both.
        if self.size > index:
            self._heapify_up(index)
            self._heapify_down(index)

    def enqueue(self, item: T) -> None:
        """Inserts given item with given value in heap."""
        new_node = item
        if len(self._heap) == self.size:
            self._heap.append(new_node)
        else:
            self._heap[self.size] = new_node
        self.elem_to_index[item] = self.size
        self.size += 1
        self._heapify_up(self.size - 1)

    def peek(self) -> T:
        """Returns top item tuple (Calculated value, item) from heap if present."""
        if self.size == 0:
            raise ValueError("Heap is empty.")
        return self._heap[0]

    def pop(self) -> T:
        """
        Return top item tuple (Calculated value, item) from heap and removes it as well
        if present.
        """
        top_item = self.peek()
        self.dequeue(top_item)
        return top_item

    def _parent(self, i: int) -> int | None:
        """Returns parent index of given index if exists, else None."""
        return ((i - 1) // 2) if 0 < i < self.size else None

    def _left(self, i: int) -> int | None:
        """Returns left-child-index of given index if exists, else None."""
        left = int(2 * i + 1)
        return left if 0 < left < self.size else None

    def _right(self, i: int) -> int | None:
        """Returns right-child-index of given index if exists, else None."""
        right = int(2 * i + 2)
        return right if 0 < right < self.size else None

    def _swap(self, i: int, j: int) -> None:
        """Performs changes required for swapping two elements in the heap."""
        # First update the indexes of the items in index map.
        self.elem_to_index[self._heap[i]], self.elem_to_index[self._heap[j]] = (
            self.elem_to_index[self._heap[j]],
            self.elem_to_index[self._heap[i]],
        )
        # Then swap the items in the list.
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _cmp(self, i: int, j: int) -> bool:
        """Compares the two items using default comparison."""
        return self.key(self._heap[i]) < self.key(self._heap[j])

    def _get_valid_parent(self, i: int) -> int:
        """
        Returns index of valid parent as per desired ordering among given index and
        both its children.
        """
        left, right = self._left(i), self._right(i)
        valid_parent = i

        if left is not None and not self._cmp(left, valid_parent):
            valid_parent = left
        if right is not None and not self._cmp(right, valid_parent):
            valid_parent = right

        return valid_parent

    def _heapify_up(self, index: int) -> None:
        """Fixes the heap in upward direction of given index."""
        parent = self._parent(index)
        while parent is not None and not self._cmp(index, parent):
            self._swap(index, parent)
            index, parent = parent, self._parent(parent)

    def _heapify_down(self, index: int) -> None:
        """Fixes the heap in downward direction of given index."""
        valid_parent = self._get_valid_parent(index)
        while valid_parent != index:
            self._swap(index, valid_parent)
            index, valid_parent = valid_parent, self._get_valid_parent(valid_parent)
