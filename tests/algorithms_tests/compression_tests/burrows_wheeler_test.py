from src.algorithms.compression.burrows_wheeler import (
    all_rotations,
    bwt_transform,
    reverse_bwt,
)


def test_all_rotations() -> None:
    assert all_rotations("") == []
    assert all_rotations("^BANANA|") == [
        "^BANANA|",
        "BANANA|^",
        "ANANA|^B",
        "NANA|^BA",
        "ANA|^BAN",
        "NA|^BANA",
        "A|^BANAN",
        "|^BANANA",
    ]
    assert all_rotations("a_asa_da_casa") == [
        "a_asa_da_casa",
        "_asa_da_casaa",
        "asa_da_casaa_",
        "sa_da_casaa_a",
        "a_da_casaa_as",
        "_da_casaa_asa",
        "da_casaa_asa_",
        "a_casaa_asa_d",
        "_casaa_asa_da",
        "casaa_asa_da_",
        "asaa_asa_da_c",
        "saa_asa_da_ca",
        "aa_asa_da_cas",
    ]
    assert all_rotations("panamabanana") == [
        "panamabanana",
        "anamabananap",
        "namabananapa",
        "amabananapan",
        "mabananapana",
        "abananapanam",
        "bananapanama",
        "ananapanamab",
        "nanapanamaba",
        "anapanamaban",
        "napanamabana",
        "apanamabanan",
    ]


def test_bwt_transform() -> None:
    assert bwt_transform("^BANANA") == ("BNN^AAA", 6)
    assert bwt_transform("a_asa_da_casa") == ("aaaadss_c__aa", 3)
    assert bwt_transform("panamabanana") == ("mnpbnnaaaaaa", 11)


def test_reverse_bwt() -> None:
    assert reverse_bwt("BNN^AAA", 6) == "^BANANA"
    assert reverse_bwt("aaaadss_c__aa", 3) == "a_asa_da_casa"
    assert reverse_bwt("mnpbnnaaaaaa", 11) == "panamabanana"
