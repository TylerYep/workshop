from cs.structures import Cuckoo, HashTable


class TestCuckoo:
    @staticmethod
    def test_print_hash_table() -> None:
        n = 10
        hash_table = Cuckoo[int, int](n, load_factor=1)
        for i in range(n):
            hash_table.insert(i, i)
        hash_table.remove(1)

        assert str(hash_table) == (
            "0  |  6              0  |  5\n"
            "1  |  None           1  |  2\n"
            "2  |  0              2  |  3\n"
            "3  |  9              3  |  7\n"
            "4  |  8              4  |  4\n"
        )

    @staticmethod
    def test_duplicates() -> None:
        """Test creating a hash_table and adding 100 values to it."""
        N = 2
        hash_table_1 = Cuckoo[str, int](N)
        hash_table_1["yo"] = 6
        hash_table_1["yolo"] = 8
        hash_table_2 = Cuckoo[str, int](N)
        hash_table_2["yo"] = 6
        hash_table_2["yolo"] = 8
        hash_table_2["yolo"] = 9

        # pylint: disable=protected-access
        assert len(HashTable._hash_ids) == 10  # noqa: SLF001
