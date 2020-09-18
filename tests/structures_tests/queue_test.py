from src.structures import Queue


def test_queue() -> None:
    keys = ["the", "a", "there", "anaswe", "any", "by", "their"]
    queue = Queue[str]()
    for key in keys:
        queue.enqueue(key)

    assert queue.dequeue() == "the"
    assert queue.dequeue() == "a"
    assert queue.peek() == "there"
    assert queue.dequeue() == "there"


def test_print_queue() -> None:
    q = Queue[int]()
    q.enqueue(34)
    q.enqueue(1)
    q.enqueue(7)

    assert str(q) == "Queue(_queue=[34, 1, 7])"
