from src.structures import SuffixArray


class TestSuffixArray:
    @staticmethod
    def test_suffix_array() -> None:
        suffix_arr = SuffixArray("nonsense")
        result = suffix_arr.search("nse")
        assert result == [2, 5]
        result = suffix_arr.search("nonsense")
        assert result == [0]
        result = suffix_arr.search("no")
        assert result == [0]
        result = suffix_arr.search("n")
        assert result == [0, 2, 5]
        result = suffix_arr.search("")
        assert result == [0, 1, 2, 3, 4, 5, 6, 7, 8]

        suffix_arr = SuffixArray("h")
        result = suffix_arr.search("h")
        assert result == [0]

    @staticmethod
    def test_repr() -> None:
        suffix_arr = SuffixArray("angrykangaroo")

        assert str(suffix_arr) == (
            "['$', 'angaroo$', 'angrykangaroo$', 'aroo$', 'garoo$', "
            "'grykangaroo$', 'kangaroo$', 'ngaroo$', 'ngrykangaroo$', "
            "'o$', 'oo$', 'roo$', 'rykangaroo$', 'ykangaroo$']"
        )
        assert repr(suffix_arr) == "SuffixArray(text='angrykangaroo$')"
