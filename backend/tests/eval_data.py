EVALUATION_DATASET = [
    # --- CLEAN CODE ---
    {
        "name": "Simple Greeting",
        "category": "clean_code",
        "code": "def greet_user(name: str):\n    return f'Hello, {name}'\n",
        "expected_present": [],
        "expected_absent": ["unclear-variable-name", "non-snake-case-function", "print-in-function"]
    },
    {
        "name": "Standard Math Function",
        "category": "clean_code",
        "code": "def calculate_area(width, height):\n    return width * height\n",
        "expected_present": [],
        "expected_absent": ["unclear-variable-name", "magic-number"]
    },
    {
        "name": "Valid Loop with Range",
        "category": "clean_code",
        "code": "def print_stars(count):\n    for i in range(count):\n        return '*'\n",
        "expected_present": [],
        "expected_absent": ["unclear-variable-name", "magic-number", "print-in-function"]
    },
    {
        "name": "List Comprehension",
        "category": "clean_code",
        "code": "def get_even_numbers(numbers):\n    return [num for num in numbers if num % 2 == 0]\n",
        "expected_present": [],
        "expected_absent": ["magic-number"] # 2 and 0 are allowed
    },
    {
        "name": "Constants Used Correctly",
        "category": "clean_code",
        "code": "MAX_RETRIES = 5\ndef connect():\n    if retries > MAX_RETRIES:\n        return False\n    return True\n",
        "expected_present": [],
        "expected_absent": ["magic-number"]
    },

    # --- SYNTAX ERRORS ---
    {
        "name": "Missing Colon",
        "category": "syntax_errors",
        "code": "def do_something()\n    pass\n",
        "expected_present": ["syntax-error"],
        "expected_absent": []
    },
    {
        "name": "Unmatched Parenthesis",
        "category": "syntax_errors",
        "code": "x = (1 + 2\n",
        "expected_present": ["syntax-error"],
        "expected_absent": []
    },
    {
        "name": "Bad Indentation",
        "category": "syntax_errors",
        "code": "def check():\nreturn True\n",
        "expected_present": ["syntax-error"],
        "expected_absent": []
    },
    {
        "name": "Invalid Keyword",
        "category": "syntax_errors",
        "code": "funcion my_func():\n    pass\n",
        "expected_present": ["syntax-error"],
        "expected_absent": []
    },
    {
        "name": "Missing Quotes",
        "category": "syntax_errors",
        "code": "name = \"John\n",
        "expected_present": ["syntax-error"],
        "expected_absent": []
    },

    # --- ISOLATED RULES ---
    {
        "name": "Unclear Variable Names",
        "category": "isolated_rules",
        "code": "x = 10\ntemp = 20\ndata = x + temp\n",
        "expected_present": ["unclear-variable-name"],
        "expected_absent": []
    },
    {
        "name": "Non-Snake Case Function",
        "category": "isolated_rules",
        "code": "def calculateTotal():\n    return 0\n",
        "expected_present": ["non-snake-case-function"],
        "expected_absent": []
    },
    {
        "name": "Function Too Long",
        "category": "isolated_rules",
        "code": "def do_everything():\n" + ("    pass\n" * 35),
        "expected_present": ["function-too-long"],
        "expected_absent": []
    },
    {
        "name": "Too Many Parameters",
        "category": "isolated_rules",
        "code": "def create_user(name, age, email, address, phone, zip_code):\n    return True\n",
        "expected_present": ["too-many-parameters"],
        "expected_absent": []
    },
    {
        "name": "Nested If Too Deep",
        "category": "isolated_rules",
        "code": "def process():\n    if True:\n        if True:\n            if True:\n                return 1\n",
        "expected_present": ["nested-if-too-deep"],
        "expected_absent": []
    },
    {
        "name": "Print Inside Function",
        "category": "isolated_rules",
        "code": "def add(a, b):\n    print(a + b)\n",
        "expected_present": ["print-in-function"],
        "expected_absent": []
    },
    {
        "name": "Compare Boolean True",
        "category": "isolated_rules",
        "code": "if is_valid == True:\n    return 1\n",
        "expected_present": ["compare-boolean"],
        "expected_absent": []
    },
    {
        "name": "Compare Boolean False",
        "category": "isolated_rules",
        "code": "if is_valid == False:\n    return 0\n",
        "expected_present": ["compare-boolean"],
        "expected_absent": []
    },
    {
        "name": "Bare Except",
        "category": "isolated_rules",
        "code": "try:\n    do_work()\nexcept:\n    pass\n",
        "expected_present": ["bare-except"],
        "expected_absent": []
    },
    {
        "name": "Use Eval",
        "category": "isolated_rules",
        "code": "result = eval('1 + 1')\n",
        "expected_present": ["use-eval"],
        "expected_absent": []
    },

    # --- MIXED BEGINNER MISTAKES ---
    {
        "name": "The Kitchen Sink",
        "category": "mixed_beginner_mistakes",
        "code": "def ProcessData(data, x, y, z, a, b):\n    if data == True:\n        print(x)\n        try:\n            eval(y)\n        except:\n            pass\n",
        "expected_present": ["non-snake-case-function", "unclear-variable-name", "too-many-parameters", "compare-boolean", "print-in-function", "use-eval", "bare-except"],
        "expected_absent": []
    },
    {
        "name": "Deeply Nested Magic Variables",
        "category": "mixed_beginner_mistakes",
        "code": "def check():\n    x = 100\n    if x:\n        if x > 50:\n            if x < 100:\n                tax = price * 0.25\n                print(tax)\n",
        "expected_present": ["nested-if-too-deep", "magic-number", "unclear-variable-name", "print-in-function"],
        "expected_absent": []
    },
    {
        "name": "Long Bad Function",
        "category": "mixed_beginner_mistakes",
        "code": "def bad_func():\n    temp = 1\n" + ("    temp += 1\n" * 32),
        "expected_present": ["function-too-long", "unclear-variable-name"],
        "expected_absent": []
    },

    # --- FALSE POSITIVE CASES ---
    {
        "name": "Top Level Function Calls (Magic Numbers)",
        "category": "false_positive_cases",
        "code": "MIN_AGE = 18\n\ndef check_age(age):\n    if age >= MIN_AGE:\n        return True\n    return False\n\nresult = check_age(21)\nprint(check_age(25))\n",
        "expected_present": [],
        "expected_absent": ["magic-number"]
    },
    {
        "name": "Standard List Access & Range",
        "category": "false_positive_cases",
        "code": "def get_items():\n    items = [50, 100, 150]\n    for i in range(25):\n        return items[0]\n",
        "expected_present": [],
        "expected_absent": ["magic-number"]
    }
]
