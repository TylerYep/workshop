from src.structures import SuffixArray


def test_suffix_array() -> None:
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


def test_print_suffix_array() -> None:
    s = SuffixArray("angrykangaroo")

    assert str(s) == (
        "['$', 'angaroo$', 'angrykangaroo$', 'aroo$', 'garoo$', "
        "'grykangaroo$', 'kangaroo$', 'ngaroo$', 'ngrykangaroo$', "
        "'o$', 'oo$', 'roo$', 'rykangaroo$', 'ykangaroo$']"
    )
