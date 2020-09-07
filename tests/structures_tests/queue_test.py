from src.structures import Queue


def test_queue() -> None:
    keys = ["the", "a", "there", "anaswe", "any", "by", "their"]
    queue: Queue[str] = Queue()
    for key in keys:
        queue.enqueue(key)

    assert queue.dequeue() == "the"
    assert queue.dequeue() == "a"
    assert queue.peek() == "there"
    assert queue.dequeue() == "there"
