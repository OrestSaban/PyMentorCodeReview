import ast
from typing import List
from ..models import Finding, Category, Severity
from .base import Rule

class ComplexityRule(Rule):
    def analyze(self, tree: ast.AST) -> List[Finding]:
        findings = []
        
        def check_nesting(node, depth, max_depth):
            if isinstance(node, ast.If):
                if depth > max_depth:
                    findings.append(
                        Finding(
                            id="nested-if-too-deep",
                            title="Too Much Nesting",
                            category=Category.COMPLEXITY,
                            severity=Severity.WARNING,
                            line_number=node.lineno,
                            explanation="This 'if' statement is nested very deeply. Heavily nested code is hard to read and usually indicates that the logic could be simplified.",
                            suggestion="Try to return early from the function, combine conditions using 'and' / 'or', or extract the nested logic into its own helper function.",
                        )
                    )
                for child in node.body:
                    check_nesting(child, depth + 1, max_depth)
                for child in node.orelse:
                    # 'elif' is technically an 'if' inside 'orelse' in AST, but it doesn't add logical indentation depth conceptually for beginners.
                    # However, to keep it simple, we'll increment for pure nesting or handle 'elif' separately.
                    if isinstance(child, ast.If):
                        check_nesting(child, depth, max_depth) # 'elif' does not increase visual depth
                    else:
                        check_nesting(child, depth + 1, max_depth)
            else:
                for child in ast.iter_child_nodes(node):
                    check_nesting(child, depth, max_depth)
        
        for node in ast.iter_child_nodes(tree):
            check_nesting(node, 1, 2)
            
        return findings
