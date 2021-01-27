from collections.abc import Callable
from typing import Any

from cs.structures import Edge, Graph, V

INF = Graph.INFINITY
SingleSourceFunction = Callable[[Graph[V], V], dict[V, float]]
APSPFunction = Callable[[Graph[V]], dict[V, dict[V, float]]]


class AllPairsShortestPaths:
    # pylint: disable=no-self-use
    @staticmethod
    def single_source_to_all_pairs(
        shortest_paths_fn: SingleSourceFunction[V],
    ) -> APSPFunction[V]:
        return lambda graph: {start: shortest_paths_fn(graph, start) for start in graph}

    # @staticmethod
    def test_no_paths(self, shortest_paths_fn: APSPFunction[Any]) -> None:
        graph = Graph[str]({"a": {}, "b": {}, "c": {}})

        assert shortest_paths_fn(graph) == {
            "a": {"a": 0, "b": INF, "c": INF},
            "b": {"a": INF, "b": 0, "c": INF},
            "c": {"a": INF, "b": INF, "c": 0},
        }

    # @staticmethod
    def test_adj_list_neg_weights(self, shortest_paths_fn: APSPFunction[Any]) -> None:
        graph = Graph[str](
            {
                "a": {"b": -1, "c": 4},
                "b": {"c": 3, "d": 2, "e": 2},
                "c": {},
                "d": {"b": 1, "c": 5},
                "e": {"d": -3},
            }
        )

        assert shortest_paths_fn(graph) == {
            "a": {"a": 0, "b": -1, "c": 2, "d": -2, "e": 1},
            "b": {"a": INF, "b": 0, "c": 3, "d": -1, "e": 2},
            "c": {"a": INF, "b": INF, "c": 0, "d": INF, "e": INF},
            "d": {"a": INF, "b": 1, "c": 4, "d": 0, "e": 3},
            "e": {"a": INF, "b": -2, "c": 1, "d": -3, "e": 0},
        }

        graph = Graph[str](
            {
                "S": {"A": 6},
                "A": {"B": 3},
                "B": {"C": 4, "E": 5},
                "C": {"A": -3, "D": 3},
                "D": {},
                "E": {},
            }
        )

        assert shortest_paths_fn(graph) == {
            "A": {"A": 0, "B": 3, "C": 7, "D": 10, "E": 8, "S": INF},
            "B": {"A": 1, "B": 0, "C": 4, "D": 7, "E": 5, "S": INF},
            "C": {"A": -3, "B": 0, "C": 0, "D": 3, "E": 5, "S": INF},
            "D": {"A": INF, "B": INF, "C": INF, "D": 0, "E": INF, "S": INF},
            "E": {"A": INF, "B": INF, "C": INF, "D": INF, "E": 0, "S": INF},
            "S": {"A": 6, "B": 9, "C": 13, "D": 16, "E": 14, "S": 0},
        }

    # @staticmethod
    def test_adj_list(self, shortest_paths_fn: APSPFunction[Any]) -> None:
        graph = Graph[str](
            {
                "A": {"B": 2, "C": 5},
                "B": {"A": 2, "D": 3, "E": 1, "F": 1},
                "C": {"A": 5, "F": 3},
                "D": {"B": 3},
                "E": {"B": 4, "F": 3},
                "F": {"C": 3, "E": 3},
            }
        )

        assert shortest_paths_fn(graph) == {
            "A": {"A": 0, "B": 2, "C": 5, "D": 5, "E": 3, "F": 3},
            "B": {"A": 2, "B": 0, "C": 4, "D": 3, "E": 1, "F": 1},
            "C": {"A": 5, "B": 7, "C": 0, "D": 10, "E": 6, "F": 3},
            "D": {"A": 5, "B": 3, "C": 7, "D": 0, "E": 4, "F": 4},
            "E": {"A": 6, "B": 4, "C": 6, "D": 7, "E": 0, "F": 3},
            "F": {"A": 8, "B": 7, "C": 3, "D": 10, "E": 3, "F": 0},
        }

        graph = Graph[str](
            {
                "B": {"C": 1},
                "C": {"D": 1},
                "D": {"F": 1},
                "E": {"B": 1, "G": 2},
                "F": {},
                "G": {"F": 1},
            }
        )

        assert shortest_paths_fn(graph) == {
            "B": {"B": 0, "C": 1, "D": 2, "E": INF, "F": 3, "G": INF},
            "C": {"B": INF, "C": 0, "D": 1, "E": INF, "F": 2, "G": INF},
            "D": {"B": INF, "C": INF, "D": 0, "E": INF, "F": 1, "G": INF},
            "E": {"B": 1, "C": 2, "D": 3, "E": 0, "F": 3, "G": 2},
            "F": {"B": INF, "C": INF, "D": INF, "E": INF, "F": 0, "G": INF},
            "G": {"B": INF, "C": INF, "D": INF, "E": INF, "F": 1, "G": 0},
        }

        graph2 = Graph[int]({2: {3: 1}, 3: {4: 1}, 4: {6: 1}, 5: {2: 1, 6: 3}, 6: {}})

        assert shortest_paths_fn(graph2) == {
            2: {2: 0, 3: 1, 4: 2, 5: INF, 6: 3},
            3: {2: INF, 3: 0, 4: 1, 5: INF, 6: 2},
            4: {2: INF, 3: INF, 4: 0, 5: INF, 6: 1},
            5: {2: 1, 3: 2, 4: 3, 5: 0, 6: 3},
            6: {2: INF, 3: INF, 4: INF, 5: INF, 6: 0},
        }

    # @staticmethod
    def edge_list(self, shortest_paths_fn: APSPFunction[Any]) -> None:
        e01 = Edge(0, 1, -1)
        e05 = Edge(0, 5, 2)
        e12 = Edge(1, 2, 2)
        e15 = Edge(1, 5, -2)
        e23 = Edge(2, 3, 5)
        e24 = Edge(2, 4, 1)
        e43 = Edge(4, 3, -4)
        e45 = Edge(4, 5, 3)
        e51 = Edge(5, 1, 2)
        e52 = Edge(5, 2, 3)
        graph = Graph.from_edgelist([e01, e05, e12, e15, e23, e24, e43, e45, e51, e52])

        assert shortest_paths_fn(graph) == {
            0: {0: 0, 1: -1, 2: 0, 3: -3, 4: 1, 5: -3},
            1: {0: INF, 1: 0, 2: 1, 3: -2, 4: 2, 5: -2},
            2: {0: INF, 1: 6, 2: 0, 3: -3, 4: 1, 5: 4},
            3: {0: INF, 1: INF, 2: INF, 3: 0, 4: INF, 5: INF},
            4: {0: INF, 1: 5, 2: 6, 3: -4, 4: 0, 5: 3},
            5: {0: INF, 1: 2, 2: 3, 3: 0, 4: 4, 5: 0},
        }

    # @staticmethod
    def test_matrix(self, shortest_paths_fn: APSPFunction[Any]) -> None:
        graph = Graph.from_matrix(
            [[0, 5, INF, 10], [INF, 0, 3, INF], [INF, INF, 0, 1], [INF, INF, INF, 0]]
        )

        assert shortest_paths_fn(graph) == {
            0: {0: 0, 1: 5, 2: 8, 3: 9},
            1: {0: INF, 1: 0, 2: 3, 3: 4},
            2: {0: INF, 1: INF, 2: 0, 3: 1},
            3: {0: INF, 1: INF, 2: INF, 3: 0},
        }
