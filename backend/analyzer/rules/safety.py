import ast
from typing import List
from ..models import Finding, Occurrence, Category, Severity
from ..context import AnalysisContext
from .base import BaseRule

class HardcodedSecretRule(BaseRule):
    id = "hardcoded-secret"
    title = "Hardcoded Secret"
    category = Category.BEST_PRACTICES
    severity = Severity.WARNING

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        secret_keywords = ["password", "passwd", "secret", "token", "api_key", "apikey", "access_key", "private_key"]
        ignore_values = ["example", "test", "demo", "placeholder", "<password>", "your_api_key_here"]

        for node in ast.walk(context.tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id.lower()
                        if any(kw in name for kw in secret_keywords):
                            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                                val = node.value.value.lower()
                                if val != "" and val not in ignore_values and not any(ig in val for ig in ignore_values):
                                    if hasattr(node, 'lineno'):
                                        lineno = node.lineno
                                        col = node.col_offset
                                        all_lines.add(lineno)
                                        snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                                        occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet, value=target.id))
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name):
                    name = node.target.id.lower()
                    if any(kw in name for kw in secret_keywords):
                        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                            val = node.value.value.lower()
                            if val != "" and val not in ignore_values and not any(ig in val for ig in ignore_values):
                                if hasattr(node, 'lineno'):
                                    lineno = node.lineno
                                    col = node.col_offset
                                    all_lines.add(lineno)
                                    snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                                    occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet, value=node.target.id))

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
                    explanation="Secrets should not be written directly in source code because they can be accidentally committed to GitHub.",
                    suggestion="Use environment variables or a secrets manager instead.",
                )
            )
        return findings

class UnsafeYamlLoadRule(BaseRule):
    id = "unsafe-yaml-load"
    title = "Unsafe YAML Load"
    category = Category.BEST_PRACTICES
    severity = Severity.WARNING

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        for node in ast.walk(context.tree):
            if isinstance(node, ast.Call):
                is_unsafe = False
                if isinstance(node.func, ast.Attribute):
                    if getattr(node.func.value, 'id', '') == 'yaml' and node.func.attr == 'load':
                        is_unsafe = True
                        for kw in node.keywords:
                            if kw.arg == 'Loader' and getattr(kw.value, 'attr', '') == 'SafeLoader':
                                is_unsafe = False
                if is_unsafe:
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
                    explanation="yaml.load() can be unsafe with untrusted input.",
                    suggestion="yaml.safe_load() is usually safer for beginner projects.",
                )
            )
        return findings

class SubprocessShellTrueRule(BaseRule):
    id = "subprocess-shell-true"
    title = "Subprocess shell=True"
    category = Category.BEST_PRACTICES
    severity = Severity.WARNING

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        subprocess_methods = {'run', 'call', 'Popen', 'check_call', 'check_output'}

        for node in ast.walk(context.tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and getattr(node.func.value, 'id', '') == 'subprocess':
                    if node.func.attr in subprocess_methods:
                        for kw in node.keywords:
                            if kw.arg == 'shell' and isinstance(kw.value, ast.Constant) and kw.value.value is True:
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
                    explanation="shell=True can be risky if the command includes user input.",
                    suggestion="Passing command arguments as a list is usually safer.",
                )
            )
        return findings

class AssertUsedForValidationRule(BaseRule):
    id = "assert-used-for-validation"
    title = "Assert Used For Validation"
    category = Category.BEST_PRACTICES
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        val_keywords = ['user', 'input', 'request', 'data', 'password', 'token', 'age', 'amount', 'price']

        class AssertVisitor(ast.NodeVisitor):
            def __init__(self):
                self.in_test_func = False
                
            def visit_FunctionDef(self, node):
                if node.name.startswith('test_'):
                    old_test = self.in_test_func
                    self.in_test_func = True
                    self.generic_visit(node)
                    self.in_test_func = old_test
                else:
                    self.generic_visit(node)
                    
            def visit_Assert(self, node):
                if not self.in_test_func:
                    class NameVisitor(ast.NodeVisitor):
                        def __init__(self):
                            self.found = False
                        def visit_Name(self, n):
                            if any(kw in n.id.lower() for kw in val_keywords):
                                self.found = True
                    
                    nv = NameVisitor()
                    nv.visit(node.test)
                    
                    if nv.found:
                        if hasattr(node, 'lineno'):
                            lineno = node.lineno
                            col = node.col_offset
                            all_lines.add(lineno)
                            snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                            occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet))
                self.generic_visit(node)

        AssertVisitor().visit(context.tree)

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
                    explanation="assert is useful for tests and debugging, but it can be disabled when Python runs with optimizations.",
                    suggestion="For real validation, use explicit if statements and raise clear exceptions.",
                )
            )
        return findings
