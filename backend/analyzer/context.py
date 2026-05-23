import ast

class AnalysisContext:
    def __init__(self, code: str, tree: ast.AST):
        self.code = code
        self.lines = code.splitlines()
        self.tree = tree
        self._set_parents()

    def _set_parents(self):
        """Annotates each node with its parent node for easier traversal."""
        for node in ast.walk(self.tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
