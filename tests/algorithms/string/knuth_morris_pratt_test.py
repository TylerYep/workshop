from src.algorithms import kmp_string_match


def test_knuth_morris_pratt() -> None:
    assert kmp_string_match("0101", "0011001011") == 5
    assert kmp_string_match("abc1abc12", "alskfjaldsabc1abc1abc12k23adsfabcabc") == 14
    assert kmp_string_match("abc1abc12", "alskfjaldsk23adsfabcabc") is None
    assert kmp_string_match("ABABX", "ABABZABABYABABX") == 10
    assert kmp_string_match("AAAB", "ABAAAAAB") == 4
    assert kmp_string_match("abcdabcy", "abcxabcdabxabcdabcdabcy") == 15
