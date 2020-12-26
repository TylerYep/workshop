from src.algorithms import ford_max_flow
from tests.algorithms.graph.problems.max_flow import TestMaxFlow


def test_ford_max_flow() -> None:
    TestMaxFlow.all_test_scenarios(ford_max_flow)
