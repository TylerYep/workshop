from cs.structures import LinearProbing


class TestLinearProbing:
    @staticmethod
    def test_print_hash_table() -> None:
        n = 5
        hash_table = LinearProbing[int, int](n)
        for i in range(n):
            hash_table.insert(i, i)
        hash_table.remove(1)

        assert str(hash_table) == "".join(
            f"{i}  |  {None if i == 1 else i}\n" for i in range(n)
        )
