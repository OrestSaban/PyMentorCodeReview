import pytest
from analyzer.core import Analyzer
from analyzer.models import Category, Severity, AnalysisReport, Finding
from typing import List

@pytest.fixture
def analyzer():
    return Analyzer()

# --- Test Helpers ---

def assert_has_finding(report: AnalysisReport, finding_id: str):
    assert any(f.id == finding_id for f in report.findings), f"Expected finding '{finding_id}' not found. Findings: {[f.id for f in report.findings]}"

def assert_not_has_finding(report: AnalysisReport, finding_id: str):
    assert not any(f.id == finding_id for f in report.findings), f"Unexpected finding '{finding_id}' was found."

def get_finding(report: AnalysisReport, finding_id: str) -> Finding:
    for f in report.findings:
        if f.id == finding_id:
            return f
    raise ValueError(f"Finding '{finding_id}' not found.")

# --- Evaluation Tests ---

EVALUATION_SNIPPETS = [
    {
        "name": "Clean Code",
        "code": """
MAX_RETRIES = 5
def connect(url: str, timeout: int = 10):
    for i in range(MAX_RETRIES):
        if try_connect(url, timeout):
            return True
    return False
""",
        "expected_present": [],
        "expected_absent": ["magic-number", "unclear-variable-name", "too-many-parameters", "function-too-long", "nested-if-too-deep", "print-in-function"]
    },
    {
        "name": "Beginner Mistakes",
        "code": """
def do_stuff():
    x = 42
    if x == True:
        print(x)
    
    try:
        y = eval("1 + 1")
    except:
        pass
""",
        "expected_present": ["unclear-variable-name", "compare-boolean", "print-in-function", "use-eval", "bare-except", "magic-number"],
        "expected_absent": ["function-too-long"]
    },
    {
        "name": "Data Structures & Simple Indexes",
        "code": """
def get_first_item():
    items = [100, 200, 300, 400]
    return items[0]
""",
        "expected_present": [],
        "expected_absent": ["magic-number"] # 100 is allowed, 200/300/400 in list, 0 is allowed and in index
    },
    {
        "name": "Deep Nesting",
        "code": """
def process():
    if condition_a():
        if condition_b():
            if condition_c():
                return 1
    return 0
""",
        "expected_present": ["nested-if-too-deep"],
        "expected_absent": ["magic-number"] # 1 and 0 are allowed magic numbers
    },
    {
        "name": "Multiple Magic Numbers & Range",
        "code": """
def calculate():
    for i in range(50):
        tax = price * 0.25
        discount = price * 0.1
""",
        "expected_present": ["magic-number"],
        "expected_absent": ["unclear-variable-name"]
    },
    {
        "name": "Top Level Function Call Magic Numbers",
        "code": """
MINIMUM_ORDER_TOTAL = 50

def calculate_shipping_cost(order_total):
    if order_total >= MINIMUM_ORDER_TOTAL:
        return 0

    return 10

shipping_cost = calculate_shipping_cost(35)
print(calculate_shipping_cost(35))
""",
        "expected_present": [],
        "expected_absent": ["magic-number"]
    }
]

@pytest.mark.parametrize("snippet", EVALUATION_SNIPPETS, ids=lambda s: s["name"])
def test_evaluation_snippets(analyzer, snippet):
    report = analyzer.analyze(snippet["code"])
    for expected in snippet["expected_present"]:
        assert_has_finding(report, expected)
    for absent in snippet["expected_absent"]:
        assert_not_has_finding(report, absent)

# --- Unit Tests ---

def test_syntax_error(analyzer):
    code = "def foo(:\n    pass"
    report = analyzer.analyze(code)
    assert report.score < 100
    assert_has_finding(report, "syntax-error")
    finding = get_finding(report, "syntax-error")
    assert finding.severity == Severity.ERROR

def test_magic_numbers_grouped(analyzer):
    code = """
a = price * 0.25
b = price * 0.25
c = price * 0.15
"""
    report = analyzer.analyze(code)
    assert_has_finding(report, "magic-number")
    finding = get_finding(report, "magic-number")
    assert len(finding.line_numbers) == 3 # Should group all 3 lines
    assert "0.25" in finding.explanation
    assert "0.15" in finding.explanation

def test_upper_case_constants_ignored(analyzer):
    code = "TAX_RATE = 0.25\nDISCOUNT = 0.15"
    report = analyzer.analyze(code)
    assert_not_has_finding(report, "magic-number")

def test_range_ignored(analyzer):
    code = "for i in range(50):\n    pass"
    report = analyzer.analyze(code)
    assert_not_has_finding(report, "magic-number")

def test_eval_detected(analyzer):
    code = "x = eval('1 + 1')"
    report = analyzer.analyze(code)
    assert_has_finding(report, "use-eval")

def test_bare_except_detected(analyzer):
    code = "try:\n    pass\nexcept:\n    pass"
    report = analyzer.analyze(code)
    assert_has_finding(report, "bare-except")

def test_boolean_comparison_detected(analyzer):
    code = "if is_valid == True:\n    pass"
    report = analyzer.analyze(code)
    assert_has_finding(report, "compare-boolean")

def test_unclear_variable_grouped(analyzer):
    code = "x = 1\ny = 2\nx = 3"
    report = analyzer.analyze(code)
    assert_has_finding(report, "unclear-variable-name")
    
    # We should have two findings, one for 'x' (lines 1, 3) and one for 'y' (line 2)
    # wait, get_finding returns the first one. Let's just manually inspect.
    findings = [f for f in report.findings if f.id == "unclear-variable-name"]
    assert len(findings) == 2
    x_finding = next(f for f in findings if "'x'" in f.explanation)
    assert len(x_finding.line_numbers) == 2
    y_finding = next(f for f in findings if "'y'" in f.explanation)
    assert len(y_finding.line_numbers) == 1

def test_print_in_function_grouped(analyzer):
    code = "def my_func():\n    print('a')\n    print('b')"
    report = analyzer.analyze(code)
    assert_has_finding(report, "print-in-function")
    finding = get_finding(report, "print-in-function")
    assert len(finding.line_numbers) == 2

def test_location_information(analyzer):
    code = "def bad_name():\n    x = 1"
    report = analyzer.analyze(code)
    f_unclear = get_finding(report, "unclear-variable-name")
    assert len(f_unclear.occurrences) == 1
    occ = f_unclear.occurrences[0]
    assert occ.line == 2
    assert occ.col is not None
    assert occ.snippet == "x = 1"
    assert occ.value == "x"

def test_syntax_error_snippet(analyzer):
    code = "def foo(:\n    pass"
    report = analyzer.analyze(code)
    finding = get_finding(report, "syntax-error")
    assert finding.snippet == "def foo(:"
    assert finding.col is not None

def test_magic_number_occurrences(analyzer):
    code = "a = 0.25\nb = 0.25"
    report = analyzer.analyze(code)
    finding = get_finding(report, "magic-number")
    assert len(finding.occurrences) == 2
    assert finding.occurrences[0].value == "0.25"
    assert finding.occurrences[0].snippet == "a = 0.25"

def test_scoring_logic(analyzer):
    # Base score is 100.
    # Magic numbers (INFO) is -3.
    # We have 3 occurrences, so base penalty (-3) + extra penalty (2 occurrences = -2) = -5
    # Total score should be 95 ("Looks clean")
    code = "val1 = 0.25\nval2 = 0.25\nval3 = 0.25"
    report = analyzer.analyze(code)
    assert report.score == 95
    assert report.score_label == "Looks clean"
    
    # Let's add more severe issues
    # Bare except (WARNING) = -8
    # eval (ERROR) = -15
    # Magic number (INFO) = -3
    # Total deduction = 26
    # Score = 74 ("Needs some improvement")
    code2 = """
try:
    val1 = eval('1 + 1')
    val2 = 0.25
except:
    pass
"""
    report2 = analyzer.analyze(code2)
    assert report2.score == 74
    assert report2.score_label == "Needs some improvement"

def test_mutable_default_argument(analyzer):
    code = "def foo(a=[]):\n    pass\ndef bar(b=dict()):\n    pass"
    report = analyzer.analyze(code)
    assert_has_finding(report, "mutable-default-argument")
    finding = get_finding(report, "mutable-default-argument")
    assert len(finding.occurrences) == 2

def test_use_exec(analyzer):
    code = "exec('x = 1')"
    report = analyzer.analyze(code)
    assert_has_finding(report, "exec-usage")

def test_broad_exception(analyzer):
    code = "try:\n    pass\nexcept Exception:\n    pass"
    report = analyzer.analyze(code)
    assert_has_finding(report, "broad-exception")

def test_missing_return_value(analyzer):
    code = "def calculate_price(cost):\n    tax = cost * 0.2"
    report = analyzer.analyze(code)
    assert_has_finding(report, "missing-return-value")
    
    # Should not trigger if it has return
    code_good = "def calculate_price(cost):\n    return cost * 1.2"
    report_good = analyzer.analyze(code_good)
    assert_not_has_finding(report_good, "missing-return-value")

def test_unused_loop_variable(analyzer):
    code = "for i in range(5):\n    print('hi')"
    report = analyzer.analyze(code)
    assert_has_finding(report, "unused-loop-variable")
    
    code_good = "for _ in range(5):\n    print('hi')"
    report_good = analyzer.analyze(code_good)
    assert_not_has_finding(report_good, "unused-loop-variable")

def test_non_snake_case_variable(analyzer):
    code = "userName = 'Alex'\nMAX_RETRIES = 3\nuser_name = 'Bob'"
    report = analyzer.analyze(code)
    assert_has_finding(report, "non-snake-case-variable")
    finding = get_finding(report, "non-snake-case-variable")
    assert len(finding.occurrences) == 1
    assert finding.occurrences[0].value == "userName"

def test_constant_not_uppercase(analyzer):
    code = "max_retries = 3\nAPI_URL = 'http'\nuser_name = 'Alex'"
    report = analyzer.analyze(code)
    assert_has_finding(report, "constant-not-uppercase")
    finding = get_finding(report, "constant-not-uppercase")
    assert len(finding.occurrences) == 1
    assert finding.occurrences[0].value == "max_retries"

def test_shadowing_builtin_name(analyzer):
    code = "list = [1, 2]\ndict = {}\nname = 'Alex'"
    report = analyzer.analyze(code)
    assert_has_finding(report, "shadowing-builtin-name")
    finding = get_finding(report, "shadowing-builtin-name")
    assert len(finding.occurrences) == 2
    
def test_unclear_function_name(analyzer):
    code = "def process():\n    pass\ndef handle_payment():\n    pass"
    report = analyzer.analyze(code)
    assert_has_finding(report, "unclear-function-name")
    finding = get_finding(report, "unclear-function-name")
    assert len(finding.occurrences) == 1
    assert finding.occurrences[0].value == "process"

def test_too_many_local_variables(analyzer):
    code = """def calc(a, b):
    v1 = 1
    v2 = 2
    v3 = 3
    v4 = 4
    v5 = 5
    v6 = 6
    v7 = 7
    v8 = 8
    v9 = 9
    return v9"""
    report = analyzer.analyze(code)
    assert_has_finding(report, "too-many-local-variables")

def test_inconsistent_return(analyzer):
    code = "def foo(x):\n    if x:\n        return 1"
    report = analyzer.analyze(code)
    assert_has_finding(report, "inconsistent-return")
    
    code_good = "def foo(x):\n    if x:\n        return 1\n    return 2"
    report_good = analyzer.analyze(code_good)
    assert_not_has_finding(report_good, "inconsistent-return")

def test_empty_function(analyzer):
    code = "def foo():\n    pass\ndef bar():\n    ..."
    report = analyzer.analyze(code)
    assert_has_finding(report, "empty-function")
    finding = get_finding(report, "empty-function")
    assert len(finding.occurrences) == 2


