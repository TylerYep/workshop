from src.structures.suffix_array import SuffixArray


def test_suffix_array():
    s = SuffixArray("nonsense")
    result = s.search("nse")
    assert result == [2, 5], result
    result = s.search("nonsense")
    assert result == [0], result
    result = s.search("no")
    assert result == [0], result
    result = s.search("n")
    assert result == [0, 2, 5], result
    result = s.search("")
    assert result == [0, 1, 2, 3, 4, 5, 6, 7, 8], result

    s = SuffixArray("h")
    result = s.search("h")
    assert result == [0], result