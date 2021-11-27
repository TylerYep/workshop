import pytest

from cs.algorithms import ford_max_flow
from tests.algorithms.graph.problems.max_flow import MaxFlow


@pytest.mark.add_function("max_flow_fn")
class TestFordFulkerson(MaxFlow):
    max_flow_fn = ford_max_flow
