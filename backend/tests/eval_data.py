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
        "name": "Complex Boolean Condition",
        "category": "isolated_rules",
        "code": "def check(a, b, c, d, e, f):\n    if a and b and c and d and e and f:\n        pass\n",
        "expected_present": ["complex-boolean-condition"],
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
    },
    {
        "name": "Mutable Default Arguments",
        "category": "isolated_rules",
        "code": "def add_item(item, items=[]):\n    items.append(item)\n    return items\n",
        "expected_present": ["mutable-default-argument"],
        "expected_absent": []
    },
    {
        "name": "Exec Usage",
        "category": "isolated_rules",
        "code": "def run_code(code_str):\n    exec(code_str)\n",
        "expected_present": ["exec-usage"],
        "expected_absent": []
    },
    {
        "name": "Broad Exception",
        "category": "isolated_rules",
        "code": "try:\n    pass\nexcept Exception:\n    pass\n",
        "expected_present": ["broad-exception"],
        "expected_absent": ["bare-except"]
    },
    {
        "name": "Missing Return Value",
        "category": "isolated_rules",
        "code": "def calculate_tax(price):\n    tax = price * 0.2\n",
        "expected_present": ["missing-return-value"],
        "expected_absent": []
    },
    {
        "name": "Unused Loop Variable",
        "category": "isolated_rules",
        "code": "def print_stars():\n    for i in range(5):\n        print('*')\n",
        "expected_present": ["unused-loop-variable"],
        "expected_absent": []
    },
    {
        "name": "New Batch Kitchen Sink",
        "category": "mixed_beginner_mistakes",
        "code": "def calculate_data(items=[]):\n    for idx in range(10):\n        try:\n            exec('print(items)')\n        except Exception:\n            pass\n",
        "expected_present": ["mutable-default-argument", "exec-usage", "broad-exception", "missing-return-value", "unused-loop-variable"],
        "expected_absent": []
    },
    {
        "name": "Non Snake Case Variable",
        "category": "isolated_rules",
        "code": "userName = 'Alex'\ndef greet():\n    totalPrice = 100\n    return totalPrice\n",
        "expected_present": ["non-snake-case-variable"],
        "expected_absent": ["unclear-variable-name"]
    },
    {
        "name": "Constant Not Uppercase",
        "category": "isolated_rules",
        "code": "max_retries = 3\ntax_rate = 0.2\nuser_name = 'Alex'\ndef calculate():\n    default_limit = 5\n    return default_limit\n",
        "expected_present": ["constant-not-uppercase"],
        "expected_absent": []
    },
    {
        "name": "Shadowing Builtins",
        "category": "isolated_rules",
        "code": "list = [1, 2, 3]\ndef calculate(dict):\n    return len(dict)\n",
        "expected_present": ["shadowing-builtin-name"],
        "expected_absent": []
    },
    {
        "name": "Unclear Function Name",
        "category": "isolated_rules",
        "code": "def do_it():\n    pass\ndef handle_payment():\n    pass\n",
        "expected_present": ["unclear-function-name"],
        "expected_absent": []
    },
    {
        "name": "Inconsistent Return",
        "category": "isolated_rules",
        "code": "def get_discount(age):\n    if age < 18:\n        return 0.2\n    if age > 65:\n        return 0.3\n",
        "expected_present": ["inconsistent-return"],
        "expected_absent": []
    },
    {
        "name": "Too Many Local Variables",
        "category": "isolated_rules",
        "code": "def process():\n    a=1\n    b=2\n    c=3\n    d=4\n    e=5\n    f=6\n    g=7\n    h=8\n    i=9\n    j=10\n    k=11\n    l=12\n",
        "expected_present": ["too-many-local-variables"],
        "expected_absent": []
    },
    {
        "name": "Empty Function",
        "category": "isolated_rules",
        "code": "def process_order(order):\n    ...\n",
        "expected_present": ["empty-function"],
        "expected_absent": ["unclear-function-name"]
    },
    {
        "name": "Too Many Branches",
        "category": "isolated_rules",
        "code": "def get_shipping(country):\n    if country == 'US':\n        return 10\n    elif country == 'CA':\n        return 12\n    elif country == 'UK':\n        return 15\n    elif country == 'DE':\n        return 13\n    elif country == 'FR':\n        return 14\n    else:\n        return 20\n",
        "expected_present": ["too-many-branches"],
        "expected_absent": []
    },
    {
        "name": "Unnecessary Else After Return",
        "category": "isolated_rules",
        "code": "def check_age(age):\n    if age >= 18:\n        return 'adult'\n    else:\n        return 'minor'\n",
        "expected_present": ["unnecessary-else-after-return"],
        "expected_absent": []
    },
    {
        "name": "Range Len Loop",
        "category": "isolated_rules",
        "code": "def print_items(items):\n    for i in range(len(items)):\n        print(items[i])\n",
        "expected_present": ["range-len-loop"],
        "expected_absent": []
    },
    {
        "name": "Manual Counter Loop",
        "category": "isolated_rules",
        "code": "def print_names(names):\n    counter = 0\n    for name in names:\n        print(counter, name)\n        counter += 1\n",
        "expected_present": ["manual-counter-loop"],
        "expected_absent": []
    },
    {
        "name": "Unnecessary List Conversion",
        "category": "isolated_rules",
        "code": "def process(items):\n    for item in list(items):\n        print(item)\n",
        "expected_present": ["unnecessary-list-conversion"],
        "expected_absent": []
    },
    {
        "name": "Repeated Condition",
        "category": "isolated_rules",
        "code": "def get_grade(score):\n    if score > 90:\n        return 'A'\n    elif score > 90:\n        return 'Excellent'\n",
        "expected_present": ["repeated-condition"],
        "expected_absent": []
    },
    {
        "name": "Hardcoded Secret",
        "category": "isolated_rules",
        "code": "api_key = 'ghp_123456789'\npassword = 'mypassword123'\n",
        "expected_present": ["hardcoded-secret"],
        "expected_absent": []
    },
    {
        "name": "Unsafe Yaml Load",
        "category": "isolated_rules",
        "code": "import yaml\nconfig = yaml.load(config_file)\n",
        "expected_present": ["unsafe-yaml-load"],
        "expected_absent": []
    },
    {
        "name": "Subprocess Shell True",
        "category": "isolated_rules",
        "code": "import subprocess\nsubprocess.run('ls -la', shell=True)\n",
        "expected_present": ["subprocess-shell-true"],
        "expected_absent": []
    },
    {
        "name": "Assert Used For Validation",
        "category": "isolated_rules",
        "code": "def process_payment(amount):\n    assert amount > 0\n    return amount\n",
        "expected_present": ["assert-used-for-validation"],
        "expected_absent": []
    },
    {
        "name": "Large Top Level Script",
        "category": "isolated_rules",
        "code": "name = input('Name: ')\nage = int(input('Age: '))\nif age >= 18:\n    print('Adult')\nelse:\n    print('Minor')\nprint(name)\ncount = 0\nfor x in range(10):\n    count += 1\n",
        "expected_present": ["large-top-level-script"],
        "expected_absent": []
    },
    {
        "name": "Global Variable Modification",
        "category": "isolated_rules",
        "code": "count = 0\ndef inc():\n    global count\n    count += 1\n",
        "expected_present": ["global-variable-modification"],
        "expected_absent": []
    },
    {
        "name": "Duplicate String Literal",
        "category": "isolated_rules",
        "code": "def check(status):\n    if status == 'pending':\n        print('pending')\n    return 'pending'\n",
        "expected_present": ["duplicate-string-literal"],
        "expected_absent": []
    },
    {
        "name": "Todo Comment",
        "category": "isolated_rules",
        "code": "def process():\n    # TODO: fix this later\n    pass\n",
        "expected_present": ["todo-comment"],
        "expected_absent": []
    }
]
