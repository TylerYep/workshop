from src.structures import Stack


def test_stack() -> None:
    keys = ["the", "a", "there", "anaswe", "any", "by", "their"]
    stack: Stack[str] = Stack()
    for key in keys:
        stack.push(key)

    assert stack.pop() == "their"
    assert stack.pop() == "by"
    assert stack.peek() == "any"
    assert stack.pop() == "any"
