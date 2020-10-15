from src.algorithms import kmp_string_match


def test_knuth_morris_pratt() -> None:
    assert kmp_string_match("0101", "0011001011") == 5
