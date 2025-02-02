import random

import pytest

from cs.structures import RMQ, FischerHeunRMQ, HybridRMQ, PrecomputedRMQ, SparseTableRMQ

parametrize_rmq_type = pytest.mark.parametrize(
    "rmq_type", ["FischerHeunRMQ", "HybridRMQ", "PrecomputedRMQ", "SparseTableRMQ"]
)


def construct_rmq(rmq_type: str, data: list[int]) -> RMQ:
    rmq_map = {
        constructor.__name__: constructor
        for constructor in (FischerHeunRMQ, HybridRMQ, PrecomputedRMQ, SparseTableRMQ)
    }
    return rmq_map[rmq_type](data)


class TestRMQ:
    @staticmethod
    @parametrize_rmq_type
    @pytest.mark.parametrize("data_range", [(0, 1), (5, 10)])
    def test_all_rmqs(rmq_type: str, data_range: tuple[int, int]) -> None:
        # Skip running FischerHeunRMQ twice.
        if rmq_type != "FischerHeunRMQ":
            run_rmq("FischerHeunRMQ", rmq_type, data_range)

    @staticmethod
    @parametrize_rmq_type
    def test_invalid_query(rmq_type: str) -> None:
        data = list(range(10))
        rmq = construct_rmq(rmq_type, data)

        with pytest.raises(RuntimeError):
            _ = rmq.rmq(6, 5)

    @staticmethod
    @pytest.mark.parametrize("data_range", [(30, 300)])
    def test_fischerheun_rmq(data_range: tuple[int, int]) -> None:
        """Separate tests to get complete test coverage of Fischer-Heun."""
        run_rmq("HybridRMQ", "FischerHeunRMQ", data_range)

    @staticmethod
    def test_calc_cart_num() -> None:
        arr = [93, 84, 33, 64, 62, 83, 63, 58]
        assert FischerHeunRMQ.calc_cart_num(arr) == int("1010110110100100"[::-1], 2)

        arr = [1, 2, 0, 4, 5]
        arr2 = [17, 34, 5, 100, 120]
        assert FischerHeunRMQ.calc_cart_num(arr) == FischerHeunRMQ.calc_cart_num(arr2)

        arr = [952, 946, 414, 894, 675, 154, 627, 154, 414]
        arr2 = [764, 319, 198, 680, 376, 113, 836, 368, 831]
        assert FischerHeunRMQ.calc_cart_num(arr) == FischerHeunRMQ.calc_cart_num(arr2)


def run_rmq(
    ref_rmq_type: str,
    proposed_rmq_type: str,
    data_range: tuple[int, int],
    num_builds: int = 5,
    num_queries: int = 10,
) -> None:
    minimum, maximum = data_range
    data = [random.randrange(minimum, maximum) for _ in range(maximum)]
    for _ in range(num_builds):
        # Compare all output to the fastest RMQ
        reference_rmq = construct_rmq(ref_rmq_type, data)
        proposed_rmq = construct_rmq(proposed_rmq_type, data)
        for _ in range(num_queries):
            low = random.randrange(minimum, maximum)
            high = random.randrange(minimum, maximum)
            if low > high:
                low, high = high, low
            high += 1

            ours = reference_rmq.rmq(low, high)
            theirs = proposed_rmq.rmq(low, high)

            assert data[ours] == data[theirs]
