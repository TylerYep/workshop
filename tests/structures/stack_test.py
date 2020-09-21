from src.structures import Stack


def test_stack() -> None:
    keys = ["the", "a", "there", "anaswe", "any", "by", "their"]
    stack = Stack[str]()
    for key in keys:
        stack.push(key)

    assert stack.pop() == "their"
    assert stack.pop() == "by"
    assert stack.peek() == "any"
    assert stack.pop() == "any"


def test_print_queue() -> None:
    stack = Stack[int]()
    stack.push(34)
    stack.push(1)
    stack.push(7)

    assert repr(stack) == str(stack) == "Stack(_stack=[34, 1, 7])"
