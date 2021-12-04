# from .rabbit import play_game
# import pytest


# class TestRabbitFinder3000:
#     @staticmethod
#     @pytest.mark.parametrize("holes,expected_guesses", [(2, 2), (3, 2), (4, 4)])
#     def test_n_holes(holes: int, expected_guesses: int) -> None:
#         simulate_worst_case = max(
#             play_game(holes, use_algorithm=True) for _ in range(20)
#         )
#         assert simulate_worst_case == expected_guesses
