from typing import Any

from cs.algorithms import edmonds_karp_max_flow
from tests.algorithms.graph.problems.max_flow import MaxFlow
from tests.conftest import add_fixtures


class TestEdmondsKarp(MaxFlow):
    max_flow_fn = edmonds_karp_max_flow


def pytest_generate_tests(metafunc: Any) -> None:
    add_fixtures(metafunc, "max_flow_fn")
