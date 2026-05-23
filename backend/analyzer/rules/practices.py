import ast
from typing import List, Dict, Set
from ..models import Finding, Category, Severity
from .base import Rule

class PrintInFunctionRule(Rule):
    id = "print-in-function"
    title = "Print Inside Function"
    category = Category.BEST_PRACTICES
    severity = Severity.INFO

    def analyze(self, tree: ast.AST) -> List[Finding]:
        findings = []
        print_lines = set()
        
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
                        print_lines.add(node.lineno)
                self.generic_visit(node)
                
        PrintVisitor().visit(tree)

        if print_lines:
            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=sorted(list(print_lines)),
                    explanation="This function prints a value directly to the screen. For small scripts this may be fine, but reusable functions are usually easier to use and test when they return their results instead of printing them.",
                    suggestion="Consider using the 'return' keyword to give the value back. Then, whoever calls the function can decide whether to print it or use it for something else.",
                    example="def add(a, b):\n    return a + b  # Good\n\ndef add(a, b):\n    print(a + b)  # Bad"
                )
            )
        return findings

class CompareBooleanRule(Rule):
    id = "compare-boolean"
    title = "Comparing with True/False"
    category = Category.BEST_PRACTICES
    severity = Severity.INFO

    def analyze(self, tree: ast.AST) -> List[Finding]:
        findings = []
        compare_bool_lines = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                for comparator in node.comparators:
                    if isinstance(comparator, ast.Constant) and isinstance(comparator.value, bool):
                        if hasattr(node, 'lineno'):
                            compare_bool_lines.add(node.lineno)
                        break

        if compare_bool_lines:
            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=sorted(list(compare_bool_lines)),
                    explanation="The code explicitly compares a value to True or False (e.g., '== True'). Python's 'if' statements already check if something is true naturally, so the extra comparison isn't needed.",
                    suggestion="You can just write 'if x:' instead of 'if x == True:'. For false checks, try 'if not x:' instead of 'if x == False:'.",
                    example="if is_valid:  # Good\nif is_valid == True:  # Bad"
                )
            )
        return findings

class BareExceptRule(Rule):
    id = "bare-except"
    title = "Bare Except Block"
    category = Category.BEST_PRACTICES
    severity = Severity.WARNING

    def analyze(self, tree: ast.AST) -> List[Finding]:
        findings = []
        bare_except_lines = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    if hasattr(node, 'lineno'):
                        bare_except_lines.add(node.lineno)

        if bare_except_lines:
            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=sorted(list(bare_except_lines)),
                    explanation="The code uses a bare 'except:' block. This catches absolutely every type of error—even if the user tries to safely exit the program (like pressing Ctrl+C). This can sometimes hide unexpected bugs.",
                    suggestion="Try to catch the specific error you expect, like 'except ValueError:'. If you want to catch all normal code errors, use 'except Exception:'.",
                    example="except ValueError:  # Good\nexcept:  # Bad"
                )
            )
        return findings

class UseEvalRule(Rule):
    id = "use-eval"
    title = "Avoid Using eval()"
    category = Category.BEST_PRACTICES
    severity = Severity.ERROR

    def analyze(self, tree: ast.AST) -> List[Finding]:
        findings = []
        eval_lines = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'eval':
                if hasattr(node, 'lineno'):
                    eval_lines.add(node.lineno)

        if eval_lines:
            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=sorted(list(eval_lines)),
                    explanation="The code uses the 'eval()' function. While 'eval' is powerful, it can be risky because it runs any text as actual Python code. If that text comes from a user, it could run harmful commands.",
                    suggestion="It's best to avoid 'eval()'. If you need to read structured data, try safer tools like 'ast.literal_eval()' or the 'json' module.",
                )
            )
        return findings

class MagicNumberRule(Rule):
    id = "magic-number"
    title = "Magic Number"
    category = Category.BEST_PRACTICES
    severity = Severity.INFO

    def analyze(self, tree: ast.AST) -> List[Finding]:
        findings = []
        magic_numbers: Dict[str, Set[int]] = {}

        # First pass to set parents
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node

        for node in ast.walk(tree):
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
                            magic_numbers[val_str] = set()
                        if hasattr(node, 'lineno'):
                            magic_numbers[val_str].add(node.lineno)

        if magic_numbers:
            all_lines = set()
            values = []
            for val, lines in magic_numbers.items():
                all_lines.update(lines)
                values.append(val)
                
            val_str = ", ".join(sorted(values))
            findings.append(
                Finding(
                    id=self.id,
                    title=self.title,
                    category=self.category,
                    severity=self.severity,
                    line_numbers=sorted(list(all_lines)),
                    explanation=f"The number {val_str} is used directly in the code without a name. Numbers like this can make the code harder to read later, because other people might not know what {val_str} means in this context.",
                    suggestion="Try assigning this number to a named variable at the top of your file or function. A descriptive name makes the purpose clear!",
                    example="MAX_RETRIES = 5\nif tries > MAX_RETRIES:  # Good\nif tries > 5:  # Bad"
                )
            )
        return findings
