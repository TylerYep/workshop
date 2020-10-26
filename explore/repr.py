class A:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def __repr__(self) -> str:
        field_pairs = [
            f"{attr}={getattr(self, attr)}"
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("_")
        ]
        return f"{self.__class__.__qualname__}({', '.join(field_pairs)})"

    def whatever(self) -> None:
        self.a *= 2
