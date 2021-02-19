import argparse
import ast
import pprint
from collections import defaultdict

from cs.structures import Graph

IGNORED = dir(__builtins__) + [
    "defaultdict",
    "Decimal",
    "Http404",
    "LOGGER",
    "ValidationError",
    "APIException",
    "STATS_CLIENT",
]


def should_add(result: str) -> bool:
    return result and result not in IGNORED and "{}" not in result


def recurse_to_function_name(ast_node) -> str:
    if isinstance(ast_node, str):
        return ast_node
    if isinstance(ast_node, ast.Name):
        return ast_node.id
    if isinstance(ast_node, ast.Call):
        return recurse_to_function_name(ast_node.func)
    if isinstance(ast_node, (ast.Attribute, ast.Constant, ast.Subscript)):
        # These are not real functions!
        return ""
    return ast_node


def run(filename: str) -> None:
    with open(filename) as f:
        tree = ast.parse(f.read())
        functions = defaultdict(list)
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            for body_node in node.body:
                for node2 in ast.walk(body_node):
                    if not isinstance(node2, ast.Call):
                        continue
                    result = recurse_to_function_name(node2.func)
                    if should_add(result):
                        functions[node.name].append(result)

        function_adj_graph = dict(functions)
        pprint.pprint(function_adj_graph)
        graph = Graph(function_adj_graph)
        graph.to_graphviz()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()

    run(args.filename)
