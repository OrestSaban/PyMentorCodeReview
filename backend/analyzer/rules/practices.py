import ast
from typing import List, Dict, Set
from ..models import Finding, Category, Severity
from .base import Rule

class PracticesRule(Rule):
    def analyze(self, tree: ast.AST) -> List[Finding]:
        findings = []
        
        # Add parent links
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
                
        print_lines = set()
        compare_bool_lines = set()
        bare_except_lines = set()
        eval_lines = set()
        magic_numbers: Dict[str, Set[int]] = {}

        # 9. Detect print() inside functions
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

        for node in ast.walk(tree):
            # 6. Detect comparisons like == True or == False
            if isinstance(node, ast.Compare):
                for comparator in node.comparators:
                    if isinstance(comparator, ast.Constant) and isinstance(comparator.value, bool):
                        if hasattr(node, 'lineno'):
                            compare_bool_lines.add(node.lineno)
                        break
            
            # 7. Detect bare except blocks
            elif isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    if hasattr(node, 'lineno'):
                        bare_except_lines.add(node.lineno)
                    
            # 8. Detect eval() usage
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'eval':
                if hasattr(node, 'lineno'):
                    eval_lines.add(node.lineno)
                
            # 10. Detect magic numbers, except 0, 1, -1, 2, 10, 100
            elif isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                    allowed_numbers = {0, 1, -1, 2, 10, 100, 0.0, 1.0}
                    if node.value not in allowed_numbers:
                        parent = getattr(node, 'parent', None)
                        
                        # Do not flag numbers assigned to UPPER_CASE constants.
                        is_upper_assign = False
                        if isinstance(parent, ast.Assign) and getattr(parent, 'value', None) is node:
                            for target in parent.targets:
                                if isinstance(target, ast.Name) and target.id.isupper():
                                    is_upper_assign = True
                                    break
                        if is_upper_assign:
                            continue
                            
                        # Do not flag numbers used inside range()
                        if isinstance(parent, ast.Call) and isinstance(parent.func, ast.Name) and parent.func.id == 'range':
                            continue
                            
                        # Do not flag list/tuple/set literal data like [1, 2, 3, 4]
                        if isinstance(parent, (ast.List, ast.Tuple, ast.Set)):
                            continue
                            
                        # Do not flag simple indexes like items[0]
                        if isinstance(parent, ast.Subscript) and getattr(parent, 'slice', None) is node:
                            continue
                        if isinstance(parent, ast.Index):
                            continue
                            
                        # Do not flag numeric literals used as arguments in top-level function calls
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

        if print_lines:
            findings.append(
                Finding(
                    id="print-in-function",
                    title="Print Inside Function",
                    category=Category.BEST_PRACTICES,
                    severity=Severity.INFO,
                    line_numbers=sorted(list(print_lines)),
                    explanation="You are using 'print()' inside a function. Usually, functions should return their results using the 'return' keyword instead of printing them directly. This makes the function more reusable.",
                    suggestion="Consider replacing 'print(...)' with 'return ...', and let the caller print the returned value.",
                    example="def add(a, b):\n    return a + b  # Good\n\ndef add(a, b):\n    print(a + b)  # Bad"
                )
            )

        if compare_bool_lines:
            findings.append(
                Finding(
                    id="compare-boolean",
                    title="Comparing with True/False",
                    category=Category.BEST_PRACTICES,
                    severity=Severity.INFO,
                    line_numbers=sorted(list(compare_bool_lines)),
                    explanation="Comparing a value directly to True or False is unnecessary in Python.",
                    suggestion="Instead of 'if x == True:', just write 'if x:'. Instead of 'if x == False:', write 'if not x:'.",
                    example="if is_valid:  # Good\nif is_valid == True:  # Bad"
                )
            )

        if bare_except_lines:
            findings.append(
                Finding(
                    id="bare-except",
                    title="Bare Except Block",
                    category=Category.BEST_PRACTICES,
                    severity=Severity.WARNING,
                    line_numbers=sorted(list(bare_except_lines)),
                    explanation="A bare 'except:' catches all errors, including system exits and keyboard interrupts (like Ctrl+C). This can hide real bugs in your program.",
                    suggestion="Specify the exact error you want to catch, like 'except ValueError:'. If you really want to catch all regular errors, use 'except Exception:'.",
                    example="except ValueError:  # Good\nexcept:  # Bad"
                )
            )

        if eval_lines:
            findings.append(
                Finding(
                    id="use-eval",
                    title="Avoid Using eval()",
                    category=Category.BEST_PRACTICES,
                    severity=Severity.ERROR,
                    line_numbers=sorted(list(eval_lines)),
                    explanation="The 'eval()' function is dangerous because it can execute arbitrary code. Using it, especially with user input, is a major security risk.",
                    suggestion="Avoid 'eval()'. If you need to parse data, use safer alternatives like 'ast.literal_eval()' or standard JSON/CSV parsers.",
                )
            )

        if magic_numbers:
            all_lines = set()
            values = []
            for val, lines in magic_numbers.items():
                all_lines.update(lines)
                values.append(val)
                
            val_str = ", ".join(sorted(values))
            findings.append(
                Finding(
                    id="magic-number",
                    title="Magic Number",
                    category=Category.BEST_PRACTICES,
                    severity=Severity.INFO,
                    line_numbers=sorted(list(all_lines)),
                    explanation=f"You are using magic numbers ({val_str}) directly in your code. Magic numbers can be hard for others (and future you) to understand what they mean.",
                    suggestion="Assign these numbers to well-named UPPER_CASE variables at the top of your file or function.",
                    example="MAX_RETRIES = 5\nif tries > MAX_RETRIES:  # Good\nif tries > 5:  # Bad"
                )
            )

        return findings
