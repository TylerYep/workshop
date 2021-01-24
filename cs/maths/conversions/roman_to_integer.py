def roman_to_int(roman: str) -> int:
    """
    Roman to Integer
    Given a roman numeral, convert it to an integer.
    Input is guaranteed to be within the range from 1 to 3999.
    https://en.wikipedia.org/wiki/Roman_numerals
    """
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total, place = 0, 0
    while place < len(roman):
        if place + 1 < len(roman) and vals[roman[place]] < vals[roman[place + 1]]:
            total += vals[roman[place + 1]] - vals[roman[place]]
            place += 2
        else:
            total += vals[roman[place]]
            place += 1
    return total
