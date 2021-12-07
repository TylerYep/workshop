import pytest

from cs.algorithms.rabbit import play_game


class TestRabbitFinder3000:
    @staticmethod
    @pytest.mark.parametrize("holes", [1, 2, 3, 4, 5, 10, 20, 100])
    def test_n_holes(holes: int) -> None:
        simulate_worst_case = max(
            play_game(holes, use_algorithm=True) for _ in range(20)
        )

        assert simulate_worst_case <= 2 * holes + 1
