import random
from typing import Callable, Optional


def get_statement(indent: int, prev_fn: Optional[Callable[[int], str]]) -> str:
    good = prev_fn not in (get_two_statements, add_statement)
    dist = {
        get_two_statements: 1 - 0.4 * indent,
        get_action: 0.6,
        get_if: 1 - 0.4 * indent,
        get_while: 0.1 if good else 0,
        get_for: 1 - 0.3 * indent if good else 0,
        get_if_else: 1 - 0.6 * indent if good else 0,
        get_if_elif_else: 1 - 0.99 * indent if good else 0,
    }
    options, probs = list(dist.keys()), list(dist.values())
    return random.choices(options, probs, k=1)[0](indent)


def add_statement(indent: int) -> str:
    return f"{add_indent(indent)}{get_statement(indent, add_statement)}"


def get_two_statements(indent: int) -> str:
    return f"{get_statement(indent, get_two_statements)}\n" f"{add_statement(indent)}"


def get_if(indent: int) -> str:
    return f"if {get_condition()}:\n" f"{add_statement(indent + 1)}"


def get_if_else(indent: int) -> str:
    return f"{get_if(indent)}\n" f"{add_indent(indent)}else:\n" f"{add_statement(indent + 1)}"


def get_if_elif_else(indent: int) -> str:
    return (
        f"{get_if(indent)}\n"
        f"{add_indent(indent)}elif:\n"
        f"{add_statement(indent + 1)}\n"
        f"{add_indent(indent)}else:\n"
        f"{add_statement(indent + 1)}"
    )


def get_while(indent: int) -> str:
    return f"while {get_condition()}:\n" f"{add_statement(indent + 1)}"


def get_for(indent: int) -> str:
    return f"for _ in range({get_num()}):\n" f"{add_statement(indent + 1)}"


def get_condition() -> str:
    options = [
        "front_is_clear()",
        "left_is_clear()",
        "right_is_clear()",
        "beepers_present()",
        "no_beepers_present()",
    ]
    options += ["not " + opt for opt in options]
    probs = [random.randrange(len(options)) for _ in options]
    return random.choice(random.choices(options, probs))


def get_action(indent: int) -> str:
    del indent
    options = ["move()", "turn_left()", "turn_right()", "put_beeper()", "pick_beeper()"]
    probs = [random.randrange(len(options)) for _ in options]
    return random.choice(random.choices(options, probs))


def get_num() -> int:
    options = list(range(1, 20))
    probs = [20 - num for num in options]
    return random.choice(random.choices(options, probs))


def add_indent(indent: int) -> str:
    return " " * 4 * indent


def main() -> str:
    indent = 1
    return f"def main():\n" f"{add_indent(indent)}{get_statement(indent, None)}"


if __name__ == "__main__":
    print(main())
