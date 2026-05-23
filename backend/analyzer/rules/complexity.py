import ast
from typing import List
from ..models import Finding, Category, Severity
from ..context import AnalysisContext
from .base import BaseRule

class NestedIfTooDeepRule(BaseRule):
    id = "nested-if-too-deep"
    title = "Deeply Nested If Statements"
    category = Category.COMPLEXITY
    severity = Severity.WARNING

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        
        class IfDepthVisitor(ast.NodeVisitor):
            def __init__(self):
                self.current_depth = 0
                
            def visit_If(self, node):
                self.current_depth += 1
                if self.current_depth > 2:
                    snippet = context.lines[node.lineno - 1].strip() if 0 < node.lineno <= len(context.lines) else ""
                    findings.append(
                        Finding(
                            id=NestedIfTooDeepRule.id,
                            title=NestedIfTooDeepRule.title,
                            category=NestedIfTooDeepRule.category,
                            severity=NestedIfTooDeepRule.severity,
                            line_number=node.lineno,
                            col=node.col_offset,
                            snippet=snippet,
                            explanation="This 'if' statement is nested deeply inside other 'if' statements. When code leans too far to the right, it becomes harder to read because you have to remember many different conditions at the same time.",
                            suggestion="Try to return early if a condition fails, or combine related conditions using the 'and' keyword. This keeps your code closer to the left margin.",
                            example="if not valid:\n    return\nif ready:\n    do_stuff()  # Good"
                        )
                    )
                self.generic_visit(node)
                self.current_depth -= 1
                
            def visit_FunctionDef(self, node):
                old_depth = self.current_depth
                self.current_depth = 0
                self.generic_visit(node)
                self.current_depth = old_depth
                
        IfDepthVisitor().visit(context.tree)
        return findings
