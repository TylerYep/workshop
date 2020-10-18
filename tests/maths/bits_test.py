from src.maths.bits import Bits


def test_constructors() -> None:
    x = Bits.from_num(5, length=4)
    assert str(x) == "0101"
    x_inv = ~x
    assert str(x_inv) == "1010"
    assert x_inv.val == 10


def test_set_bit() -> None:
    y = Bits("11001", length=6)
    assert str(y) == "011001"
    assert y.is_solo is False

    assert str(~y) == "100110"

    y.set_bit(3, True)
    assert str(y) == "011101"
    y.set_bit(3, False)
    assert str(y) == "011001"
    y.set_bit(0, False)
    assert str(y) == "011001"
    y.set_bit(5, False)
    y.set_bit(1, False)
    assert str(y) == "001000"

    assert y.is_solo is True


def test_bit_setter() -> None:
    y = Bits("11001", length=6)
    assert str(y) == "011001"
    assert y.is_solo is False

    assert str(~y) == "100110"

    y[3] = 1
    assert str(y) == "011101"
    y[3] = 0
    assert str(y) == "011001"
    assert y[3] == 0
    y[0] = 0
    assert str(y) == "011001"
    y[5] = 0
    y[1] = 0
    assert str(y) == "001000"

    assert y.is_solo is True


def test_add() -> None:
    assert Bits("0") + Bits("0") == Bits("0")
    assert Bits("0") + Bits("1") == Bits("1")
    assert Bits("1") + Bits("1") == Bits("10")

    x = Bits("11001", length=6)
    y = ~x
    assert x + y == Bits(length=6)
