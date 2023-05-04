import operator

from cs.structures import BinaryHeap


class TestBinaryHeap:
    @staticmethod
    def test_max_heap() -> None:
        h = BinaryHeap[int]()
        h.enqueue(34)
        h.enqueue(31)
        h.enqueue(37)
        assert h.peek() == 37
        assert h.pop() == 37
        assert h.pop() == 34
        assert h.pop() == 31

    @staticmethod
    def test_min_heap() -> None:
        h = BinaryHeap[int](key=operator.neg)
        h.enqueue(34)
        h.enqueue(31)
        h.enqueue(37)
        assert h.peek() == 31
        assert h.pop() == 31
        assert h.pop() == 34
        assert h.pop() == 37
        h.enqueue(45)
        h.enqueue(40)
        h.enqueue(50)
        assert h.peek() == 40
        h.update(50, 10)
        assert h.peek() == 10
        h.dequeue(10)
        assert h.peek() == 40

    @staticmethod
    def test_repr() -> None:
        h = BinaryHeap[int]()
        h.enqueue(34)
        h.enqueue(1)
        h.enqueue(7)

        assert repr(h) == str(h) == "BinaryHeap(_heap=[34, 1, 7])"
