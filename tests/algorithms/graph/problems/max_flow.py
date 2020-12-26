from typing import Any, Callable

from src.structures import Graph, V

MaxFlowFunction = Callable[[Graph[V], V, V], float]


class TestMaxFlow:
    @staticmethod
    def all_test_scenarios(max_flow_fn: MaxFlowFunction[Any]) -> None:
        TestMaxFlow.matrix(max_flow_fn)
        TestMaxFlow.brilliant(max_flow_fn)

    @staticmethod
    def matrix(max_flow_fn: MaxFlowFunction[Any]) -> None:
        graph = Graph.from_matrix(
            [
                [0, 16, 13, 0, 0, 0],
                [0, 0, 10, 12, 0, 0],
                [0, 4, 0, 0, 14, 0],
                [0, 0, 9, 0, 0, 20],
                [0, 0, 0, 7, 0, 4],
                [0, 0, 0, 0, 0, 0],
            ],
        )

        assert max_flow_fn(graph, 0, 5) == 23

    @staticmethod
    def brilliant(max_flow_fn: MaxFlowFunction[Any]) -> None:
        graph = Graph[str]()
        for letter in ("s", "t", "a", "b", "c", "d"):
            graph.add_node(letter)
        graph.add_edge("s", "a", 4)
        graph.add_edge("a", "b", 4)
        graph.add_edge("b", "t", 2)
        graph.add_edge("s", "c", 3)
        graph.add_edge("c", "d", 6)
        graph.add_edge("d", "t", 6)
        graph.add_edge("b", "c", 3)

        assert max_flow_fn(graph, "s", "t") == 7
