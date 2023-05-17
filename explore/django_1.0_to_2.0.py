# pylint: skip-file
import ast
import inspect
import pathlib

import asttokens

# import black


def ForeignKey(
    to,
    on_delete,
    related_name=None,
    related_query_name=None,
    limit_choices_to=None,
    parent_link=False,
    to_field=None,
    db_constraint=True,
    **kwargs,
):
    pass


sig = inspect.signature(ForeignKey)


def walk(parent):
    for path in parent.iterdir():
        if path.is_dir():
            yield from walk(path)
        elif path.suffix == ".py":
            yield path


def get_replacements(tree):
    visitor = Visitor(tree)
    visitor.visit(tree.tree)
    return visitor.replacements


def replace(src, replacements):
    chunks = []
    end = len(src)
    for (start, stop), mod in reversed(replacements):
        chunks += [src[stop:end], mod]
        end = start
    chunks.append(src[0:end])

    return "".join(reversed(chunks))


class Visitor(ast.NodeVisitor):
    def __init__(self, tree) -> None:
        self.tree = tree
        self.replacements = []

    def visit_Call(self, node):
        self.generic_visit(node)
        if not isinstance(node.func, ast.Attribute):
            return
        if node.func.attr not in ("ForeignKey", "OneToOneField"):
            return
        args = node.args
        kwargs = {k.arg: k.value for k in node.keywords}

        bound_args = sig.bind_partial(*args, **kwargs)
        if "on_delete" in bound_args.arguments:
            return

        src = (
            f"{self.tree.get_text(node)[:-1].rstrip().rstrip(',')}, "
            "on_delete=models.CASCADE)"
        )
        self.replacements.append((self.tree.get_text_range(node), src))


for path in walk(pathlib.Path()):
    src = path.read_text()

    try:
        tree = asttokens.ASTTokens(src, filename=path, parse=True)
    except SyntaxError:
        print(f"Cannot parse {path}")
        continue

    replacements = get_replacements(tree)
    if not replacements:
        continue

    print(f"Modifying {len(replacements)} calls in {path}")
    src = replace(src, replacements)

    # src = black.format_str(src, line_length=79)
    path.write_text(src)
