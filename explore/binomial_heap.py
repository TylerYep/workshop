# # pylint: disable=too-many-branches
# from __future__ import annotations

# import collections
# import math
# from dataclasses import dataclass, field
# from typing import Deque, Dict, Generic, List, Optional, Tuple, TypeVar, Union
# from uuid import UUID, uuid4

# from src.util import formatter

# T = TypeVar("T")


# @dataclass(order=True)
# class Entry(Generic[T]):
#     """
#     Hold an entry in the heap.
#     In order for all of the Binomial heap operations to complete in O(1),
#     clients need to have O(1) access to any element in the heap. We make
#     this work by having each insertion operation produce a handle to the
#     node in the tree. In actuality, this handle is the node itself.

#     Priority is the first parameter because the dataclass orders Entry as a
#     tuple (priority, value)
#     """

#     priority: float
#     value: T = field(compare=False)

#     def __post_init__(self) -> None:
#         """ Initialize an Entry in the heap. """
#         self.child: Optional[Entry[T]] = None
#         self.right = None

#     def __repr__(self) -> str:
#         return str(formatter.pformat(self))


# @dataclass(init=False)
# class BinomialHeap(Generic[T]):
#     """
#     See docs/binomial_heap.md for code credits and implementation details.
#     Author: Keith Schwarz (htiek@cs.stanford.edu)
#     """

#     trees: List[Entry[T]]

#     def __init__(self, *, allow_duplicates: bool = False) -> None:
#         # List of all the trees, by order. If there is no tree of the given
#         # order, there will be a None element in the vector.
#         self.trees: List[Optional[Entry[T]]] = []

#         # Mapping from element to corresponding entry.
#         # Should not introduce any additional memory overhead.
#         self.elem_to_entry: Dict[Union[UUID, T], Entry[T]] = {}

#         # Cached size of the heap, so we don't have to recompute this explicitly.
#         self.size = 0

#         # Whether to allow duplicate key entries, which means using UUIDs for
#         # elem_to_entry's keys instead.
#         self.allow_duplicates = allow_duplicates

#     def __bool__(self) -> bool:
#         return bool(self.trees)

#     def __len__(self) -> int:
#         return self.size

#     def __contains__(self, item: T) -> bool:
#         if self.allow_duplicates:
#             # TODO
#             raise NotImplementedError
#         return item in self.elem_to_entry

#     def __getitem__(self, value: Union[T, UUID]) -> Entry[T]:
#         """ Gets the correct Entry object from the given value or UUID. """
#         if self.allow_duplicates and not isinstance(value, UUID):
#             raise RuntimeError(
#                 "You must pass in a valid UUID or set allow_duplicates = False."
#             )
#         if not self.allow_duplicates and isinstance(value, UUID):
#             raise RuntimeError("You must pass in a value of type T, not a UUID.")

#         if value not in self.elem_to_entry:
#             raise KeyError(
#                 f"Invalid {'UUID' if self.allow_duplicates else 'key'}: {value}"
#             )

#         return self.elem_to_entry[value]

#     @staticmethod
#     def merge_lists(
#         one: List[Optional[Entry[T]]], two: List[Optional[Entry[T]]]
#     ) -> List[Optional[Entry[T]]]:
#         """
#         Merge 2 lists.

#         Utility function which, given two pointers into disjoint circularly-
#         linked lists, merges the two lists together into one circularly-linked
#         list in O(1) time. Because the lists may be empty, the return value
#         is the only pointer that's guaranteed to be to an element of the
#         resulting list.

#         This function assumes that one and two are the minimum elements of the
#         lists they are in, and returns a pointer to whichever is smaller. If
#         this condition does not hold, the return value is some arbitrary pointer
#         into the doubly-linked list.

#         @param one A reference to one of the two deques.
#         @param two A reference to the other of the two deques.
#         @return A reference to the smallest element of the resulting list.
#         """
#         raise NotImplementedError

#     @staticmethod
#     def _check_priority(priority: float) -> None:
#         """
#         Given a user-specified priority, check whether it's a valid double
#         and throw a ValueError otherwise.

#         @param priority The user's specified priority.
#         @raises ValueError if it is not valid.
#         """
#         if math.isnan(priority):
#             raise ValueError(f"Priority {priority} is invalid.")

#     def enqueue(self, value: T, priority: float = 0) -> Union[T, UUID]:
#         """
#         Insert an element into the Binomial heap with the specified priority.

#         Its priority must be a valid double, so you cannot set the priority to NaN.

#         @param value The value to insert.
#         @param priority Its priority, which must be valid.
#         @return An Entry representing that element in the tree.
#         """
#         self._check_priority(priority)
#         if not self.allow_duplicates and value in self.elem_to_entry:
#             raise KeyError(
#                 f"Duplicate key detected: {value}. "
#                 f"Use allow_duplicates = True to allow duplicate entries using UUIDs."
#             )

#         # Create the entry object, which is a circularly-linked list of length one.
#         result = Entry(priority, value)

#         # Merge this singleton list with the tree list.
#         self.top = self.merge_lists(self.top, result)
#         self.size += 1

#         key: Union[T, UUID] = uuid4() if self.allow_duplicates else value
#         self.elem_to_entry[key] = result
#         return key

#     def min(self) -> Entry[T]:
#         """
#         Return an Entry object corresponding to the minimum element of the heap.

#         Raise an IndexError if the heap is empty.

#         @return The smallest element of the heap.
#         @raises IndexError If the heap is empty.
#         """
#         if self.top is None:
#             raise IndexError("Heap is empty.")
#         return self.top

#     def dequeue(self) -> Tuple[T, float]:
#         """
#         Dequeue and return the minimum element of the Binomial heap.

#         If the heap is empty, this throws an IndexError.

#         @return The smallest element of the Binomial heap.
#         @raises IndexError if the heap is empty.
#         """
#         raise NotImplementedError

#     def decrease_key(self, value: Union[T, UUID], new_priority: float) -> None:
#         """
#         Decrease the key of the specified element to the new priority.

#         If the new priority is greater than the old priority, this function raises an
#         ValueError. The new priority must be a finite double, so you cannot set the
#         priority to be NaN, or +/- infinity. Doing so also raises an ValueError.

#         @param entry The element whose priority should be decreased.
#         @param new_priority The new priority to associate with this entry.
#         @raises ValueError If the new priority exceeds the old
#                 priority, or if the argument is not a finite double.
#         """
#         entry = self[value]
#         self._check_priority(new_priority)
#         if new_priority > entry.priority:
#             raise ValueError("New priority exceeds old.")

#         # Forward this to a helper function.
#         self._decrease_key_unchecked(entry, new_priority)

#     def delete(self, value: Union[T, UUID]) -> None:
#         """
#         Delete this Entry from the Binomial heap that contains it.

#         @param entry The entry to delete.
#         """
#         # Use decreaseKey to drop the entry's key to -infinity. This will
#         # guarantee that the node is cut and set to the global minimum.
#         self._decrease_key_unchecked(self[value], float("-inf"))
#         self.dequeue()

#     def merge(self, other: BinomialHeap[T]) -> BinomialHeap[T]:
#         """
#         Merge 2 Binomial heaps.

#         Given two Binomial heaps, returns a new Binomial heap that contains
#         all of the elements of the two heaps. Each of the input heaps is
#         destructively modified by having all its elements removed. You can
#         continue to use those heaps, but be aware that they will be empty
#         after this call completes.

#         @param self The first Binomial heap to merge.
#         @param other The second Binomial heap to merge.
#         @return A new BinomialHeap containing all of the elements of both heaps.
#         """
#         # Create a new BinomialHeap to hold the result.
#         result = BinomialHeap[T]()

#         # Merge the two Binomial heap root lists together. This helper function
#         # also computes the min of the two lists, so we can store the result in
#         # the top field of the new heap.
#         result.top = self.merge_lists(self.top, other.top)

#         # The size of the new heap is the sum of the sizes of the input heaps.
#         result.size = self.size + other.size
#         result.allow_duplicates = self.allow_duplicates or other.allow_duplicates
#         if set(self.elem_to_entry) & set(other.elem_to_entry):
#             raise RuntimeError(
#                 "You must pass in two unoverlapping heaps or set "
#                 "allow_duplicates = True on both heaps."
#             )

#         # TODO: Python 3.9
#         # result.elem_to_entry = self.elem_to_entry | other.elem_to_entry
#         result.elem_to_entry = {**self.elem_to_entry, **other.elem_to_entry}

#         # Clear the old heaps.
#         self.size = other.size = 0
#         self.top = other.top = None
#         return result

#     def _decrease_key_unchecked(self, entry: Entry[T], priority: float) -> None:
#         """
#         Decrease the key of a node in the tree without doing any checking to ensure
#         that the new priority is valid.

#         @param entry The node whose key should be decreased.
#         @param priority The node's new priority.
#         """
#         raise NotImplementedError
