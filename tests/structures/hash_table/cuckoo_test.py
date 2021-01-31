from cs.structures import Cuckoo


class TestCuckoo:
    @staticmethod
    def test_print_hash_table() -> None:
        n = 5
        hash_table = Cuckoo[int, int](n)
        for i in range(n):
            hash_table.insert(i, i)

        assert str(hash_table) == (
            "0  |  1              0  |  3\n" "1  |  0              1  |  4\n"
        )
