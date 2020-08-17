from src.structures import BinaryHeap


def test_max_heap() -> None:
    h = BinaryHeap[int]()
    h.insert(34)
    h.insert(31)
    h.insert(37)
    assert h.get_top() == 37
    assert h.extract_top() == 37
    assert h.extract_top() == 34
    assert h.extract_top() == 31


def test_min_heap() -> None:
    h = BinaryHeap[int](key=lambda x: -x)
    h.insert(34)
    h.insert(31)
    h.insert(37)
    assert h.get_top() == 31
    assert h.extract_top() == 31
    assert h.extract_top() == 34
    assert h.extract_top() == 37
    h.insert(45)
    h.insert(40)
    h.insert(50)
    assert h.get_top() == 40
    h.update(50, 10)
    assert h.get_top() == 10
    h.delete(10)
    assert h.get_top() == 40
