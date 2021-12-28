# pylint: disable=too-many-branches
from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID, uuid4

from cs.structures.heap.heap import Heap
from cs.util import Comparable, formatter

T = TypeVar("T", bound=Comparable)


@dataclass(order=True)
class Entry(Generic[T]):
    """
    Hold an entry in the heap.
    In order for all of the Fibonacci heap operations to complete in O(1), clients need
    to have O(1) access to any element in the heap. We make this work by having each
    insertion operation produce a handle to the node in the tree. In actuality, this
    handle is the node itself.

    Priority is the first parameter because the dataclass orders Entry as a tuple
    (priority, value).

    Note that the input type should be bounded by Comparable in order for the
    implementation to type-check. Otherwise, the heap should still work so long as there
    are no equal priorities. If you want to use a non-comparable type with this class,
    use a wrapper class with a custom comparator or only use unique priorities.
    """

    priority: float
    value: T

    def __post_init__(self) -> None:
        """Initialize an Entry in the heap."""
        # Number of children
        self.degree = 0
        self.is_marked = False
        self.parent: Entry[T] | None = None
        self.child: Entry[T] | None = None
        self.next = self.prev = self

    def __repr__(self) -> str:
        return str(formatter.pformat(self))


@dataclass(init=False)
class FibonacciHeap(Heap[T]):
    """See docs/fibonacci_heap.md for code credits and implementation details."""

    top: Entry[T] | None

    def __init__(self, *, allow_duplicates: bool = False) -> None:
        # Pointer to the minimum element in the heap.
        self.top: Entry[T] | None = None

        # Mapping from element to corresponding entry.
        # Should not introduce any asymptotic change in memory overhead.
        self.elem_to_entry: dict[T | UUID, Entry[T]] = {}

        # Cached size of the heap, so we don't have to recompute this explicitly.
        self.size = 0

        # Whether to allow duplicate key entries, which means using UUIDs for
        # elem_to_entry's keys instead.
        self.allow_duplicates = allow_duplicates

    def __bool__(self) -> bool:
        return self.top is not None

    def __len__(self) -> int:
        return self.size

    def __contains__(self, item: T) -> bool:
        if self.allow_duplicates:
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

    def __or__(self, other: object) -> FibonacciHeap[T]:
        # TODO - this is a destructive operation
        if isinstance(other, FibonacciHeap):
            result = FibonacciHeap[T]()
            self.merge(other)
            result.merge(self)
            return result
        raise NotImplementedError

    def __ior__(self, other: object) -> None:
        if isinstance(other, FibonacciHeap):
            self.merge(other)
        raise NotImplementedError

    @staticmethod
    def merge_lists(one: Entry[T] | None, two: Entry[T] | None) -> Entry[T] | None:
        """
        Merge 2 lists.

        Utility function which, given two pointers into disjoint circularly- linked
        lists, merges the two lists together into one circularly-linked list in O(1)
        time. Because the lists may be empty, the return value is the only pointer
        that's guaranteed to be to an element of the resulting list.

        This function assumes one and two are the minimum elements of the lists they are
        in, and returns a pointer to whichever is smaller. If this condition does not
        hold, the return value is some arbitrary pointer into the doubly-linked list.

        @param one A reference to one of the two deques.
        @param two A reference to the other of the two deques.
        @return A reference to the smallest element of the resulting list.
        """
        if one is None:
            return two or None

        if two is None:
            return one or None

        # Both non-None; actually do the splice.
        # We have two lists that look like this and we want to switch A and B.
        # +----+     +----+     +----+
        # |    |--N->|one |--N->|  A |
        # |    |<-P--|    |<-P--|    |
        # +----+     +----+     +----+
        #
        # +----+     +----+     +----+
        # |    |--N->|two |--N->|  B |
        # |    |<-P--|    |<-P--|    |
        # +----+     +----+     +----+
        one.next, two.next = two.next, one.next
        one.next.prev, two.next.prev = one, two
        return one if one < two else two

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
        Insert an element into the Fibonacci heap with the specified priority.

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
        self.top = self.merge_lists(self.top, result)
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
        if self.top is None:
            raise IndexError("Heap is empty.")
        top = self.top
        return top.value, top.priority

    def dequeue(self) -> tuple[T, float]:
        """
        Dequeue and return the minimum element of the Fibonacci heap.

        If the heap is empty, this throws an IndexError.

        @return The smallest element of the Fibonacci heap.
        @raises IndexError if the heap is empty.
        """
        if self.top is None:
            raise IndexError("Heap is empty.")

        # Otherwise, we're about to lose an element, so decrement the number of
        # entries in this heap.
        self.size -= 1

        # Grab the minimum element so we know what to return.
        min_elem = self.top
        return_val = (min_elem.value, min_elem.priority)

        # Now, we need to get rid of this element from the list of roots. There
        # are two cases to consider. First, if this is the only element in the
        # list of roots, we set the list of roots to be None by clearing top.
        # Otherwise, if it's not None, then we write the elements next to the
        # min element around the min element to remove it, then arbitrarily
        # reassign the min.
        if self.top.next is self.top:
            self.top = None
        else:
            self.top.prev.next = self.top.next
            self.top.next.prev = self.top.prev
            # Arbitrary element of the root list.
            self.top = self.top.next

        # Next, clear the parent fields of all of the min element's children,
        # since they're about to become roots. Because the elements are
        # stored in a circular list, the traversal is a bit complex.
        if min_elem.child is not None:
            # Keep track of the first visited node.
            curr = min_elem.child
            while True:
                curr.parent = None

                # Walk to the next node, then stop if this is the node we
                # started at.
                curr = curr.next
                if curr is min_elem.child:
                    # This was a do-while (curr != minElem.mChild);
                    break

        # Next, splice the children of the root node into the topmost list,
        # then set self.top to point somewhere in that list.
        self.top = self.merge_lists(self.top, min_elem.child)

        # If there are no entries left, we're done.
        if self.top is None:
            if not self.allow_duplicates:
                del self.elem_to_entry[min_elem.value]
            return return_val

        # Next, we need to coalesce all of the roots so that there is only one
        # tree of each degree. To track trees of each size, we allocate an
        # ArrayList where the entry at position i is either None or the
        # unique tree of degree i.
        tree_table: deque[Entry[T] | None] = deque()

        # We need to traverse the entire list, but since we're going to be
        # messing around with it we have to be careful not to break our
        # traversal order mid-stream. One major challenge is how to detect
        # whether we're visiting the same node twice. To do this, we'll
        # spent a bit of overhead adding all of the nodes to a list, and
        # then will visit each element of this list in order.
        to_visit: deque[Entry[T]] = deque()

        # To add everything, we'll iterate across the elements until we
        # find the first element twice. We check this by looping while the
        # list is empty or while the current element isn't the first element
        # of that list.

        curr = self.top
        while not to_visit or to_visit[0] is not curr:
            to_visit.append(curr)
            curr = curr.next

        # Traverse this list and perform the appropriate unioning steps.
        for curr in to_visit:
            # Keep merging until a match arises.
            while True:
                # Ensure that the list is long enough to hold an element of this degree.
                while curr.degree >= len(tree_table):
                    tree_table.append(None)

                # If nothing's here, we can record that this tree has this size
                # and are done processing.
                if tree_table[curr.degree] is None:
                    tree_table[curr.degree] = curr
                    break

                # Otherwise, merge with what's there.
                other = tree_table[curr.degree]
                if other is None:
                    raise RuntimeError

                # Clear the slot
                tree_table[curr.degree] = None

                # Determine which of the two trees has the smaller root, storing
                # the two trees accordingly.
                minimum = other if other < curr else curr
                maximum = curr if other < curr else other

                # Break max out of the root list, then merge it into min's child list.
                maximum.next.prev = maximum.prev
                maximum.prev.next = maximum.next

                # Make it a singleton so that we can merge it.
                maximum.next = maximum.prev = maximum
                minimum.child = self.merge_lists(minimum.child, maximum)

                # Reparent maximum appropriately.
                maximum.parent = minimum

                # Clear maximum's mark, since it can now lose another child.
                maximum.is_marked = False

                # Increase minimum's degree; it now has another child.
                minimum.degree += 1

                # Continue merging this tree.
                curr = minimum

            # Update the global min based on this node. Note that we compare
            # for <= instead of < here. That's because if we just did a
            # reparent operation that merged two different trees of equal
            # priority, we need to make sure that the min pointer points to
            # the root-level one.
            if curr <= self.top:
                self.top = curr
        if not self.allow_duplicates:
            del self.elem_to_entry[min_elem.value]
        return return_val

    def decrease_key(self, value: T | UUID, new_priority: float) -> None:
        """
        Decrease the key of the specified element to the new priority.

        If the new priority is greater than the old priority, this function raises an
        ValueError. The new priority must be a finite double, so you cannot set the
        priority to be NaN, or +/- infinity. Doing so also raises an ValueError.

        @param entry The element whose priority should be decreased.
        @param new_priority The new priority to associate with this entry.
        @raises ValueError If the new priority exceeds the old
                priority, or if the argument is not a finite double.
        """
        entry = self[value]
        self._check_priority(new_priority)
        if new_priority > entry.priority:
            raise ValueError("New priority exceeds old.")
        self._decrease_key_unchecked(entry, new_priority)

    def remove(self, value: T | UUID) -> None:
        """
        Remove this Entry from the Fibonacci heap that contains it.

        @param entry The entry to delete.
        """
        # Use decreaseKey to drop the entry's key to -infinity. This will
        # guarantee that the node is cut and set to the global minimum.
        self._decrease_key_unchecked(self[value], float("-inf"))
        self.dequeue()

    def merge(self, other: Heap[T]) -> None:
        """
        Merge 2 Fibonacci heaps.

        Given two Fibonacci heaps, obtain a Fibonacci heap that contains
        all of the elements of the two heaps in place.

        @param self The first Fibonacci heap to merge.
        @param other The second Fibonacci heap to merge.
        """
        if not isinstance(other, FibonacciHeap):
            raise TypeError("Heap types must match when merging.")

        if not self.allow_duplicates and set(self.elem_to_entry) & set(
            other.elem_to_entry
        ):
            raise RuntimeError(
                "You must pass in two unoverlapping heaps or set "
                "allow_duplicates = True on both heaps."
            )

        # Merge the two Fibonacci heap root lists together. This helper function
        # also computes the min of the two lists, so we can store the result in
        # the top field of the new heap.
        self.top = self.merge_lists(self.top, other.top)

        # The size of the new heap is the sum of the sizes of the input heaps.
        self.size += other.size
        self.allow_duplicates = self.allow_duplicates or other.allow_duplicates
        self.elem_to_entry |= other.elem_to_entry

    def _decrease_key_unchecked(self, entry: Entry[T], priority: float) -> None:
        """
        Decrease the key of a node in the tree without doing any checking to ensure
        that the new priority is valid.

        @param entry The node whose key should be decreased.
        @param priority The node's new priority.
        """
        # First, change the node's priority.
        entry.priority = priority

        # If the node no longer has a higher priority than its parent, cut it.
        # Note that this also means that if we try to run a delete operation
        # that decreases the key to -infinity, it's guaranteed to cut the node
        # from its parent.
        if entry.parent is not None and entry <= entry.parent:
            self._cut_node(entry)

        # If our new value is the new min, mark it as such. Note that if we
        # ended up decreasing the key in a way that ties the current minimum
        # priority, this will change the min accordingly.
        if self.top is not None and entry <= self.top:
            self.top = entry

    def _cut_node(self, entry: Entry[T]) -> None:
        """
        Cut a node from its parent.

        If the parent was already marked, recursively cuts that node from its
        parent as well.

        @param entry The node to cut from its parent.
        """
        # Begin by clearing the node's mark, since we just cut it.
        entry.is_marked = False

        # Base case: If the node has no parent, we're done.
        if entry.parent is None:
            return

        # Rewire the node's siblings around it, if it has any siblings.
        if entry.next is not entry:
            # Has siblings
            entry.next.prev = entry.prev
            entry.prev.next = entry.next

        # If the node is the one identified by its parent as its child,
        # we need to rewrite that pointer to point to some arbitrary other child.
        if entry.parent.child is entry:
            # If there are any other children, pick one of them arbitrarily.
            # Otherwise, there aren't any children left and we should clear the
            # pointer and drop the node's degree.
            entry.parent.child = None if entry.next is entry else entry.next

        # Decrease the degree of the parent, since it just lost a child.
        entry.parent.degree -= 1

        # Splice this tree into the root list by converting it to a singleton
        # and invoking the merge subroutine.
        entry.prev = entry.next = entry
        self.top = self.merge_lists(self.top, entry)

        # Mark the parent and recursively cut it if it's already been
        # marked.
        if entry.parent.is_marked:
            self._cut_node(entry.parent)
        else:
            entry.parent.is_marked = True

        # Clear the relocated node's parent; it's now a root.
        entry.parent = None
