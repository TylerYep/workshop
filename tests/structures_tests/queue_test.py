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
    queue = Queue[int]()
    queue.enqueue(34)
    queue.enqueue(1)
    queue.enqueue(7)

    assert repr(queue) == str(queue) == "Queue(_queue=[34, 1, 7])"
