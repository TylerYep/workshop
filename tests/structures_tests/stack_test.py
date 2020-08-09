from src.structures.stack import Stack


def test_stack() -> None:
    keys = ["the", "a", "there", "anaswe", "any", "by", "their"]
    stack: Stack[str] = Stack()
    for key in keys:
        stack.push(key)

    # Search for different keys
    assert stack.pop() == "their"
    assert stack.pop() == "by"
    assert stack.peek() == "any"
    assert stack.pop() == "any"
