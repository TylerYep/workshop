import random

from cs.structures import BinomialHeap


class TestBinomialHeap:
    """
    This class only contains tests exclusive to Binomial Heaps.
    All other common heap functionality tests are located in heap_test.py.
    """

    @staticmethod
    def test_binomial_property() -> None:
        heap = BinomialHeap[int](allow_duplicates=True)
        for _ in range(15):
            random_value = random.randrange(10)
            random_priority = random.randrange(10)
            heap.enqueue(random_value, random_priority)

        assert [len(tree) for tree in heap.trees if tree is not None] == [1, 2, 3, 5]
