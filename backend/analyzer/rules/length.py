import ast
from typing import List
from ..models import Finding, Category, Severity
from .base import Rule

class LengthRule(Rule):
    def analyze(self, tree: ast.AST) -> List[Finding]:
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 3. Detect functions longer than 30 lines
                if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
                    length = node.end_lineno - node.lineno
                    if length > 30:
                        findings.append(
                            Finding(
                                id="function-too-long",
                                title="Function is Too Long",
                                category=Category.MAINTAINABILITY,
                                severity=Severity.WARNING,
                                line_number=node.lineno,
                                explanation=f"The function '{node.name}' is {length} lines long. Long functions are harder to read, test, and debug.",
                                suggestion="Try splitting this function into smaller, more focused helper functions. A good rule of thumb is keeping functions under 30 lines.",
                            )
                        )
                
                # 4. Detect functions with too many parameters (> 4)
                # Count regular args and kwonlyargs
                num_params = len(node.args.args) + len(node.args.kwonlyargs)
                if num_params > 4:
                    findings.append(
                        Finding(
                            id="too-many-parameters",
                            title="Too Many Parameters",
                            category=Category.COMPLEXITY,
                            severity=Severity.WARNING,
                            line_number=node.lineno,
                            explanation=f"The function '{node.name}' takes {num_params} arguments, which can be hard to remember and use correctly.",
                            suggestion="Consider grouping related parameters into a single object (like a dictionary, dataclass, or a regular class).",
                        )
                    )
        return findings
