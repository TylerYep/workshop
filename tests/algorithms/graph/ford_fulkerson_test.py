from typing import Any

from conftest import add_fixtures
from src.algorithms import ford_max_flow
from tests.algorithms.graph.problems.max_flow import MaxFlow


class TestFordFulkerson(MaxFlow):
    max_flow_fn = ford_max_flow


def pytest_generate_tests(metafunc: Any) -> None:
    add_fixtures(metafunc, "max_flow_fn")
