"""
Convert International System of Units (SI) and Binary prefixes
"""
from enum import IntEnum, unique


@unique
class SI_Unit(IntEnum):
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
class Binary_Unit(IntEnum):
    yotta = 8
    zetta = 7
    exa = 6
    peta = 5
    tera = 4
    giga = 3
    mega = 2
    kilo = 1


def convert_si_prefix(
    known_amount: float, from_prefix: SI_Unit, to_prefix: SI_Unit
) -> float:
    """
    >>> convert_si_prefix(1, SI_Unit.giga, SI_Unit.mega)
    1000
    >>> convert_si_prefix(1, SI_Unit.mega, SI_Unit.giga)
    0.001
    >>> convert_si_prefix(1, SI_Unit.kilo, SI_Unit.kilo)
    1
    >>> convert_si_prefix(1, 'giga', 'mega')
    1000
    >>> convert_si_prefix(1, 'gIGa', 'mEGa')
    1000
    """
    difference: float = from_prefix.value - to_prefix.value
    return known_amount * (10 ** difference)


def convert_binary_prefix(
    known_amount: float, from_prefix: Binary_Unit, to_prefix: Binary_Unit
) -> float:
    """
    >>> convert_binary_prefix(1, Binary_Unit.giga, Binary_Unit.mega)
    1024
    >>> convert_binary_prefix(1, Binary_Unit.mega, Binary_Unit.giga)
    0.0009765625
    >>> convert_binary_prefix(1, Binary_Unit.kilo, Binary_Unit.kilo)
    1
    >>> convert_binary_prefix(1, 'giga', 'mega')
    1024
    >>> convert_binary_prefix(1, 'gIGa', 'mEGa')
    1024
    """
    difference: float = from_prefix.value - to_prefix.value
    return known_amount * (2 ** (difference * 10))
