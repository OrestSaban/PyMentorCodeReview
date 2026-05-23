import ast
import re
from typing import List, Dict, Set, Tuple
from ..models import Finding, Occurrence, Category, Severity
from ..context import AnalysisContext
from .base import BaseRule

class LargeTopLevelScriptRule(BaseRule):
    id = "large-top-level-script"
    title = "Large Top-Level Script"
    category = Category.MAINTAINABILITY
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        executable_stmts = 0

        # Count statements at the top level
        for node in context.tree.body:
            # Ignore function definitions, class definitions, imports
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)):
                continue
                
            # Ignore simple constants/docstrings
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                continue
                
            executable_stmts += 1

            if hasattr(node, 'lineno'):
                all_lines.add(node.lineno)

        if executable_stmts > 5:
            lines_sorted = sorted(list(all_lines))
            for lineno in lines_sorted[:3]: # show first 3
                snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                occurrences.append(Occurrence(line=lineno, col=0, snippet=snippet))
            
            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=lines_sorted,
                    occurrences=occurrences,
                    explanation="Putting too much logic at the top level can make code harder to test and reuse.",
                    suggestion="Moving logic into functions makes the program easier to understand.",
                )
            )
        return findings

class GlobalVariableModificationRule(BaseRule):
    id = "global-variable-modification"
    title = "Global Variable Modification"
    category = Category.MAINTAINABILITY
    severity = Severity.WARNING

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        for node in ast.walk(context.tree):
            if isinstance(node, ast.Global):
                if hasattr(node, 'lineno'):
                    lineno = node.lineno
                    col = node.col_offset
                    all_lines.add(lineno)
                    snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                    val = ", ".join(node.names)
                    occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet, value=val))

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
                    explanation="Changing global variables inside functions can make code harder to follow because the function changes values outside itself.",
                    suggestion="Passing values in and returning new values is often clearer.",
                )
            )
        return findings

class DuplicateStringLiteralRule(BaseRule):
    id = "duplicate-string-literal"
    title = "Duplicate String Literal"
    category = Category.MAINTAINABILITY
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        
        string_counts: Dict[str, List[Tuple[int, int]]] = {}
        ignore_strings = {"yes", "no", "ok", "true", "false", "none", "error"}

        for node in ast.walk(context.tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                val = node.value
                val_lower = val.lower()
                if len(val) >= 4 and val_lower not in ignore_strings:
                    if hasattr(node, 'lineno'):
                        if val not in string_counts:
                            string_counts[val] = []
                        string_counts[val].append((node.lineno, node.col_offset))

        all_occurrences = []
        all_lines = set()
        
        for val, instances in string_counts.items():
            if len(instances) >= 3:
                for lineno, col in instances:
                    all_lines.add(lineno)
                    snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                    all_occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet, value=val))

        if all_occurrences:
            all_occurrences.sort(key=lambda o: (o.line, o.col or 0))
            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=sorted(list(all_lines)),
                    occurrences=all_occurrences,
                    explanation="Repeating the same meaningful text in many places can make code harder to change later.",
                    suggestion="A named constant can make the meaning clearer.",
                )
            )
        return findings

class TodoCommentRule(BaseRule):
    id = "todo-comment"
    title = "TODO Comment"
    category = Category.MAINTAINABILITY
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        todo_pattern = re.compile(r'#\s*(TODO|FIXME|HACK)\b', re.IGNORECASE)

        for i, line in enumerate(context.lines):
            match = todo_pattern.search(line)
            if match:
                lineno = i + 1
                col = match.start()
                all_lines.add(lineno)
                snippet = line.strip()
                occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet, value=match.group(1).upper()))

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
                    explanation="TODO and FIXME comments are useful while developing, but before finalizing a project it is good to review them.",
                    suggestion="Decide whether they should be fixed, removed, or tracked as future work.",
                )
            )
        return findings
