from src.algorithms import edmonds_karp_max_flow
from tests.algorithms.graph.problems.max_flow import TestMaxFlow


def test_edmonds_karp_max_flow() -> None:
    TestMaxFlow.all_test_scenarios(edmonds_karp_max_flow)
