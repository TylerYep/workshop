import random

from src.structures import FibonacciHeap


def test_addition_of_100() -> None:
    """ Test creating a fibonacci heap and adding 100 values to it. """
    fib_heap = FibonacciHeap[int]()
    for _ in range(100):
        random_value = random.randrange(100)
        random_priority = random.randrange(100)
        fib_heap.enqueue(random_value, random_priority)


def test_get_min_of_1() -> None:
    """
    Test creating a fibonacci heap, adding a single value to it, and retrieving it.
    """
    fib_heap = FibonacciHeap[int]()
    fib_heap.enqueue(1, 1)
    entry = fib_heap.min()

    assert entry.value == 1


def test_get_min_of_3() -> None:
    """
    Test creating a fibonacci heap, adding 3 values, and retrieving
    the minimum-priority entry.
    """
    fib_heap = FibonacciHeap[int]()
    fib_heap.enqueue(1, 1)
    fib_heap.enqueue(10, 0)
    fib_heap.enqueue(20, 100)
    entry = fib_heap.min()

    assert entry.value == 10


def test_get_min_of_3_float() -> None:
    """
    Test creating a fibonacci heap, adding 3 values, and
    retrieving the minimum-float-priority entry.
    """
    fib_heap = FibonacciHeap[int]()
    fib_heap.enqueue(10, 1.1)
    fib_heap.enqueue(100, 1.0)
    fib_heap.enqueue(20, 1.2)
    entry = fib_heap.min()

    assert entry.value == 100


def test_empty() -> None:
    """ Test an empty heap to see if it's Falsy. """
    assert bool(FibonacciHeap[int]()) is False


def test_nonempty() -> None:
    """ Test creating a fibonacci, adding a value, and checking if it's Truthy. """
    fib_heap = FibonacciHeap[int]()
    fib_heap.enqueue(1, 1)
    assert bool(fib_heap) is True


def test_len() -> None:
    """
    Test creating a fibonacci heap, adding "intended_length" values, and checking
    for correct length.
    """
    for intended_length in (0, 1, 3, 100):
        fib_heap = FibonacciHeap[int]()
        for _ in range(intended_length):
            random_value = random.randrange(intended_length)
            random_priority = random.randrange(intended_length)
            fib_heap.enqueue(random_value, random_priority)

        assert len(fib_heap) == intended_length


def test_dequeue_min() -> None:
    """
    Test creating a fibonacci heap, adding "intended_length" values,
    and checking for correct dequeue_min values.
    """
    for intended_length in (0, 1, 2, 3, 10, 100):
        fib_heap = FibonacciHeap[int]()
        # random.seed(0) gives too-consistent priorities
        random.seed(1)
        expected_priorities_list = []
        for _ in range(intended_length):
            random_value = random.randrange(intended_length)
            random_priority = random.randrange(intended_length)
            fib_heap.enqueue(random_value, random_priority)
            expected_priorities_list.append(random_priority)
        expected_priorities_list.sort()

        actual_priorities_list = []
        for _ in range(intended_length):
            entry = fib_heap.dequeue_min()
            actual_priorities_list.append(entry.priority)

        # We can't just compare lists, because this is basically a heapsort,
        # which isn't stable.  So instead we compare all the priorities
        assert expected_priorities_list == actual_priorities_list


def test_dequeue_min_sort() -> None:
    """
    Test creating a fibonacci heap, adding "intended_length" values, and
    checking for correct dequeue_min values.
    """
    for intended_length in (0, 1, 2, 3, 10, 100):
        fib_heap = FibonacciHeap[int]()
        # random.seed(0) gives too-consistent priorities
        random.seed(1)
        random_values = list(range(intended_length))
        random_priorities = list(range(intended_length))
        tuples = list(zip(random_priorities, random_values))
        random.shuffle(tuples)

        for tuple_ in tuples:
            fib_heap.enqueue(*tuple_)
        expected_list = tuples[:]
        expected_list.sort()

        actual_list = []
        for _ in range(intended_length):
            entry = fib_heap.dequeue_min()
            actual_list.append((entry.priority, entry.value))

        # We can just compare lists, because although this is basically a heapsort,
        # which isn't stable, we have no duplicate priorities or duplicate values,
        # so the instability doesn't matter.
        assert expected_list == actual_list


def test_decrease_key() -> None:
    """ Test decrease_key method. """
    fib_heap = FibonacciHeap[int]()
    fib_heap.enqueue(1, 1)
    entry3 = fib_heap.enqueue(3, 3)
    fib_heap.enqueue(5, 5)

    fib_heap.decrease_key(entry3, -1)

    actual_list = []
    while fib_heap:
        entry = fib_heap.dequeue_min()
        actual_list.append((entry.priority, entry.value))

    assert actual_list == [(-1, 3), (1, 1), (5, 5)]


def test_merge() -> None:
    """ Test merging two heaps. """
    heap1 = FibonacciHeap[int]()
    heap2 = FibonacciHeap[int]()

    heap1.enqueue(1, 1)
    heap1.enqueue(3, 3)
    heap1.enqueue(5, 5)

    heap2.enqueue(2, 2)
    heap2.enqueue(3, 3)
    heap2.enqueue(4, 4)
    heap2.enqueue(6, 6)

    merged_heap = heap1.merge(heap2)

    assert len(merged_heap) == 7

    actual_list = []
    while merged_heap:
        entry = merged_heap.dequeue_min()
        actual_list.append((entry.priority, entry.value))

    assert actual_list == [(1, 1), (2, 2), (3, 3), (3, 3), (4, 4), (5, 5), (6, 6)]


def severe_decrease_key_test() -> None:
    """ More severe decrease_key test, based on SSCCE code from Marian Aioanei. """
    min_prio_queue = FibonacciHeap[int]()
    map_entries = {}
    expected_count = 17
    for index in range(expected_count):
        map_entries[index] = min_prio_queue.enqueue(index, 2.0)

    _ = min_prio_queue.dequeue_min()
    expected_count -= 1

    for index in range(10, 7, -1):
        min_prio_queue.decrease_key(map_entries[index], 1.0)

    actual_count = 0
    while min_prio_queue:
        _ = min_prio_queue.dequeue_min()
        actual_count += 1

    assert actual_count == expected_count


def test_duplicates() -> None:
    """ Add lots of duplicates and see what happens. """
    min_prio_queue = FibonacciHeap[int]()
    for _ in range(10):
        for index2 in range(10):
            min_prio_queue.enqueue(index2, 1.0)

    actual_count = 0
    while min_prio_queue:
        _ = min_prio_queue.dequeue_min()
        actual_count += 1

    assert actual_count == 100


def test_duplicates_with_decreases() -> None:
    """ Add lots of duplicates and see what happens. """
    min_prio_queue = FibonacciHeap[int]()
    priority = 0.0
    entries = {}
    for index in range(10):
        for index2 in range(10):
            priority += 1.0
            entries[(index, index2)] = min_prio_queue.enqueue(index, -priority)

    for index in range(10):
        min_prio_queue.decrease_key(entries[(index, 0)], -100.0 - index)

    actual_list = []
    actual_count = 0
    while bool(min_prio_queue):
        actual_list.append(min_prio_queue.dequeue_min().value)
        actual_count += 1

    assert actual_count == 100

    expected_list = list(range(9, -1, -1))
    for number in range(9, -1, -1):
        expected_list.extend([number] * 9)

    assert actual_list == expected_list
