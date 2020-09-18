from src.structures import BinaryHeap


def test_max_heap() -> None:
    h = BinaryHeap[int]()
    h.insert(34)
    h.insert(31)
    h.insert(37)
    assert h.peek() == 37
    assert h.pop() == 37
    assert h.pop() == 34
    assert h.pop() == 31


def test_min_heap() -> None:
    h = BinaryHeap[int](key=lambda x: -x)
    h.insert(34)
    h.insert(31)
    h.insert(37)
    assert h.peek() == 31
    assert h.pop() == 31
    assert h.pop() == 34
    assert h.pop() == 37
    h.insert(45)
    h.insert(40)
    h.insert(50)
    assert h.peek() == 40
    h.update(50, 10)
    assert h.peek() == 10
    h.delete(10)
    assert h.peek() == 40


def test_print_heap() -> None:
    h = BinaryHeap[int]()
    h.insert(34)
    h.insert(1)
    h.insert(7)

    assert str(h) == "BinaryHeap(_heap=[34, 1, 7])"
