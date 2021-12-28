def celsius_to_fahrenheit(celsius: float, ndigits: int = 2) -> float:
    """
    Convert a given value from Celsius to Fahrenheit and round it to 2 decimal places.
    Wikipedia reference: https://en.wikipedia.org/wiki/Celsius
    Wikipedia reference: https://en.wikipedia.org/wiki/Fahrenheit
    """
    return round(celsius * 9 / 5 + 32, ndigits)


def celsius_to_kelvin(celsius: float, ndigits: int = 2) -> float:
    """
    Convert a given value from Celsius to Kelvin and round it to 2 decimal places.
    Wikipedia reference: https://en.wikipedia.org/wiki/Celsius
    Wikipedia reference: https://en.wikipedia.org/wiki/Kelvin
    """
    return round(celsius + 273.15, ndigits)


def celsius_to_rankine(celsius: float, ndigits: int = 2) -> float:
    """
    Convert a given value from Celsius to Rankine and round it to 2 decimal places.
    Wikipedia reference: https://en.wikipedia.org/wiki/Celsius
    Wikipedia reference: https://en.wikipedia.org/wiki/Rankine_scale
    """
    return round(celsius * 9 / 5 + 491.67, ndigits)


def fahrenheit_to_celsius(fahrenheit: float, ndigits: int = 2) -> float:
    """
    Convert a given value from Fahrenheit to Celsius and round it to 2 decimal places.
    Wikipedia reference: https://en.wikipedia.org/wiki/Fahrenheit
    Wikipedia reference: https://en.wikipedia.org/wiki/Celsius
    """
    return round((fahrenheit - 32) * 5 / 9, ndigits)


def fahrenheit_to_kelvin(fahrenheit: float, ndigits: int = 2) -> float:
    """
    Convert a given value from Fahrenheit to Kelvin and round it to 2 decimal places.
    Wikipedia reference: https://en.wikipedia.org/wiki/Fahrenheit
    Wikipedia reference: https://en.wikipedia.org/wiki/Kelvin
    """
    return round(((fahrenheit - 32) * 5 / 9) + 273.15, ndigits)


def fahrenheit_to_rankine(fahrenheit: float, ndigits: int = 2) -> float:
    """
    Convert a given value from Fahrenheit to Rankine and round it to 2 decimal places.
    Wikipedia reference: https://en.wikipedia.org/wiki/Fahrenheit
    Wikipedia reference: https://en.wikipedia.org/wiki/Rankine_scale
    """
    return round(fahrenheit + 459.67, ndigits)


def kelvin_to_celsius(kelvin: float, ndigits: int = 2) -> float:
    """
    Convert a given value from Kelvin to Celsius and round it to 2 decimal places.
    Wikipedia reference: https://en.wikipedia.org/wiki/Kelvin
    Wikipedia reference: https://en.wikipedia.org/wiki/Celsius
    """
    return round(kelvin - 273.15, ndigits)


def kelvin_to_fahrenheit(kelvin: float, ndigits: int = 2) -> float:
    """
    Convert a given value from Kelvin to Fahrenheit and round it to 2 decimal places.
    Wikipedia reference: https://en.wikipedia.org/wiki/Kelvin
    Wikipedia reference: https://en.wikipedia.org/wiki/Fahrenheit
    """
    return round((kelvin - 273.15) * 9 / 5 + 32, ndigits)


def kelvin_to_rankine(kelvin: float, ndigits: int = 2) -> float:
    """
    Convert a given value from Kelvin to Rankine and round it to 2 decimal places.
    Wikipedia reference: https://en.wikipedia.org/wiki/Kelvin
    Wikipedia reference: https://en.wikipedia.org/wiki/Rankine_scale
    """
    return round(kelvin * 9 / 5, ndigits)


def rankine_to_celsius(rankine: float, ndigits: int = 2) -> float:
    """
    Convert a given value from Rankine to Celsius and round it to 2 decimal places.
    Wikipedia reference: https://en.wikipedia.org/wiki/Rankine_scale
    Wikipedia reference: https://en.wikipedia.org/wiki/Celsius
    """
    return round((rankine - 491.67) * 5 / 9, ndigits)


def rankine_to_fahrenheit(rankine: float, ndigits: int = 2) -> float:
    """
    Convert a given value from Rankine to Fahrenheit and round it to 2 decimal places.
    Wikipedia reference: https://en.wikipedia.org/wiki/Rankine_scale
    Wikipedia reference: https://en.wikipedia.org/wiki/Fahrenheit
    """
    return round(rankine - 459.67, ndigits)


def rankine_to_kelvin(rankine: float, ndigits: int = 2) -> float:
    """
    Convert a given value from Rankine to Kelvin and round it to 2 decimal places.
    Wikipedia reference: https://en.wikipedia.org/wiki/Rankine_scale
    Wikipedia reference: https://en.wikipedia.org/wiki/Kelvin
    """
    return round(rankine * 5 / 9, ndigits)
