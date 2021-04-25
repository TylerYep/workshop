from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID, uuid4

from cs.structures.heap.heap import Heap
from cs.util import Comparable, dfield, formatter

T = TypeVar("T", bound=Comparable)


@dataclass(order=True)
class Entry(Generic[T]):
    """
    Hold an entry in the heap.
    In order for all of the Binomial heap operations to complete in O(1),
    clients need to have O(1) access to any element in the heap. We make
    this work by having each insertion operation produce a handle to the
    node in the tree. In actuality, this handle is the node itself.

    Priority is the first parameter because the dataclass orders Entry as a
    tuple (priority, value)
    """

    priority: float
    value: T
    child: Entry[T] | None = dfield(None, repr=True)
    right: Entry[T] | None = dfield(None, repr=True)

    def __repr__(self) -> str:
        return str(formatter.pformat(self))

    def __len__(self) -> int:
        """
        Recursively calculate length. Since we never use this function except
        in tests, this is simpler than keeping track of each node's size.
        """
        if self.child is None:
            return 1 if self.right is None else len(self.right) + 1
        if self.right is None:
            return len(self.child) + 1
        return len(self.child) + len(self.right) + 1


@dataclass(init=False)
class BinomialHeap(Heap[T]):
    """
    Binomial Heap implementation using a list of trees, represented by Entry objects.

    Note that the input type should be bounded by Comparable in order for the
    implementation to type-check. Otherwise, the heap should still work so long as
    there are no equal priorities. If you want to use a non-comparable type with this
    class, use a wrapper class with a custom comparator or only use unique priorities.
    """

    trees: list[Entry[T] | None]

    def __init__(self, *, allow_duplicates: bool = False) -> None:
        # Trees in ascending order: 1, 2, 4, 8, ..., etc.
        self.trees: list[Entry[T] | None] = []

        # Mapping from element to corresponding entry.
        # Should not introduce any asymptotic change in memory overhead.
        self.elem_to_entry: dict[UUID | T, Entry[T]] = {}

        # Cached size of the heap, so we don't have to recompute this explicitly.
        self.size = 0

        # Whether to allow duplicate key entries, which means using UUIDs for
        # elem_to_entry's keys instead.
        self.allow_duplicates = allow_duplicates

    def __bool__(self) -> bool:
        return bool(self.trees)

    def __len__(self) -> int:
        return self.size

    def __contains__(self, item: T) -> bool:
        if self.allow_duplicates:
            # TODO
            raise NotImplementedError
        return item in self.elem_to_entry

    def __getitem__(self, value: T | UUID) -> Entry[T]:
        """Gets the correct Entry object from the given value or UUID."""
        if self.allow_duplicates and not isinstance(value, UUID):
            raise RuntimeError(
                "You must pass in a valid UUID or set allow_duplicates = False."
            )
        if not self.allow_duplicates and isinstance(value, UUID):
            raise RuntimeError("You must pass in a value of type T, not a UUID.")

        if value not in self.elem_to_entry:
            raise KeyError(
                f"Invalid {'UUID' if self.allow_duplicates else 'key'}: {value}"
            )

        return self.elem_to_entry[value]

    def __or__(self, other: object) -> BinomialHeap[T]:
        # TODO - this is a destructive operation
        if isinstance(other, BinomialHeap):
            result = BinomialHeap[T]()
            self.merge(other)
            result.merge(self)
            return result
        raise NotImplementedError

    def __ior__(self, other: object) -> None:
        if isinstance(other, BinomialHeap):
            self.merge(other)
        raise NotImplementedError

    @staticmethod
    def merge_lists(
        one: list[Entry[T] | None], two: list[Entry[T] | None]
    ) -> list[Entry[T] | None]:
        """
        Merging two binomial heaps is similar to adding two binary numbers. We proceed
        from the "least-significant tree" to the "most-significant tree", merging the
        two trees and storing the result either back in the same slot (if no trees were
        added) or in a carry register to be used in the next computation. This next
        variable declaration contains the carry.

        @param one A reference to one of the two deques.
        @param two A reference to the other of the two deques.
        @return A reference to the smallest element of the resulting list.
        """

        def _merge_trees(one: Entry[T], two: Entry[T]) -> Entry[T]:
            """Merge 2 trees."""
            if two < one:
                one, two = two, one
            two.right = one.child
            one.child = two
            return one

        max_order = max(len(one), len(two))
        lhs = one + [None] * (max_order - len(one))
        rhs = two + [None] * (max_order - len(two))

        result: list[Entry[T] | None] = []
        carry: Entry[T] | None = None
        for order in range(max_order):
            # There are eight possible combinations of the None-ity of the carry,
            # lhs, and rhs trees. To make the logic simpler, we'll add them all to
            # a temporary buffer and proceed from there.
            trees: list[Entry[T]] = []
            if carry is not None:
                trees.append(carry)
            if (left := lhs[order]) is not None:
                trees.append(left)
            if (right := rhs[order]) is not None:
                trees.append(right)

            # Case one: both trees and the carry are None. Then the result of
            # this step is None and the carry should be cleared.
            if not trees:
                result.append(None)
                carry = None
            # Case two: There's exactly one tree. Then the result of this
            # step is that tree and the carry is cleared.
            elif len(trees) == 1:
                result.append(trees[0])
                carry = None
            # Case three: There's exactly two trees. Then the result of this
            # operation is None and the carry will be set to the merge of those trees.
            elif len(trees) == 2:
                result.append(None)
                carry = _merge_trees(trees[0], trees[1])
            # Case four: There's exactly three trees. Then we'll arbitrarily
            # store one of them in the current slot, then put the merge of the
            # other two into the carry.
            else:
                result.append(trees[0])
                carry = _merge_trees(trees[1], trees[2])

        # Finally, if the carry is set, append it to the result.
        if carry is not None:
            result.append(carry)
        return result

    @staticmethod
    def _check_priority(priority: float) -> None:
        """
        Given a user-specified priority, check whether it's a valid double
        and throw a ValueError otherwise.

        @param priority The user's specified priority.
        @raises ValueError if it is not valid.
        """
        if math.isnan(priority):
            raise ValueError(f"Priority {priority} is invalid.")

    def enqueue(self, value: T, priority: float = 0) -> T | UUID:
        """
        Insert an element into the Binomial heap with the specified priority.

        Its priority must be a valid double, so you cannot set the priority to NaN.

        @param value The value to insert.
        @param priority Its priority, which must be valid.
        @return An Entry representing that element in the tree.
        """
        self._check_priority(priority)
        if not self.allow_duplicates and value in self.elem_to_entry:
            raise KeyError(
                f"Duplicate key detected: {value}. "
                "Use allow_duplicates = True to allow duplicate entries using UUIDs."
            )

        # Create the entry object, which is a circularly-linked list of length one.
        result = Entry(priority, value)

        # Merge this singleton list with the tree list.
        self.trees = self.merge_lists(self.trees, [result])
        self.size += 1

        key: T | UUID = uuid4() if self.allow_duplicates else value
        self.elem_to_entry[key] = result
        return key

    def peek(self) -> tuple[T, float]:
        """
        Return an Entry object corresponding to the minimum element of the heap.

        Raise an IndexError if the heap is empty.

        @return The smallest element of the heap.
        @raises IndexError If the heap is empty.
        """
        if not self.trees:
            raise IndexError("Heap is empty.")
        top = min(entry for entry in self.trees if entry is not None)
        return top.value, top.priority

    def dequeue(self) -> tuple[T, float]:
        """
        Dequeue and return the minimum element of the Binomial heap.

        If the heap is empty, this throws an IndexError.

        @return The smallest element of the Binomial heap.
        @raises IndexError if the heap is empty.
        """
        if not self.trees:
            raise IndexError("Heap is empty.")

        result = min(entry for entry in self.trees if entry is not None)
        index = self.trees.index(result)
        children: list[Entry[T] | None] = []
        entry = result.child
        while entry is not None:
            children.append(entry)
            next_ = entry.right
            entry.right = None
            entry = next_
        del self.trees[index]

        # Shrink forest size if we just got rid of the largest tree size.
        if self.trees and self.trees[-1] is None:
            del self.trees[-1]

        # These children were added in reverse order because as they're
        # merged, higher-order trees have lower-order trees as children
        # but the trees are stored in ascending orders in the vectors.
        # Therefore, we need to reverse the list.
        children.reverse()
        self.trees = self.merge_lists(self.trees, children)
        self.size -= 1
        if not self.allow_duplicates:
            del self.elem_to_entry[result.value]
        return result.value, result.priority

    def merge(self, other: Heap[T]) -> None:
        """
        Merge 2 Binomial heaps.

        Given two Binomial heaps, obtain a Binomial heap that contains
        all of the elements of the two heaps in place.

        @param self The first Binomial heap to merge.
        @param other The second Binomial heap to merge.
        """
        if not isinstance(other, BinomialHeap):
            raise TypeError("Heap types must match when merging.")
        if not self.allow_duplicates and set(self.elem_to_entry) & set(
            other.elem_to_entry
        ):
            raise RuntimeError(
                "You must pass in two unoverlapping heaps or set "
                "allow_duplicates = True on both heaps."
            )

        # Clear out the rhs and assign the lhs the value of result.
        self.trees = self.merge_lists(self.trees, other.trees)

        # The size of the new heap is the sum of the sizes of the input heaps.
        self.size += other.size
        self.allow_duplicates = self.allow_duplicates or other.allow_duplicates
        self.elem_to_entry |= other.elem_to_entry
