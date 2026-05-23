import ast
import re
from typing import List, Dict, Set
from ..models import Finding, Occurrence, Category, Severity
from ..context import AnalysisContext
from .base import BaseRule

class UnclearVariableNameRule(BaseRule):
    id = "unclear-variable-name"
    title = "Unclear Variable Name"
    category = Category.NAMING
    severity = Severity.WARNING

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        found_unclear_names: Dict[str, List[tuple]] = {}
        unclear_names = {'x', 'y', 'a', 'b', 'temp', 'data', 'foo', 'bar'}

        for node in ast.walk(context.tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store) and node.id in unclear_names:
                    if node.id not in found_unclear_names:
                        found_unclear_names[node.id] = []
                    found_unclear_names[node.id].append((node.lineno, node.col_offset))
            elif isinstance(node, ast.arg):
                if node.arg in unclear_names:
                    if node.arg not in found_unclear_names:
                        found_unclear_names[node.arg] = []
                    found_unclear_names[node.arg].append((node.lineno, node.col_offset))

        for name, instances in found_unclear_names.items():
            unique_lines = sorted(list(set(line for line, _ in instances)))
            
            occurrences = []
            for lineno, col in instances:
                snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet, value=name))
                
            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=unique_lines,
                    occurrences=occurrences,
                    explanation=f"The variable name '{name}' is very short or generic. While this works perfectly fine for the computer, a clearer name helps other people (and future you!) understand what the value actually represents.",
                    suggestion="Try renaming this variable to describe the data it holds. For example, use 'user_age' or 'total_price' instead of just a single letter.",
                    example=f"user_age = 25  # Good\n{name} = 25  # Bad"
                )
            )
        return findings

class NonSnakeCaseFunctionRule(BaseRule):
    id = "non-snake-case-function"
    title = "Function Name Not Snake Case"
    category = Category.NAMING
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        snake_case_pattern = re.compile(r'^[a-z_][a-z0-9_]*$')
        
        for node in ast.walk(context.tree):
            if isinstance(node, ast.FunctionDef):
                if not snake_case_pattern.match(node.name):
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
                            explanation=f"The function name '{node.name}' uses capital letters. In Python, the community generally agrees to use all lowercase letters with underscores for function names. This shared style makes everyone's code easier to read together.",
                            suggestion="Try changing the name to be all lowercase, using underscores to separate words (this is called 'snake_case').",
                            example=f"def calculate_total():  # Good\ndef {node.name}():  # Bad"
                        )
                    )
        return findings
