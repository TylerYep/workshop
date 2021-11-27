import pytest

from cs.algorithms import edmonds_karp_max_flow
from tests.algorithms.graph.problems.max_flow import MaxFlow


@pytest.mark.add_function("max_flow_fn")
class TestEdmondsKarp(MaxFlow):
    max_flow_fn = edmonds_karp_max_flow
