from cs.structures import Cuckoo


class TestCuckoo:
    @staticmethod
    def test_print_hash_table() -> None:
        n = 10
        hash_table = Cuckoo[int, int](n, load_factor=1)
        for i in range(n):
            hash_table.insert(i, i)
        hash_table.remove(1)

        assert str(hash_table) == (
            "0  |  8              0  |  6\n"
            "1  |  None           1  |  2\n"
            "2  |  5              2  |  4\n"
            "3  |  3              3  |  0\n"
            "4  |  9              4  |  7\n"
        )
