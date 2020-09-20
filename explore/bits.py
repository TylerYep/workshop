""" statements.py """
from __future__ import annotations

import math
from typing import Optional


class Bits:
    def __init__(self, val: str = "", length: Optional[int] = None) -> None:
        # assert all(ch in ("0", "1") for ch in val)
        self.val = int(val, 2) if val else -1  # -1 == 111111
        self.length = len(val) if length is None else length

    def __repr__(self) -> str:
        return self.binary_str(self.val, self.length)

    def __invert__(self) -> Bits:
        """ Inverts all bits. """
        return Bits.from_num(~self.val, self.length)

    def __and__(self, other: object) -> Bits:
        """ Intersection of two role sets. """
        assert isinstance(other, Bits)
        return Bits.from_num(self.val & other.val, self.length)

    @property
    def is_solo(self) -> bool:
        return self.val != 0 and (self.val & (self.val - 1)) == 0

    @property
    def solo(self) -> int:
        """ Assumes is_solo is True. """
        assert self.is_solo
        return self.length - int(math.log2(self.val)) - 1

    @staticmethod
    def binary_str(val: int, length: int) -> str:
        # return bin(val & (2 ** length - 1))
        coerced_positive_val = val & (2 ** length - 1)
        return f"{coerced_positive_val:0{length}b}"

    @classmethod
    def from_num(cls, val: int, length: int) -> Bits:
        return cls(f"{val:b}", length)

    def is_one(self, index: int) -> bool:
        """ Returns True if the bit at given index is 1. """
        return (self.val & (1 << index)) == 0

    def set_bit(self, index: int, new_val: bool) -> None:
        """ Mark an index as the given value of its current state. """
        assert self.length > index
        reversed_index = self.length - index - 1
        if new_val:
            self.val |= 1 << reversed_index
        else:
            self.val &= ~(1 << reversed_index)

    # def flip_index(self, index: int) -> RoleBits:
    #     """ Mark an index as opposite of its current state. """
    #     reversed_index = NUM_UNIQUE_ROLES - index - 1
    #     new_val = self
    #     new_val &= ~(1 << reversed_index)
    #     if new_val == self:
    #         new_val |= 1 << reversed_index
    #     return new_val

    def flip_index(self, index: int) -> Bits:
        """ Mark an index as opposite of its current state. """
        # TODO SHOULD THESE RETURN NEW STATES OR MODIFY OLD STATES IN PLACE
        # TODO USE XOR
        reversed_index = self.length - index - 1
        new_val = self.val
        new_val &= ~(1 << reversed_index)
        if new_val == self.val:
            new_val |= 1 << reversed_index
        return Bits.from_num(new_val, self.length)
