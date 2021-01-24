from cs.maths.conversions.molecular_chemistry import (
    molarity_to_normality,
    moles_to_pressure,
    moles_to_volume,
    pressure_and_volume_to_temperature,
)
from cs.maths.conversions.roman_to_integer import roman_to_int
from cs.maths.conversions.si_units import (
    Binary_Unit,
    SI_Unit,
    convert_binary_prefix,
    convert_si_prefix,
)
from cs.maths.conversions.temperature import (
    celsius_to_fahrenheit,
    celsius_to_kelvin,
    celsius_to_rankine,
    fahrenheit_to_celsius,
    fahrenheit_to_kelvin,
    fahrenheit_to_rankine,
    kelvin_to_celsius,
    kelvin_to_fahrenheit,
    kelvin_to_rankine,
    rankine_to_celsius,
    rankine_to_fahrenheit,
    rankine_to_kelvin,
)


def test_molecular_chemistry() -> None:
    assert molarity_to_normality(2, 3.1, 0.31) == 20
    assert molarity_to_normality(4, 11.4, 5.7) == 8
    assert moles_to_pressure(0.82, 3, 300) == 90
    assert moles_to_pressure(8.2, 5, 200) == 10
    assert moles_to_volume(0.82, 3, 300) == 90
    assert moles_to_volume(8.2, 5, 200) == 10
    assert pressure_and_volume_to_temperature(0.82, 1, 2) == 20
    assert pressure_and_volume_to_temperature(8.2, 5, 3) == 60


def test_roman_numerals() -> None:
    tests = {"III": 3, "CLIV": 154, "MIX": 1009, "MMD": 2500, "MMMCMXCIX": 3999}
    assert all(roman_to_int(key) == value for key, value in tests.items())


def test_si_units() -> None:
    assert convert_si_prefix(1, SI_Unit.giga, SI_Unit.mega) == 1000
    assert convert_si_prefix(1, SI_Unit.mega, SI_Unit.giga) == 0.001
    assert convert_si_prefix(1, SI_Unit.kilo, SI_Unit.kilo) == 1
    assert convert_binary_prefix(1, Binary_Unit.giga, Binary_Unit.mega) == 1024
    assert convert_binary_prefix(1, Binary_Unit.mega, Binary_Unit.giga) == 0.0009765625
    assert convert_binary_prefix(1, Binary_Unit.kilo, Binary_Unit.kilo) == 1


def test_celsius() -> None:
    assert celsius_to_fahrenheit(273.354, 3) == 524.037
    assert celsius_to_fahrenheit(273.354, 0) == 524.0
    assert celsius_to_fahrenheit(-40.0) == -40.0
    assert celsius_to_fahrenheit(-20.0) == -4.0
    assert celsius_to_fahrenheit(0) == 32.0
    assert celsius_to_fahrenheit(20) == 68.0
    assert celsius_to_fahrenheit(40) == 104.0

    assert celsius_to_kelvin(273.354, 3) == 546.504
    assert celsius_to_kelvin(273.354, 0) == 547.0
    assert celsius_to_kelvin(0) == 273.15
    assert celsius_to_kelvin(20.0) == 293.15
    assert celsius_to_kelvin(40) == 313.15

    assert celsius_to_rankine(273.354, 3) == 983.707
    assert celsius_to_rankine(273.354, 0) == 984.0
    assert celsius_to_rankine(0) == 491.67
    assert celsius_to_rankine(20.0) == 527.67
    assert celsius_to_rankine(40) == 563.67


def test_fahrenheit() -> None:
    assert fahrenheit_to_celsius(273.354, 3) == 134.086
    assert fahrenheit_to_celsius(273.354, 0) == 134.0
    assert fahrenheit_to_celsius(0) == -17.78
    assert fahrenheit_to_celsius(20.0) == -6.67
    assert fahrenheit_to_celsius(40.0) == 4.44
    assert fahrenheit_to_celsius(60) == 15.56
    assert fahrenheit_to_celsius(80) == 26.67
    assert fahrenheit_to_celsius(100) == 37.78

    assert fahrenheit_to_kelvin(273.354, 3) == 407.236
    assert fahrenheit_to_kelvin(273.354, 0) == 407.0
    assert fahrenheit_to_kelvin(0) == 255.37
    assert fahrenheit_to_kelvin(20.0) == 266.48
    assert fahrenheit_to_kelvin(40.0) == 277.59
    assert fahrenheit_to_kelvin(60) == 288.71
    assert fahrenheit_to_kelvin(80) == 299.82
    assert fahrenheit_to_kelvin(100) == 310.93

    assert fahrenheit_to_rankine(273.354, 3) == 733.024
    assert fahrenheit_to_rankine(273.354, 0) == 733.0
    assert fahrenheit_to_rankine(0) == 459.67
    assert fahrenheit_to_rankine(20.0) == 479.67
    assert fahrenheit_to_rankine(40.0) == 499.67
    assert fahrenheit_to_rankine(60) == 519.67
    assert fahrenheit_to_rankine(80) == 539.67
    assert fahrenheit_to_rankine(100) == 559.67


def test_kelvin() -> None:
    assert kelvin_to_fahrenheit(273.354, 3) == 32.367
    assert kelvin_to_fahrenheit(273.354, 0) == 32.0
    assert kelvin_to_fahrenheit(273.15) == 32.0
    assert kelvin_to_fahrenheit(300) == 80.33
    assert kelvin_to_fahrenheit(315.5) == 108.23

    assert kelvin_to_rankine(273.354, 3) == 492.037
    assert kelvin_to_rankine(273.354, 0) == 492.0
    assert kelvin_to_rankine(0) == 0.0
    assert kelvin_to_rankine(20.0) == 36.0
    assert kelvin_to_rankine(40) == 72.0

    assert kelvin_to_celsius(273.354, 3) == 0.204
    assert kelvin_to_celsius(273.354, 0) == 0.0
    assert kelvin_to_celsius(273.15) == 0.0
    assert kelvin_to_celsius(300) == 26.85
    assert kelvin_to_celsius(315.5) == 42.35


def test_rankine() -> None:
    assert rankine_to_celsius(273.354, 3) == -121.287
    assert rankine_to_celsius(273.354, 0) == -121.0
    assert rankine_to_celsius(273.15) == -121.4
    assert rankine_to_celsius(300) == -106.48
    assert rankine_to_celsius(315.5) == -97.87

    assert rankine_to_fahrenheit(273.15) == -186.52
    assert rankine_to_fahrenheit(300) == -159.67
    assert rankine_to_fahrenheit(315.5) == -144.17

    assert rankine_to_kelvin(0) == 0.0
    assert rankine_to_kelvin(20.0) == 11.11
    assert rankine_to_kelvin(40) == 22.22
