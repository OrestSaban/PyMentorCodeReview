import ast
from typing import List
from ..models import Finding, Category, Severity
from ..context import AnalysisContext
from .base import BaseRule

class FunctionTooLongRule(BaseRule):
    id = "function-too-long"
    title = "Function is Too Long"
    category = Category.MAINTAINABILITY
    severity = Severity.WARNING

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        for node in ast.walk(context.tree):
            if isinstance(node, ast.FunctionDef):
                if hasattr(node, 'end_lineno') and node.end_lineno and node.lineno:
                    length = node.end_lineno - node.lineno
                    if length > 30:
                        snippet = context.lines[node.lineno - 1].strip() if 0 < node.lineno <= len(context.lines) else ""
                        findings.append(
                            Finding(
                                id=self.id,
                                title=self.title,
                                category=self.category,
                                severity=self.severity,
                                line_number=node.lineno,
                                col=node.col_offset,
                                snippet=snippet,
                                explanation=f"This function is {length} lines long. While it works, long functions can be a bit tricky to read and test because they usually try to do many different things at once.",
                                suggestion="Consider breaking this function down into 2 or 3 smaller helper functions. Let each small function handle just one specific task.",
                            )
                        )
        return findings

class TooManyParametersRule(BaseRule):
    id = "too-many-parameters"
    title = "Too Many Parameters"
    category = Category.COMPLEXITY
    severity = Severity.WARNING

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        for node in ast.walk(context.tree):
            if isinstance(node, ast.FunctionDef):
                num_args = len(node.args.args)
                if num_args > 4:
                    snippet = context.lines[node.lineno - 1].strip() if 0 < node.lineno <= len(context.lines) else ""
                    findings.append(
                        Finding(
                            id=self.id,
                            title=self.title,
                            category=self.category,
                            severity=self.severity,
                            line_number=node.lineno,
                            col=node.col_offset,
                            snippet=snippet,
                            explanation=f"This function takes {num_args} parameters. When a function needs this much information to work, it might be doing too many tasks at once. It also makes it easier to accidentally pass the wrong data.",
                            suggestion="See if you can group related parameters into a single structure (like a dictionary or dataclass), or break the function into smaller pieces.",
                        )
                    )
        return findings

class TooManyLocalVariablesRule(BaseRule):
    id = "too-many-local-variables"
    title = "Too Many Local Variables"
    category = Category.COMPLEXITY
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        for node in ast.walk(context.tree):
            if isinstance(node, ast.FunctionDef):
                locals_set = set()
                
                class LocalVisitor(ast.NodeVisitor):
                    def visit_FunctionDef(self, n):
                        if n is not node: return
                        self.generic_visit(n)
                    def visit_AsyncFunctionDef(self, n):
                        if n is not node: return
                        self.generic_visit(n)
                    def visit_ClassDef(self, n):
                        return
                    def visit_Assign(self, n):
                        for target in n.targets:
                            if isinstance(target, ast.Name):
                                locals_set.add(target.id)
                            elif isinstance(target, (ast.Tuple, ast.List)):
                                for elt in target.elts:
                                    if isinstance(elt, ast.Name):
                                        locals_set.add(elt.id)
                        self.generic_visit(n)
                    def visit_AnnAssign(self, n):
                        if isinstance(n.target, ast.Name):
                            locals_set.add(n.target.id)
                        self.generic_visit(n)
                        
                LocalVisitor().visit(node)
                
                arg_names = {a.arg for a in node.args.args + node.args.kwonlyargs}
                if node.args.vararg: arg_names.add(node.args.vararg.arg)
                if node.args.kwarg: arg_names.add(node.args.kwarg.arg)
                
                true_locals = locals_set - arg_names
                
                if len(true_locals) > 10:
                    snippet = context.lines[node.lineno - 1].strip() if 0 < node.lineno <= len(context.lines) else ""
                    findings.append(
                        Finding(
                            id=self.id,
                            title=self.title,
                            category=self.category,
                            severity=self.severity,
                            line_number=node.lineno,
                            col=node.col_offset,
                            snippet=snippet,
                            explanation=f"This function creates {len(true_locals)} local variables. Many local variables can be a sign that a function is doing too many steps.",
                            suggestion="Splitting the logic into smaller helper functions can make the code easier to read and test.",
                        )
                    )
        return findings
