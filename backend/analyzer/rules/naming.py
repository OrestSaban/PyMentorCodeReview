import ast
import re
from typing import List
from ..models import Finding, Category, Severity
from .base import Rule

class NamingRule(Rule):
    def analyze(self, tree: ast.AST) -> List[Finding]:
        findings = []
        unclear_names = {"x", "y", "a", "b", "temp", "data", "foo", "bar"}
        snake_case_pattern = re.compile(r"^[a-z_][a-z0-9_]*$")
        
        found_unclear_names = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                if node.id in unclear_names:
                    if node.id not in found_unclear_names:
                        found_unclear_names[node.id] = set()
                    if hasattr(node, "lineno"):
                        found_unclear_names[node.id].add(node.lineno)
                        
        for name, lines in found_unclear_names.items():
            findings.append(
                Finding(
                    id="unclear-variable-name",
                    title="Unclear Variable Name",
                    category=Category.NAMING,
                    severity=Severity.WARNING,
                    line_numbers=sorted(list(lines)),
                    explanation=f"The variable name '{name}' is too generic. Meaningful names make your code much easier to understand.",
                    suggestion="Rename this variable to describe what it actually holds (e.g., 'user_age' instead of 'x').",
                    example="user_age = 25  # Good\n{name} = 25  # Bad"
                )
            )
            
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not snake_case_pattern.match(node.name) and not node.name.startswith("__"):
                    findings.append(
                        Finding(
                            id="non-snake-case-function",
                            title="Function Name is not snake_case",
                            category=Category.NAMING,
                            severity=Severity.INFO,
                            line_number=getattr(node, "lineno", None),
                            explanation=f"The function '{node.name}' doesn't follow Python's naming convention. Python functions should use snake_case (lowercase words separated by underscores).",
                            suggestion=f"Rename it to something like '{self._to_snake_case(node.name)}'.",
                            example="def calculate_total():  # Good\ndef calculateTotal():  # Bad"
                        )
                    )
        return findings

    def _to_snake_case(self, name: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
