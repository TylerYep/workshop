from fractions import Fraction


def convert_decimal_to_fraction() -> None:
    while num := input("Enter a decimal: "):
        try:
            result = Fraction(float(num))
            print(
                "The approximate equivalent fraction is: "
                f"{result.limit_denominator(1000)}\n"
            )
        except ValueError:
            print("Invalid decimal.\n")


if __name__ == "__main__":
    convert_decimal_to_fraction()
