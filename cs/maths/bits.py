from __future__ import annotations

import math
from collections.abc import Iterator


class Bits:
    """
    Personal bits implementation. For all real purposes, use the bitarray library.
    https://docs.python.org/3/library/operator.html
    """

    def __init__(self, val: str = "", *, length: int | None = None) -> None:
        assert length is None or length > 0
        is_negative = len(val) > 0 and val[0] == "-"
        val_check = val[1:] if is_negative else val
        if not all(ch in ("0", "1") for ch in val_check):
            raise RuntimeError(f"{val} is not a valid Bits initial value.")

        self.val = int(val, 2) if val else -1  # -1 == 111111
        self.length = length or len(val)

    def __str__(self) -> str:
        return self.binary_str(self.val, self.length)

    def __repr__(self) -> str:
        return f"Bits({str(self)}, val={self.val}, length={self.length})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.val == other
        if isinstance(other, Bits):
            return str(self) == str(other)
        return NotImplemented

    def __len__(self) -> int:
        return self.length

    def __lshift__(self, other: object) -> Bits:
        if not isinstance(other, int):
            raise TypeError("Bit shifts require an integer shift amount.")
        return Bits(str(self.val * (2**other)), length=self.length)

    def __rshift__(self, other: object) -> Bits:
        if not isinstance(other, int):
            raise TypeError("Bit shifts require an integer shift amount.")
        return Bits(str(self.val // (2**other)), length=self.length)

    def __ilshift__(self, other: object) -> None:
        if not isinstance(other, int):
            raise TypeError("Bit shifts require an integer shift amount.")
        self.val *= 2**other

    def __irshift__(self, other: object) -> None:
        if not isinstance(other, int):
            raise TypeError("Bit shifts require an integer shift amount.")
        self.val //= 2**other

    def __invert__(self) -> Bits:
        """Inverts all bits."""
        return Bits.from_num(~self.val, self.length)

    def __and__(self, other: object) -> Bits:
        """Intersection of two role sets."""
        if not isinstance(other, Bits):
            raise TypeError(f"{other} cannot be intersected with Bits.")
        return Bits.from_num(self.val & other.val, self.length)

    def __iand__(self, other: object) -> None:
        """Intersection of two role sets."""
        if not isinstance(other, Bits):
            raise TypeError(f"{other} cannot be intersected with Bits.")
        self.val &= other.val

    def __or__(self, other: object) -> Bits:
        """Intersection of two role sets."""
        if not isinstance(other, Bits):
            raise TypeError(f"{other} cannot be or'd with Bits.")
        return Bits.from_num(self.val | other.val, self.length)

    def __ior__(self, other: object) -> None:
        """Intersection of two role sets."""
        if not isinstance(other, Bits):
            raise TypeError(f"{other} cannot be or'd with Bits.")
        self.val |= other.val

    def __xor__(self, other: object) -> Bits:
        """Intersection of two role sets."""
        if not isinstance(other, Bits):
            raise TypeError(f"{other} cannot be xor'd with Bits.")
        return Bits.from_num(self.val ^ other.val, self.length)

    def __ixor__(self, other: object) -> None:
        """Intersection of two role sets."""
        if not isinstance(other, Bits):
            raise TypeError(f"{other} cannot be xor'd with Bits.")
        self.val ^= other.val

    def __getitem__(self, index: int) -> int:
        return int(str(self)[index])

    def __setitem__(self, index: int, bit: int) -> None:
        if bit not in (0, 1):
            raise ValueError(f"Bit value must be 0 or 1: {bit}")
        new_val = str(self)
        new_val = new_val[:index] + str(bit) + new_val[index + 1 :]
        self.val = int(new_val, 2) if new_val else -1

    def __iter__(self) -> Iterator[int]:
        for bit in str(self):
            yield int(bit)

    def __add__(self, other: object) -> Bits:
        if not isinstance(other, Bits):
            raise TypeError(f"{other} cannot be added with Bits.")
        length = max(len(self), len(other))
        lhs = [0] * (length - len(self)) + [int(digit) for digit in self]
        rhs = [0] * (length - len(other)) + [int(digit) for digit in other]
        carry = 0
        result = []
        for i in range(1, len(lhs) + 1):
            column = lhs[-i] + rhs[-i] + carry
            result.append(column % 2)
            carry = column // 2
        if carry != 0:
            result.append(carry)
        result.reverse()
        return Bits("".join([str(s) for s in result]))

    def __sub__(self, other: object) -> Bits:
        if not isinstance(other, Bits):
            raise TypeError(f"{other} cannot be subtracted from Bits.")
        length = max(len(self), len(other))
        lhs = [0] * (length - len(self)) + [int(digit) for digit in self]
        rhs = [0] * (length - len(other)) + [int(digit) for digit in other]
        result = []
        for i in range(1, len(lhs) + 1):
            difference = lhs[-i] - rhs[-i]
            if difference >= 0:
                result.append(difference)
                continue
            for j in range(i + 1, length + 1):
                lhs[-j] = (lhs[-j] + 1) % 2
                if lhs[-j] != 1:
                    break
            result.append(difference + 2)
        result.reverse()
        return Bits("".join([str(s) for s in result]))

    @property
    def is_solo(self) -> bool:
        return self.val != 0 and (self.val & (self.val - 1)) == 0

    @property
    def solo(self) -> int:
        """Assumes is_solo is True."""
        if not self.is_solo:
            raise RuntimeError("Does not contain a solo bit.")
        return self.length - int(math.log2(self.val)) - 1

    @classmethod
    def from_num(cls, val: int, length: int) -> Bits:
        return cls(cls.binary_str(val, length), length=length)

    @staticmethod
    def binary_str(val: int, length: int) -> str:
        # return bin(val & (2 ** length - 1))
        coerced_positive_val = val & (2**length - 1)
        return f"{coerced_positive_val:0{length}b}"

    def is_one(self, index: int) -> bool:
        """Returns True if the bit at given index is 1."""
        if index > self.length:
            return False
        return (self.val & (1 << index)) == 0
        # return ((self.val >> index) & 1) == 1

    def set_bit(self, index: int, new_val: bool = True) -> Bits:
        """Mark an index as the given value of its current state."""
        if not 0 <= index < self.length:
            raise RuntimeError("Invalid bit; cannot be set.")

        reversed_index = self.length - index - 1
        if new_val:
            self.val |= 1 << reversed_index
        else:
            self.val &= ~(1 << reversed_index)

        return Bits.from_num(self.val, self.length)

    def flip_index(self, index: int) -> Bits:
        """Mark an index as opposite of its current state."""
        return Bits.from_num(self.val ^ (1 << index), self.length)
        # reversed_index = self.length - index - 1
        # new_val = self.val
        # new_val &= ~(1 << reversed_index)
        # if new_val == self.val:
        #     new_val |= 1 << reversed_index
        # return Bits.from_num(new_val, self.length)
