from src.algorithms import dijkstra
from src.structures import Graph


def test_dijkstra() -> None:
    G = Graph[str, int](
        {
            "A": {"B": 2, "C": 5},
            "B": {"A": 2, "D": 3, "E": 1, "F": 1},
            "C": {"A": 5, "F": 3},
            "D": {"B": 3},
            "E": {"B": 4, "F": 3},
            "F": {"C": 3, "E": 3},
        }
    )

    G2 = Graph[str, int](
        {"B": {"C": 1}, "C": {"D": 1}, "D": {"F": 1}, "E": {"B": 1, "F": 3}, "F": {}}
    )

    G3 = Graph[str, int](
        {
            "B": {"C": 1},
            "C": {"D": 1},
            "D": {"F": 1},
            "E": {"B": 1, "G": 2},
            "F": {},
            "G": {"F": 1},
        }
    )

    assert dijkstra(G, "E", "C") == 6
    assert dijkstra(G2, "E", "F") == 3
    assert dijkstra(G3, "E", "F") == 3

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
