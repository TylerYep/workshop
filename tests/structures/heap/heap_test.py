import random
from typing import TypeVar, cast

import pytest

from src.structures import BinomialHeap, FibonacciHeap, Heap

T = TypeVar("T")
HEAP_TYPES = ("BinomialHeap", "FibonacciHeap")


def construct_heap(heap_type: str, allow_duplicates: bool = False) -> Heap[T]:
    heap_map = {
        heap_constructor.__name__: heap_constructor
        for heap_constructor in (BinomialHeap, FibonacciHeap)
    }
    return cast(Heap[T], heap_map[heap_type](allow_duplicates=allow_duplicates))


class TestHeap:
    @staticmethod
    @pytest.mark.parametrize("heap_type", HEAP_TYPES)
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_enqueue_100(heap_type: str, allow_duplicates: bool) -> None:
        """ Test creating a heap and adding 100 values to it. """
        fib_heap: Heap[int] = construct_heap(heap_type, allow_duplicates)
        for i in range(100):
            random_value = random.randrange(100) if allow_duplicates else i
            random_priority = random.randrange(100)
            fib_heap.enqueue(random_value, random_priority)

    @staticmethod
    @pytest.mark.parametrize("heap_type", HEAP_TYPES)
    def test_get_min_of_1(heap_type: str) -> None:
        """ Test creating a heap, adding a single value, and retrieving it. """
        fib_heap: Heap[int] = construct_heap(heap_type)
        fib_heap.enqueue(1, 1)

        assert fib_heap.peek().value == 1

    @staticmethod
    @pytest.mark.parametrize("heap_type", HEAP_TYPES)
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_get_min_of_3(heap_type: str, allow_duplicates: bool) -> None:
        """
        Test creating a heap, adding 3 values, and retrieving
        the minimum-priority entry.
        """
        fib_heap: Heap[int] = construct_heap(heap_type, allow_duplicates)
        fib_heap.enqueue(1, 1)
        fib_heap.enqueue(10, 0)
        fib_heap.enqueue(20, 100)

        assert fib_heap.peek().value == 10

    @staticmethod
    @pytest.mark.parametrize("heap_type", HEAP_TYPES)
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_get_min_of_3_float(heap_type: str, allow_duplicates: bool) -> None:
        """
        Test creating a heap, adding 3 values, and
        retrieving the minimum-float-priority entry.
        """
        fib_heap: Heap[int] = construct_heap(heap_type, allow_duplicates)
        fib_heap.enqueue(10, 1.1)
        fib_heap.enqueue(100, 1.0)
        fib_heap.enqueue(20, 1.2)

        assert fib_heap.peek().value == 100

    # @staticmethod
    # @pytest.mark.parametrize("heap_type", HEAP_TYPES)
    # @pytest.mark.parametrize("entries", ((3,), (4, 2), (2, 7, 1, 8, 3, 1, 4)))
    # def test_enqueue_dequeue_no_priority(heap_type: str, entries: Tuple[int]) -> None:
    #     h: Heap[int] = construct_heap(heap_type, allow_duplicates=True)
    #     for i in entries:
    #         h.enqueue(i)

    #     for i, item in enumerate(sorted(entries)):
    #         assert len(h) == len(entries) - i
    #         val, _ = h.dequeue()
    #         assert val == item

    @staticmethod
    @pytest.mark.parametrize("heap_type", HEAP_TYPES)
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_empty(heap_type: str, allow_duplicates: bool) -> None:
        """ Test an empty heap to see if it's Falsy. """
        assert bool(construct_heap(heap_type, allow_duplicates)) is False

        fib_heap: Heap[int] = construct_heap(heap_type, allow_duplicates)
        fib_heap.enqueue(1, 1)
        assert bool(fib_heap) is True

    @staticmethod
    @pytest.mark.parametrize("heap_type", HEAP_TYPES)
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_len(heap_type: str, allow_duplicates: bool) -> None:
        """
        Test creating a heap, adding "intended_length" values, and checking
        for correct length.
        """
        for intended_length in (0, 1, 3, 100):
            fib_heap: Heap[int] = construct_heap(heap_type, allow_duplicates)
            for i in range(intended_length):
                random_value = (
                    random.randrange(intended_length) if allow_duplicates else i
                )
                random_priority = random.randrange(intended_length)
                fib_heap.enqueue(random_value, random_priority)

            assert len(fib_heap) == intended_length

    @staticmethod
    @pytest.mark.parametrize("heap_type", HEAP_TYPES)
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_dequeue(heap_type: str, allow_duplicates: bool) -> None:
        """
        Test creating a heap, adding "intended_length" values,
        and checking for correct dequeue values.
        """
        for intended_length in (0, 1, 2, 3, 10, 100):
            fib_heap: Heap[int] = construct_heap(heap_type, allow_duplicates)
            # random.seed(0) gives too-consistent priorities
            random.seed(1)
            expected_priorities_list = []
            for i in range(intended_length):
                random_value = (
                    random.randrange(intended_length) if allow_duplicates else i
                )
                random_priority = random.randrange(intended_length)
                fib_heap.enqueue(random_value, random_priority)
                expected_priorities_list.append(random_priority)
            expected_priorities_list.sort()

            assert len(fib_heap) == intended_length
            actual_priorities_list = []
            for _ in range(intended_length):
                _, priority = fib_heap.dequeue()
                actual_priorities_list.append(priority)

            with pytest.raises(IndexError):
                _ = fib_heap.dequeue()

            # We can't just compare lists, because this is basically a heapsort,
            # which isn't stable. So instead we compare all the priorities
            assert expected_priorities_list == actual_priorities_list

    @staticmethod
    @pytest.mark.parametrize("heap_type", HEAP_TYPES)
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_dequeue_sort(heap_type: str, allow_duplicates: bool) -> None:
        """
        Test creating a heap, adding "intended_length" values, and
        checking for correct dequeue values.

        Does not use duplicate vales or priorities.
        """
        for intended_length in (0, 1, 2, 3, 10, 100):
            fib_heap: Heap[int] = construct_heap(heap_type, allow_duplicates)
            # random.seed(0) gives too-consistent priorities
            random.seed(1)
            random_values = range(intended_length)
            random_priorities = range(intended_length)
            tuples = list(zip(random_priorities, random_values))
            random.shuffle(tuples)

            for tuple_ in tuples:
                fib_heap.enqueue(*tuple_)
            expected_list = tuples[:]
            expected_list.sort()

            assert len(fib_heap) == intended_length
            actual_list = [fib_heap.dequeue() for _ in range(intended_length)]

            # We can just compare lists, because although this is basically a heapsort,
            # which isn't stable, we have no duplicate priorities or duplicate values,
            # so the instability doesn't matter.
            assert expected_list == actual_list

    @staticmethod
    @pytest.mark.parametrize("heap_type", HEAP_TYPES)
    def test_merge_duplicates(heap_type: str) -> None:
        """ Test merging two heaps. """
        heap1: Heap[int] = construct_heap(heap_type, allow_duplicates=True)
        heap2: Heap[int] = construct_heap(heap_type)
        heap1.enqueue(1, 1)
        heap1.enqueue(3, 3)
        heap1.enqueue(5, 5)

        heap2.enqueue(2, 2)
        heap2.enqueue(3, 3)
        heap2.enqueue(4, 4)
        heap2.enqueue(6, 6)

        heap1.merge(heap2)

        assert len(heap1) == 7
        assert len(heap2) == 4

        actual_list = []
        while heap1:
            actual_list.append(heap1.dequeue())

        assert actual_list == [(1, 1), (2, 2), (3, 3), (3, 3), (4, 4), (5, 5), (6, 6)]

    @staticmethod
    @pytest.mark.parametrize("heap_type", HEAP_TYPES)
    def test_merge(heap_type: str) -> None:
        """ Test merging two heaps. """
        heap1: Heap[int] = construct_heap(heap_type)
        heap2: Heap[int] = construct_heap(heap_type)
        heap1.enqueue(1, 1)
        heap1.enqueue(3, 3)
        heap1.enqueue(5, 5)

        heap2.enqueue(2, 2)
        heap2.enqueue(4, 4)
        heap2.enqueue(6, 6)

        heap1.merge(heap2)

        assert len(heap1) == 6
        assert len(heap2) == 3

        actual_list = []
        while heap1:
            actual_list.append(heap1.dequeue())

        assert actual_list == [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]

    @staticmethod
    @pytest.mark.parametrize("heap_type", HEAP_TYPES)
    def test_merge_exception(heap_type: str) -> None:
        """ Test merging two heaps. """
        heap1: Heap[int] = construct_heap(heap_type)
        heap2: Heap[int] = construct_heap(heap_type)
        heap1.enqueue(1, 1)
        heap1.enqueue(3, 3)
        heap1.enqueue(5, 5)

        heap2.enqueue(2, 2)
        heap2.enqueue(3, 3)
        heap2.enqueue(4, 4)

        with pytest.raises(RuntimeError):
            heap1.merge(heap2)

    @staticmethod
    @pytest.mark.parametrize("heap_type", HEAP_TYPES)
    def test_print_heap(heap_type: str) -> None:
        heap: Heap[int] = construct_heap(heap_type)
        heap.enqueue(1, 1)
        heap.enqueue(3, 3)
        heap.enqueue(5, 2)
        heap.enqueue(2, 2)
        heap.enqueue(4, 4)
        heap.enqueue(6, 8)
        heap.dequeue()
        if isinstance(heap, FibonacciHeap):
            assert str(heap) == "FibonacciHeap(top=Entry(priority=2, value=5))"
        elif isinstance(heap, BinomialHeap):
            assert str(heap) == (
                "BinomialHeap(trees=[Entry(priority=3, value=3), None, Entry(\n"
                "    priority=2,\n"
                "    value=5,\n"
                "    child=Entry(\n"
                "        priority=4,\n"
                "        value=4,\n"
                "        child=Entry(priority=8, value=6),\n"
                "        right=Entry(priority=2, value=2)\n"
                "    )\n"
                ")])"
            )
