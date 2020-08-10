from src.algorithms.dfs import depth_first_search, depth_first_search_recursive
from src.structures import Graph

# graph: Graph[str, str] = Graph.from_iterable({
#     '0': ['1', '2'],
#     '1': ['0', '3', '4'],
#     '2': ['0'],
#     '3': ['1'],
#     '4': ['2', '3']
# })


def test_dfs() -> None:
    graph: Graph[str, str] = Graph.from_iterable(
        {
            "A": ["B", "C"],
            "B": ["A", "D", "E"],
            "C": ["A", "F"],
            "D": ["B"],
            "E": ["B", "F"],
            "F": ["C", "E"],
        }
    )
    assert depth_first_search(graph, "A", "F") == ["A", "C", "F"]
    assert depth_first_search_recursive(graph, "A", "F") == ["A", "B", "E", "F"]
