"""
Functions useful for doing molecular chemistry:
* molarity_to_normality
* moles_to_pressure
* moles_to_volume
* pressure_and_volume_to_temperature
"""


def molarity_to_normality(nfactor: int, moles: float, volume: float) -> float:
    """
    Convert molarity to normality.
    Volume is taken in litres.

    Wikipedia reference: https://en.wikipedia.org/wiki/Equivalent_concentration
    Wikipedia reference: https://en.wikipedia.org/wiki/Molar_concentration
    """
    return round(moles / volume * nfactor)


def moles_to_pressure(volume: float, moles: float, temperature: float) -> float:
    """
    Convert moles to pressure.
    Ideal gas laws are used.
    Temperature is taken in kelvin.
    Volume is taken in litres.
    Pressure has atm as SI unit.

    Wikipedia reference: https://en.wikipedia.org/wiki/Gas_laws
    Wikipedia reference: https://en.wikipedia.org/wiki/Pressure
    Wikipedia reference: https://en.wikipedia.org/wiki/Temperature
    """
    return round(moles * 0.0821 * temperature / volume)


def moles_to_volume(pressure: float, moles: float, temperature: float) -> float:
    """
    Convert moles to volume.
    Ideal gas laws are used.
    Temperature is taken in kelvin.
    Volume is taken in litres.
    Pressure has atm as SI unit.

    Wikipedia reference: https://en.wikipedia.org/wiki/Gas_laws
    Wikipedia reference: https://en.wikipedia.org/wiki/Pressure
    Wikipedia reference: https://en.wikipedia.org/wiki/Temperature
    """
    return round(moles * 0.0821 * temperature / pressure)


def pressure_and_volume_to_temperature(
    pressure: float, moles: float, volume: float
) -> float:
    """
    Convert pressure and volume to temperature.
    Ideal gas laws are used.
    Temperature is taken in kelvin.
    Volume is taken in litres.
    Pressure has atm as SI unit.

    Wikipedia reference: https://en.wikipedia.org/wiki/Gas_laws
    Wikipedia reference: https://en.wikipedia.org/wiki/Pressure
    Wikipedia reference: https://en.wikipedia.org/wiki/Temperature
    """
    return round(pressure * volume / (0.0821 * moles))
