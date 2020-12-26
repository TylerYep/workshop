from src.algorithms import dijkstra_search, dijkstra_shortest_paths
from src.structures import Graph
from tests.algorithms.graph.problems.all_pairs_shortest_paths import TestShortestPaths


def test_dijkstra_search() -> None:
    G = Graph[str](
        {
            "A": {"B": 2, "C": 5},
            "B": {"A": 2, "D": 3, "E": 1, "F": 1},
            "C": {"A": 5, "F": 3},
            "D": {"B": 3},
            "E": {"B": 4, "F": 3},
            "F": {"C": 3, "E": 3},
        }
    )

    G2 = Graph[int]({2: {3: 1}, 3: {4: 1}, 4: {6: 1}, 5: {2: 1, 6: 3}, 6: {}})

    G3 = Graph[str](
        {
            "B": {"C": 1},
            "C": {"D": 1},
            "D": {"F": 1},
            "E": {"B": 1, "G": 2},
            "F": {},
            "G": {"F": 1},
        }
    )

    assert dijkstra_search(G, "E", "C") == 6
    assert dijkstra_search(G2, 5, 6) == 3
    assert dijkstra_search(G3, "E", "F") == 3

    r"""
    Layout of G2:
    E -- (1) --> B -- (1) --> C
    |                         |
    (3)                       (1)
    \                       /
        F <-- (1) --- D  <--
    """

    r"""
    Layout of G3:
    E -- 1 --> B -- 1 --> C -- 1 --> D -- 1 --> F
    \                                         /\
    \                                        ||
        -------- 2 ---------> G ------- 1 ------
    """


def test_dijkstra_shortest_paths() -> None:
    TestShortestPaths.all_test_scenarios(
        TestShortestPaths.single_source_to_all_pairs(dijkstra_shortest_paths),
        negative_weights=False,
    )
