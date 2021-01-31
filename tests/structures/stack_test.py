from cs.structures import Stack


class TestStack:
    @staticmethod
    def test_stack() -> None:
        keys = ["the", "a", "there", "anaswe", "any", "by", "their"]
        stack = Stack[str]()
        for key in keys:
            stack.push(key)
        if stack:
            assert "any" in stack

        assert len(stack) == 7
        assert stack.pop() == "their"
        assert stack.pop() == "by"
        assert stack.peek() == "any"
        assert stack.pop() == "any"

    @staticmethod
    def test_repr() -> None:
        stack = Stack[int]()
        stack.push(34)
        stack.push(1)
        stack.push(7)

        assert repr(stack) == str(stack) == "Stack(_stack=[34, 1, 7])"
