import random

import pytest

from src.structures import BinomialHeap


class TestBinomialHeap:
    @staticmethod
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_enqueue_100(allow_duplicates: bool) -> None:
        """ Test creating a Binomial heap and adding 100 values to it. """
        fib_heap = BinomialHeap[int](allow_duplicates=allow_duplicates)
        for i in range(100):
            random_value = random.randrange(100) if allow_duplicates else i
            random_priority = random.randrange(100)
            fib_heap.enqueue(random_value, random_priority)

    @staticmethod
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_get_min_of_1(allow_duplicates: bool) -> None:
        """
        Test creating a Binomial heap, adding a single value to it, and retrieving it.
        """
        fib_heap = BinomialHeap[int](allow_duplicates=allow_duplicates)
        fib_heap.enqueue(1, 1)

        assert fib_heap.peek().value == 1

    @staticmethod
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_get_min_of_3(allow_duplicates: bool) -> None:
        """
        Test creating a Binomial heap, adding 3 values, and retrieving
        the minimum-priority entry.
        """
        fib_heap = BinomialHeap[int](allow_duplicates=allow_duplicates)
        fib_heap = BinomialHeap[int]()
        fib_heap.enqueue(1, 1)
        fib_heap.enqueue(10, 0)
        fib_heap.enqueue(20, 100)

        assert fib_heap.peek().value == 10

    @staticmethod
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_get_min_of_3_float(allow_duplicates: bool) -> None:
        """
        Test creating a Binomial heap, adding 3 values, and
        retrieving the minimum-float-priority entry.
        """
        fib_heap = BinomialHeap[int](allow_duplicates=allow_duplicates)
        fib_heap.enqueue(10, 1.1)
        fib_heap.enqueue(100, 1.0)
        fib_heap.enqueue(20, 1.2)

        assert fib_heap.peek().value == 100

    @staticmethod
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_empty(allow_duplicates: bool) -> None:
        """ Test an empty heap to see if it's Falsy. """
        assert bool(BinomialHeap[int](allow_duplicates=allow_duplicates)) is False

    @staticmethod
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_nonempty(allow_duplicates: bool) -> None:
        """ Test creating a Binomial, adding a value, and checking if it's truthy. """
        fib_heap = BinomialHeap[int](allow_duplicates=allow_duplicates)
        fib_heap.enqueue(1, 1)
        assert bool(fib_heap) is True

    @staticmethod
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_len(allow_duplicates: bool) -> None:
        """
        Test creating a Binomial heap, adding "intended_length" values, and checking
        for correct length.
        """
        for intended_length in (0, 1, 3, 100):
            fib_heap = BinomialHeap[int](allow_duplicates=allow_duplicates)
            for i in range(intended_length):
                random_value = (
                    random.randrange(intended_length) if allow_duplicates else i
                )
                random_priority = random.randrange(intended_length)
                fib_heap.enqueue(random_value, random_priority)

            assert len(fib_heap) == intended_length

    @staticmethod
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_dequeue(allow_duplicates: bool) -> None:
        """
        Test creating a Binomial heap, adding "intended_length" values,
        and checking for correct dequeue values.
        """
        for intended_length in (10,):  # (0, 1, 2, 3, 10, 100):
            fib_heap = BinomialHeap[int](allow_duplicates=allow_duplicates)
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
    @pytest.mark.parametrize("allow_duplicates", (True, False))
    def test_dequeue_sort(allow_duplicates: bool) -> None:
        """
        Test creating a Binomial heap, adding "intended_length" values, and
        checking for correct dequeue values.

        Does not use duplicate vales or priorities.
        """
        for intended_length in (0, 1, 2, 3, 10, 100):
            fib_heap = BinomialHeap[int](allow_duplicates=allow_duplicates)
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
    def test_merge_duplicates() -> None:
        """ Test merging two heaps. """
        heap1 = BinomialHeap[int](allow_duplicates=True)
        heap2 = BinomialHeap[int]()
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
    def test_merge() -> None:
        """ Test merging two heaps. """
        heap1 = BinomialHeap[int](allow_duplicates=False)
        heap2 = BinomialHeap[int]()
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
    def test_merge_exception() -> None:
        """ Test merging two heaps. """
        heap1 = BinomialHeap[int](allow_duplicates=False)
        heap2 = BinomialHeap[int]()
        heap1.enqueue(1, 1)
        heap1.enqueue(3, 3)
        heap1.enqueue(5, 5)

        heap2.enqueue(2, 2)
        heap2.enqueue(3, 3)
        heap2.enqueue(4, 4)
        heap2.enqueue(6, 6)

        with pytest.raises(RuntimeError):
            heap1.merge(heap2)

    @staticmethod
    def test_duplicates() -> None:
        """ Add lots of duplicates and see what happens. """
        heap = BinomialHeap[int](allow_duplicates=True)
        for _ in range(10):
            for index2 in range(10):
                heap.enqueue(index2, 1.0)

        assert len(heap) == 100
        actual_count = 0
        while heap:
            _ = heap.dequeue()
            actual_count += 1

        assert actual_count == 100

    @staticmethod
    def test_print_heap() -> None:
        heap = BinomialHeap[int]()
        heap.enqueue(1, 1)
        heap.enqueue(3, 3)
        heap.enqueue(5, 2)
        heap.enqueue(2, 2)
        heap.enqueue(4, 4)
        heap.enqueue(6, 8)
        heap.dequeue()

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
