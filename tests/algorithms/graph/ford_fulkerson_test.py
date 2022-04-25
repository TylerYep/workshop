import pytest

from cs.algorithms import bipartite_matching, ford_max_flow
from cs.structures.graph import Edge, Graph
from tests.algorithms.graph.problems.max_flow import MaxFlow


@pytest.mark.add_function("max_flow_fn")
class TestFordFulkerson(MaxFlow):
    max_flow_fn = ford_max_flow


class TestBipartiteMatching:
    @staticmethod
    def test_bipartite_matching() -> None:
        """
        Bipartite matching:
        .    / D
        A --/- E
        B -/-- F
        C /    .
        """
        graph = Graph[str]()
        for char in "ABCDEF":
            graph.add_node(char)
        graph.add_edge("A", "E")
        graph.add_edge("B", "E")
        graph.add_edge("B", "F")
        graph.add_edge("C", "D")
        graph.add_edge("C", "E")

        max_flow_graph, matching_edges = bipartite_matching(
            graph, ["A", "B", "C"], ["D", "E", "F"]
        )
        assert len(max_flow_graph.edges) == 11
        assert matching_edges == [Edge("A", "E"), Edge("B", "F"), Edge("C", "D")]
