from cs.structures import FibonacciHeap
from tests.structures.heap.heap_test import parametrize_allow_duplicates


class TestFibonacciHeap:
    """
    This class only contains tests exclusive to Fibonacci Heaps.
    All other common heap functionality tests are located in heap_test.py.
    """

    @staticmethod
    def test_remove() -> None:
        """ Test decrease_key method. """
        fib_heap = FibonacciHeap[int]()
        fib_heap.enqueue(1, 1)
        fib_heap.enqueue(3, 3)
        fib_heap.enqueue(5, 5)

        fib_heap.remove(3)

        assert len(fib_heap) == 2

        actual_list = []
        while fib_heap:
            actual_list.append(fib_heap.dequeue())

        assert actual_list == [(1, 1), (5, 5)]

    @staticmethod
    @parametrize_allow_duplicates
    def test_decrease_key(allow_duplicates: bool) -> None:
        """ Test decrease_key method. """
        fib_heap = FibonacciHeap[int](allow_duplicates=allow_duplicates)
        fib_heap.enqueue(1, 1)
        entry3 = fib_heap.enqueue(3, 3)
        fib_heap.enqueue(5, 5)

        fib_heap.decrease_key(entry3 if allow_duplicates else 3, -1)

        actual_list = []
        while fib_heap:
            actual_list.append(fib_heap.dequeue())

        assert actual_list == [(3, -1), (1, 1), (5, 5)]

    @staticmethod
    @parametrize_allow_duplicates
    def test_severe_decrease_key(allow_duplicates: bool) -> None:
        """ More severe decrease_key test, based on SSCCE code from Marian Aioanei. """
        heap = FibonacciHeap[int](allow_duplicates=allow_duplicates)
        expected_count = 17
        entries = {}
        for index in range(expected_count):
            entry = heap.enqueue(index, 2.0)
            entries[index] = entry

        _ = heap.dequeue()
        expected_count -= 1

        for index in range(10, 7, -1):
            heap.decrease_key(entries[index], 1.0)

        actual_count = 0
        while heap:
            _ = heap.dequeue()
            actual_count += 1

        assert actual_count == expected_count

    @staticmethod
    def test_duplicates_with_decreases() -> None:
        """ Add lots of duplicates and see what happens. """
        heap = FibonacciHeap[int](allow_duplicates=True)
        priority = 0.0
        entries = {}
        for i in range(10):
            for j in range(10):
                priority += 1.0
                entries[(i, j)] = heap.enqueue(i, -priority)

        for i in range(10):
            heap.decrease_key(entries[(i, i)], -100.0 - i)

        actual_list = []
        while heap:
            value, _ = heap.dequeue()
            actual_list.append(value)

        assert len(actual_list) == 100

        expected_list = list(range(9, -1, -1))
        for number in range(9, -1, -1):
            expected_list.extend([number] * 9)

        assert actual_list == expected_list
