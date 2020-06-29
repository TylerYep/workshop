from src.algorithms.sais import (
    get_suffix_annotations,
    induced_sort,
    sais,
    to_rank_array,
)
from src.structures.suffix_array import SuffixArray


def test_suffix_array():
    text = "AAAAACACAG"
    s = SuffixArray(text)
    assert str(s) == str(sorted([s.text[suffix:] for suffix in s.suffix_arr]))


def run_sais(orig_text, expected_suffix_arr):
    text = to_rank_array(orig_text)
    suffix_arr = sais(text)
    assert suffix_arr == expected_suffix_arr


def test_nonsense():
    run_sais("nonsense", [8, 7, 4, 0, 5, 2, 1, 6, 3])


def test_mississippi():
    run_sais("mmiissiissiippii", [16, 15, 14, 10, 6, 2, 11, 7, 3, 1, 0, 13, 12, 9, 5, 8, 4])


def test_lecture_example():
    run_sais(
        "GTCCCGATGTCATGTCAGGA",
        [20, 19, 16, 11, 6, 15, 10, 2, 3, 4, 18, 5, 17, 13, 8, 0, 14, 9, 1, 12, 7],
    )


class TestAssignmentSpec:
    @staticmethod
    def test_assignment_spec():
        run_sais(
            "ACGTGCCTAGCCTACCGTGCC",
            [21, 13, 0, 8, 20, 19, 14, 10, 5, 15, 1, 11, 6, 18, 9, 4, 16, 2, 12, 7, 17, 3],
        )

    @staticmethod
    def test_induced_sort():
        text = to_rank_array("ACGTGCCTAGCCTACCGTGCC")
        suffix_marks, lms_suffixes = get_suffix_annotations(text)
        suffix_arr = induced_sort(text, suffix_marks, lms_suffixes)
        assert suffix_arr == [
            21,
            13,
            0,
            8,
            20,
            19,
            14,
            5,
            10,
            15,
            1,
            6,
            11,
            18,
            4,
            9,
            16,
            2,
            7,
            12,
            17,
            3,
        ]

        suffix_arr = induced_sort(text, suffix_marks, [21, 13, 8, 10, 5])
        assert suffix_arr == [
            21,
            13,
            0,
            8,
            20,
            19,
            14,
            10,
            5,
            15,
            1,
            11,
            6,
            18,
            9,
            4,
            16,
            2,
            12,
            7,
            17,
            3,
        ]


def test_failed_edge_case1():
    run_sais("AAAAAGAGAC", [10, 0, 1, 2, 3, 8, 6, 4, 9, 7, 5])


class TestEdgeCase2:
    @staticmethod
    def test_failed_edge_case2():
        run_sais("AAAAACACAG", [10, 0, 1, 2, 3, 4, 6, 8, 5, 7, 9])

    @staticmethod
    def test_induced_sort_edge_case_2():
        text = to_rank_array("AAAAACACAG")
        suffix_marks, lms_suffixes = get_suffix_annotations(text)
        suffix_arr = induced_sort(text, suffix_marks, lms_suffixes)
        assert suffix_arr == [10, 0, 1, 2, 3, 4, 6, 8, 5, 7, 9]

        # [6, 10, 8], [6, 8, 10], [10, 6, 8] works
        # [8, 10, 6], [10, 8, 6], [8, 6, 10] doesn't

        suffix_arr = induced_sort(text, suffix_marks, [10, 6, 8])
        assert suffix_arr == [10, 0, 1, 2, 3, 4, 6, 8, 5, 7, 9]
