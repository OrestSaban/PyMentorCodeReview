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

class NonSnakeCaseVariableRule(BaseRule):
    id = "non-snake-case-variable"
    title = "Variable Name Not Snake Case"
    category = Category.NAMING
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        snake_case_pattern = re.compile(r'^[a-z_][a-z0-9_]*$')
        upper_case_pattern = re.compile(r'^[A-Z0-9_]+$')
        
        found_vars: Dict[str, List[tuple]] = {}
        
        for node in ast.walk(context.tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                var_name = node.id
                if var_name != '_' and not snake_case_pattern.match(var_name) and not upper_case_pattern.match(var_name):
                    if var_name not in found_vars: found_vars[var_name] = []
                    found_vars[var_name].append((node.lineno, node.col_offset))
            elif isinstance(node, ast.arg):
                var_name = node.arg
                if var_name != '_' and not snake_case_pattern.match(var_name) and not upper_case_pattern.match(var_name):
                    if var_name not in found_vars: found_vars[var_name] = []
                    found_vars[var_name].append((node.lineno, node.col_offset))
                    
        for name, instances in found_vars.items():
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
                    explanation=f"The variable name '{name}' contains uppercase letters. In Python, the community convention is to use all lowercase letters with underscores for regular variables (like 'user_name').",
                    suggestion="Try renaming this variable to be all lowercase, using underscores to separate words.",
                    example=f"user_name = 'Alex'  # Good\n{name} = 'Alex'  # Bad"
                )
            )
        return findings

class ConstantNotUppercaseRule(BaseRule):
    id = "constant-not-uppercase"
    title = "Constant Not Uppercase"
    category = Category.NAMING
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()
        
        config_keywords = ['max_', 'min_', 'default_', 'tax_', 'rate', 'limit', 'threshold', 'timeout', 'retry', 'retries', 'api_url']
        upper_case_pattern = re.compile(r'^[A-Z0-9_]+$')

        if isinstance(context.tree, ast.Module):
            for stmt in context.tree.body:
                if isinstance(stmt, ast.Assign):
                    for target in stmt.targets:
                        if isinstance(target, ast.Name):
                            var_name = target.id
                            
                            is_config_like = any(kw in var_name.lower() for kw in config_keywords)
                            if is_config_like and not upper_case_pattern.match(var_name):
                                if hasattr(stmt, 'lineno'):
                                    lineno = stmt.lineno
                                    col = target.col_offset
                                    all_lines.add(lineno)
                                    snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                                    occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet, value=var_name))

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
                    explanation="This top-level variable looks like a configuration value or constant, but it is written in lowercase. In Python, constants are typically written in ALL_CAPS.",
                    suggestion="Rename this constant to be fully uppercase so other programmers immediately know it's a fixed value.",
                    example="MAX_RETRIES = 3  # Good\nmax_retries = 3  # Bad"
                )
            )
        return findings

class ShadowingBuiltinNameRule(BaseRule):
    id = "shadowing-builtin-name"
    title = "Shadowing Built-in Name"
    category = Category.NAMING
    severity = Severity.WARNING

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        found_builtins: Dict[str, List[tuple]] = {}
        builtins = {'list', 'dict', 'set', 'str', 'int', 'float', 'sum', 'min', 'max', 'input', 'id', 'type', 'file', 'object'}

        for node in ast.walk(context.tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                if node.id in builtins:
                    if node.id not in found_builtins: found_builtins[node.id] = []
                    found_builtins[node.id].append((node.lineno, node.col_offset))
            elif isinstance(node, ast.arg):
                if node.arg in builtins:
                    if node.arg not in found_builtins: found_builtins[node.arg] = []
                    found_builtins[node.arg].append((node.lineno, node.col_offset))

        for name, instances in found_builtins.items():
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
                    explanation=f"The name '{name}' is already used by Python for a built-in function or type. Using names like this can hide Python's built-ins and cause confusing bugs later.",
                    suggestion=f"Try renaming '{name}' to something more specific, like 'my_{name}' or 'user_{name}'.",
                    example=f"items_list = [1, 2, 3]  # Good\n{name} = [1, 2, 3]  # Bad"
                )
            )
        return findings

class UnclearFunctionNameRule(BaseRule):
    id = "unclear-function-name"
    title = "Unclear Function Name"
    category = Category.NAMING
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()
        
        generic_names = {'do_it', 'process', 'handle', 'stuff', 'func', 'run', 'main_function'}

        for node in ast.walk(context.tree):
            if isinstance(node, ast.FunctionDef):
                if node.name in generic_names:
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
                    explanation="This function's name is very generic. A good function name should describe exactly what the function does.",
                    suggestion="Try renaming this function to be more descriptive. For example, 'process_order' or 'handle_error' is better than just 'process' or 'handle'.",
                    example="def process_order():  # Good\ndef process():  # Bad"
                )
            )
        return findings
