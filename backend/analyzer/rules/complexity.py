import ast
from typing import List
from ..models import Finding, Occurrence, Category, Severity
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

class TooManyBranchesRule(BaseRule):
    id = "too-many-branches"
    title = "Too Many Branches"
    category = Category.COMPLEXITY
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        class BranchVisitor(ast.NodeVisitor):
            def __init__(self):
                self.branches = 0

            def visit_If(self, node):
                self.branches += 1
                if node.orelse and not (len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If)):
                    self.branches += 1
                self.generic_visit(node)
                
            def visit_For(self, node):
                self.branches += 1
                self.generic_visit(node)
                
            def visit_While(self, node):
                self.branches += 1
                self.generic_visit(node)

        for node in ast.walk(context.tree):
            if isinstance(node, ast.FunctionDef):
                visitor = BranchVisitor()
                visitor.visit(node)
                
                if visitor.branches > 5:
                    if hasattr(node, 'lineno'):
                        lineno = node.lineno
                        col = node.col_offset
                        all_lines.add(lineno)
                        snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                        occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet, value=node.name))

        if occurrences:
            occurrences.sort(key=lambda o: (o.line, o.col or 0))
            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=sorted(list(all_lines)),
                    occurrences=occurrences,
                    explanation="Many branches can make a function harder to read and maintain. When there are many paths, it is difficult to keep track of all possible outcomes.",
                    suggestion="Sometimes a dictionary mapping, a helper function, or an early return structure can make the logic clearer and flatter.",
                )
            )
        return findings

class ComplexBooleanConditionRule(BaseRule):
    id = "complex-boolean-condition"
    title = "Complex Boolean Condition"
    category = Category.COMPLEXITY
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        def count_terms(node):
            if isinstance(node, ast.BoolOp):
                return sum(count_terms(v) for v in node.values)
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
                return count_terms(node.operand)
            elif isinstance(node, ast.Compare):
                return max(1, len(node.comparators))
            else:
                return 1

        for node in ast.walk(context.tree):
            if isinstance(node, (ast.If, ast.While)):
                terms = count_terms(node.test)
                if terms > 4:
                    if hasattr(node, 'lineno'):
                        lineno = node.lineno
                        col = node.col_offset
                        all_lines.add(lineno)
                        snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                        occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet))

        if occurrences:
            occurrences.sort(key=lambda o: (o.line, o.col or 0))
            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=sorted(list(all_lines)),
                    occurrences=occurrences,
                    explanation="A long condition can be difficult to understand at a glance. When many boolean parts (and/or) are combined, it's easy to make a logic mistake.",
                    suggestion="Naming parts of the condition by assigning them to variables can make the code much easier to read (e.g., 'is_adult = age >= 18').",
                )
            )
        return findings

class UnnecessaryElseAfterReturnRule(BaseRule):
    id = "unnecessary-else-after-return"
    title = "Unnecessary Else After Return"
    category = Category.COMPLEXITY
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        for node in ast.walk(context.tree):
            if isinstance(node, ast.If):
                if node.orelse and node.body:
                    last_stmt = node.body[-1]
                    if isinstance(last_stmt, (ast.Return, ast.Raise)):
                        if hasattr(node, 'lineno'):
                            lineno = node.lineno
                            col = node.col_offset
                            all_lines.add(lineno)
                            snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                            occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet))

        if occurrences:
            occurrences.sort(key=lambda o: (o.line, o.col or 0))
            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=sorted(list(all_lines)),
                    occurrences=occurrences,
                    explanation="When an 'if' branch already ends with a 'return', the 'else' is often unnecessary because the function would have already exited.",
                    suggestion="Removing the 'else' and un-indenting its code can make your logic flatter and easier to read.",
                    example="if ready:\n    return True\nreturn False  # Good"
                )
            )
        return findings
