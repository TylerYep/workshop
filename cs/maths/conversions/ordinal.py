def make_ordinal(n: int) -> str:
    """
    Convert an integer into its ordinal representation:

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    """
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    suffix = ("th", "st", "nd", "rd", "th")[min(n % 10, 4)]
    return f"{n}{suffix}"
