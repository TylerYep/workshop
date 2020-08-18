from src.algorithms import longest_common_subsequence


def test_lcs() -> None:
    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("ace", "ace") == 3
    assert longest_common_subsequence("abcde", "ghi") == 0
