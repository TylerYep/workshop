"""
Convert International System of Units (SI) and Binary prefixes
"""
from enum import IntEnum, unique


@unique
class SIUnit(IntEnum):
    yotta = 24
    zetta = 21
    exa = 18
    peta = 15
    tera = 12
    giga = 9
    mega = 6
    kilo = 3
    hecto = 2
    deca = 1
    deci = -1
    centi = -2
    milli = -3
    micro = -6
    nano = -9
    pico = -12
    femto = -15
    atto = -18
    zepto = -21
    yocto = -24


@unique
class BinaryUnit(IntEnum):
    yotta = 8
    zetta = 7
    exa = 6
    peta = 5
    tera = 4
    giga = 3
    mega = 2
    kilo = 1


def convert_si_prefix(
    known_amount: float, from_prefix: SIUnit, to_prefix: SIUnit
) -> float:
    difference: float = from_prefix - to_prefix
    return known_amount * float(10**difference)


def convert_binary_prefix(
    known_amount: float, from_prefix: BinaryUnit, to_prefix: BinaryUnit
) -> float:
    difference: float = from_prefix.value - to_prefix.value
    return known_amount * float(2 ** (difference * 10))
