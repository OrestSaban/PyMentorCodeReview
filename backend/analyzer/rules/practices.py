import ast
from typing import List, Dict, Set, Tuple
from ..models import Finding, Occurrence, Category, Severity
from ..context import AnalysisContext
from .base import BaseRule

class PrintInFunctionRule(BaseRule):
    id = "print-in-function"
    title = "Print Inside Function"
    category = Category.BEST_PRACTICES
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        # Store tuples of (lineno, col_offset)
        print_instances: List[Tuple[int, int]] = []
        
        class PrintVisitor(ast.NodeVisitor):
            def __init__(self):
                self.in_function = False
                
            def visit_FunctionDef(self, node):
                old_in_function = self.in_function
                self.in_function = True
                self.generic_visit(node)
                self.in_function = old_in_function
                
            def visit_Call(self, node):
                if self.in_function and isinstance(node.func, ast.Name) and node.func.id == 'print':
                    if hasattr(node, 'lineno'):
                        print_instances.append((node.lineno, node.col_offset))
                self.generic_visit(node)
                
        PrintVisitor().visit(context.tree)

        if print_instances:
            unique_lines = sorted(list(set(line for line, _ in print_instances)))
            occurrences = []
            for lineno, col in print_instances:
                snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet))

            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=unique_lines,
                    occurrences=occurrences,
                    explanation="This function prints a value directly to the screen. For small scripts this may be fine, but reusable functions are usually easier to use and test when they return their results instead of printing them.",
                    suggestion="Consider using the 'return' keyword to give the value back. Then, whoever calls the function can decide whether to print it or use it for something else.",
                    example="def add(a, b):\n    return a + b  # Good\n\ndef add(a, b):\n    print(a + b)  # Bad"
                )
            )
        return findings

class CompareBooleanRule(BaseRule):
    id = "compare-boolean"
    title = "Comparing with True/False"
    category = Category.BEST_PRACTICES
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        compare_bool_instances: List[Tuple[int, int]] = []

        for node in ast.walk(context.tree):
            if isinstance(node, ast.Compare):
                for comparator in node.comparators:
                    if isinstance(comparator, ast.Constant) and isinstance(comparator.value, bool):
                        if hasattr(node, 'lineno'):
                            compare_bool_instances.append((node.lineno, node.col_offset))
                        break

        if compare_bool_instances:
            unique_lines = sorted(list(set(line for line, _ in compare_bool_instances)))
            occurrences = []
            for lineno, col in compare_bool_instances:
                snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet))

            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=unique_lines,
                    occurrences=occurrences,
                    explanation="The code explicitly compares a value to True or False (e.g., '== True'). Python's 'if' statements already check if something is true naturally, so the extra comparison isn't needed.",
                    suggestion="You can just write 'if x:' instead of 'if x == True:'. For false checks, try 'if not x:' instead of 'if x == False:'.",
                    example="if is_valid:  # Good\nif is_valid == True:  # Bad"
                )
            )
        return findings

class BareExceptRule(BaseRule):
    id = "bare-except"
    title = "Bare Except Block"
    category = Category.BEST_PRACTICES
    severity = Severity.WARNING

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        bare_except_instances: List[Tuple[int, int]] = []

        for node in ast.walk(context.tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    if hasattr(node, 'lineno'):
                        bare_except_instances.append((node.lineno, node.col_offset))

        if bare_except_instances:
            unique_lines = sorted(list(set(line for line, _ in bare_except_instances)))
            occurrences = []
            for lineno, col in bare_except_instances:
                snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet))

            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=unique_lines,
                    occurrences=occurrences,
                    explanation="The code uses a bare 'except:' block. This catches absolutely every type of error—even if the user tries to safely exit the program (like pressing Ctrl+C). This can sometimes hide unexpected bugs.",
                    suggestion="Try to catch the specific error you expect, like 'except ValueError:'. If you want to catch all normal code errors, use 'except Exception:'.",
                    example="except ValueError:  # Good\nexcept:  # Bad"
                )
            )
        return findings

class UseEvalRule(BaseRule):
    id = "use-eval"
    title = "Avoid Using eval()"
    category = Category.BEST_PRACTICES
    severity = Severity.ERROR

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        eval_instances: List[Tuple[int, int]] = []

        for node in ast.walk(context.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'eval':
                if hasattr(node, 'lineno'):
                    eval_instances.append((node.lineno, node.col_offset))

        if eval_instances:
            unique_lines = sorted(list(set(line for line, _ in eval_instances)))
            occurrences = []
            for lineno, col in eval_instances:
                snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet))

            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=unique_lines,
                    occurrences=occurrences,
                    explanation="The code uses the 'eval()' function. While 'eval' is powerful, it can be risky because it runs any text as actual Python code. If that text comes from a user, it could run harmful commands.",
                    suggestion="It's best to avoid 'eval()'. If you need to read structured data, try safer tools like 'ast.literal_eval()' or the 'json' module.",
                )
            )
        return findings

class MagicNumberRule(BaseRule):
    id = "magic-number"
    title = "Magic Number"
    category = Category.BEST_PRACTICES
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        # Store string_value -> list of (lineno, col_offset)
        magic_numbers: Dict[str, List[Tuple[int, int]]] = {}

        for node in ast.walk(context.tree):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                    allowed_numbers = {0, 1, -1, 2, 10, 100, 0.0, 1.0}
                    if node.value not in allowed_numbers:
                        parent = getattr(node, 'parent', None)
                        
                        is_upper_assign = False
                        if isinstance(parent, ast.Assign) and getattr(parent, 'value', None) is node:
                            for target in parent.targets:
                                if isinstance(target, ast.Name) and target.id.isupper():
                                    is_upper_assign = True
                                    break
                        if is_upper_assign:
                            continue
                            
                        if isinstance(parent, ast.Call) and isinstance(parent.func, ast.Name) and parent.func.id == 'range':
                            continue
                            
                        if isinstance(parent, (ast.List, ast.Tuple, ast.Set)):
                            continue
                            
                        if isinstance(parent, ast.Subscript) and getattr(parent, 'slice', None) is node:
                            continue
                        if isinstance(parent, ast.Index):
                            continue
                            
                        call_parent = None
                        if isinstance(parent, ast.Call):
                            call_parent = parent
                        elif isinstance(parent, ast.keyword):
                            call_parent = getattr(parent, 'parent', None)

                        if isinstance(call_parent, ast.Call):
                            in_function = False
                            curr = call_parent
                            while curr is not None:
                                if isinstance(curr, ast.FunctionDef):
                                    in_function = True
                                    break
                                curr = getattr(curr, 'parent', None)
                            if not in_function:
                                continue
                            
                        val_str = str(node.value)
                        if val_str not in magic_numbers:
                            magic_numbers[val_str] = []
                        if hasattr(node, 'lineno'):
                            magic_numbers[val_str].append((node.lineno, node.col_offset))

        if magic_numbers:
            all_lines = set()
            occurrences = []
            values = []
            
            for val, instances in magic_numbers.items():
                values.append(val)
                for lineno, col in instances:
                    all_lines.add(lineno)
                    snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                    occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet, value=val))
                
            val_str = ", ".join(sorted(values))
            
            # Sort occurrences by line number to keep it clean
            occurrences.sort(key=lambda o: (o.line, o.col or 0))
            
            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=sorted(list(all_lines)),
                    occurrences=occurrences,
                    explanation=f"The number {val_str} is used directly in the code without a name. Numbers like this can make the code harder to read later, because other people might not know what {val_str} means in this context.",
                    suggestion="Try assigning this number to a named variable at the top of your file or function. A descriptive name makes the purpose clear!",
                    example="MAX_RETRIES = 5\nif tries > MAX_RETRIES:  # Good\nif tries > 5:  # Bad"
                )
            )
        return findings

class MutableDefaultArgumentRule(BaseRule):
    id = "mutable-default-argument"
    title = "Mutable Default Argument"
    category = Category.BEST_PRACTICES
    severity = Severity.WARNING

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        for node in ast.walk(context.tree):
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    is_mutable = False
                    val_str = ""
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        is_mutable = True
                        if isinstance(default, ast.List): val_str = "list"
                        elif isinstance(default, ast.Dict): val_str = "dict"
                        elif isinstance(default, ast.Set): val_str = "set"
                    elif isinstance(default, ast.Call) and isinstance(default.func, ast.Name):
                        if default.func.id in {'list', 'dict', 'set'}:
                            is_mutable = True
                            val_str = default.func.id

                    if is_mutable and hasattr(default, 'lineno'):
                        lineno = default.lineno
                        col = default.col_offset
                        all_lines.add(lineno)
                        snippet = context.lines[lineno - 1].strip() if 0 < lineno <= len(context.lines) else ""
                        occurrences.append(Occurrence(line=lineno, col=col, snippet=snippet, value=val_str))

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
                    explanation="Mutable default arguments (like lists or dictionaries) are created once when the function is defined, not each time the function is called. This can cause values to be shared unexpectedly between calls.",
                    suggestion="Use 'None' as the default value and create the new list/dict inside the function instead.",
                    example="def add(item, items=None):\n    if items is None:\n        items = []\n    items.append(item)  # Good"
                )
            )
        return findings

class UseExecRule(BaseRule):
    id = "exec-usage"
    title = "Avoid Using exec()"
    category = Category.BEST_PRACTICES
    severity = Severity.ERROR

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        for node in ast.walk(context.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'exec':
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
                    explanation="The code uses the 'exec()' function. Executing dynamic code can be unsafe and hard to debug, especially if it involves user input.",
                    suggestion="Avoid 'exec()'. Usually, there are safer and more structured ways to achieve the same result using regular Python features.",
                )
            )
        return findings

class BroadExceptionRule(BaseRule):
    id = "broad-exception"
    title = "Broad Exception Block"
    category = Category.BEST_PRACTICES
    severity = Severity.WARNING

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        for node in ast.walk(context.tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is not None and isinstance(node.type, ast.Name) and node.type.id == 'Exception':
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
                    explanation="The code uses 'except Exception:'. While better than a bare except, this is still very broad and can hide unexpected bugs.",
                    suggestion="Try to catch the most specific exception type possible (e.g., ValueError, FileNotFoundError) when you know what error might occur.",
                    example="except ValueError:  # Good\nexcept Exception:  # Bad"
                )
            )
        return findings

class MissingReturnValueRule(BaseRule):
    id = "missing-return-value"
    title = "Missing Return Value"
    category = Category.BEST_PRACTICES
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()
        
        prefixes = ('calculate', 'compute', 'get', 'find', 'create', 'build', 'convert', 'generate')

        for node in ast.walk(context.tree):
            if isinstance(node, ast.FunctionDef):
                name = node.name.lower()
                if name.startswith(prefixes):
                    has_return_val = False
                    has_logic = False
                    for child in ast.walk(node):
                        if isinstance(child, ast.Return) and child.value is not None:
                            has_return_val = True
                            break
                        if isinstance(child, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.BinOp, ast.Call)):
                            has_logic = True
                            
                    if has_logic and not has_return_val:
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
                    explanation="This function's name suggests it calculates or produces a value, but it doesn't return anything. If a function calculates a value, it usually should return it so other code can use it.",
                    suggestion="Add a 'return' statement at the end of the function to give the calculated value back to the caller.",
                    example="def calculate_total():\n    return 100  # Good"
                )
            )
        return findings

class UnusedLoopVariableRule(BaseRule):
    id = "unused-loop-variable"
    title = "Unused Loop Variable"
    category = Category.BEST_PRACTICES
    severity = Severity.INFO

    def check(self, context: AnalysisContext) -> List[Finding]:
        findings = []
        occurrences = []
        all_lines = set()

        for node in ast.walk(context.tree):
            if isinstance(node, ast.For):
                target = node.target
                names_to_check = []
                if isinstance(target, ast.Name):
                    names_to_check.append(target)
                elif isinstance(target, (ast.Tuple, ast.List)):
                    for elt in target.elts:
                        if isinstance(elt, ast.Name):
                            names_to_check.append(elt)
                            
                for name_node in names_to_check:
                    var_name = name_node.id
                    if var_name == '_':
                        continue
                        
                    is_used = False
                    for child in node.body + node.orelse:
                        for descendant in ast.walk(child):
                            if isinstance(descendant, ast.Name) and descendant.id == var_name and isinstance(descendant.ctx, ast.Load):
                                is_used = True
                                break
                        if is_used: break
                        
                    if not is_used:
                        if hasattr(node, 'lineno'):
                            lineno = node.lineno
                            col = node.col_offset
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
                    explanation="This loop creates a variable, but never actually uses it inside the loop. This can be confusing because it looks like the value is important.",
                    suggestion="If the value is intentionally unused (like when you just want to repeat an action 5 times), use an underscore '_' as the variable name. Python programmers use '_' to signal 'I don't need this value'.",
                    example="for _ in range(5):\n    print('Hello')  # Good"
                )
            )
        return findings
