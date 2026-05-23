# PyMentor Review: MVP Scope

This document outlines the scope of the MVP for the PyMentor Review educational code analysis tool. The goal of this tool is to provide beginner-friendly, static-analysis-based feedback on Python code. It is designed to act as a helpful mentor, not a strict enterprise linter.

## Supported Rules (11)

The MVP strictly implements the following 11 rules:

1. **Syntax Error (`syntax-error`)**
   - **Detects:** Any Python syntax error preventing the code from parsing.
   - **Category:** Syntax (Error)

2. **Unclear Variable Name (`unclear-variable-name`)**
   - **Detects:** The use of overly generic or single-letter variable names (e.g., `x`, `y`, `a`, `b`, `temp`, `data`, `foo`, `bar`).
   - **Category:** Naming (Warning)

3. **Non-Snake Case Function (`non-snake-case-function`)**
   - **Detects:** Function names that do not follow the standard Python `snake_case` convention.
   - **Category:** Naming (Info)

4. **Function Too Long (`function-too-long`)**
   - **Detects:** Functions that exceed 30 lines of code.
   - **Category:** Maintainability (Warning)

5. **Too Many Parameters (`too-many-parameters`)**
   - **Detects:** Functions that accept more than 4 parameters.
   - **Category:** Complexity (Warning)

6. **Nested If Too Deep (`nested-if-too-deep`)**
   - **Detects:** `if` statements that are nested more than 2 levels deep.
   - **Category:** Complexity (Warning)

7. **Print Inside Function (`print-in-function`)**
   - **Detects:** The use of `print()` inside a function definition, rather than returning a value.
   - **Category:** Best Practices (Info)

8. **Compare Boolean (`compare-boolean`)**
   - **Detects:** Direct comparisons to boolean values (e.g., `if x == True:` or `if is_valid == False:`).
   - **Category:** Best Practices (Info)

9. **Bare Except (`bare-except`)**
   - **Detects:** The use of a bare `except:` block, which dangerously catches all exceptions including system exits.
   - **Category:** Best Practices (Warning)

10. **Use Eval (`use-eval`)**
    - **Detects:** Any invocation of the dangerous `eval()` function.
    - **Category:** Best Practices (Error)

11. **Magic Number (`magic-number`)**
    - **Detects:** Unexplained numeric literals used in calculations, conditions, or general assignments.
    - **Ignores:** Common values (`0`, `1`, `-1`, `2`, `10`, `100`), values assigned to `UPPER_CASE` constants, range arguments, list/tuple/set elements, simple indexes, and top-level function arguments.
    - **Category:** Best Practices (Info)

## Explicitly Out of Scope

To keep the MVP focused and lightweight, the following are explicitly out of scope:

- **AI/LLM Integrations:** The tool is strictly rule-based and deterministic.
- **Type Checking (MyPy):** Advanced static type analysis and inference are not supported.
- **Code Execution:** The code is parsed into an AST but never executed (no runtime security risks).
- **Auto-formatting:** The tool does not automatically rewrite the user's code (no `black` or `ruff` integration).
- **Database & Authentication:** No user accounts, history tracking, or persistent storage.
- **Project-Level Analysis:** The analyzer evaluates isolated snippets of code, not entire repositories or multi-file projects.
