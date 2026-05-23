# PyMentor Review: MVP Scope

This document outlines the scope of the MVP for the PyMentor Review educational code analysis tool. The goal of this tool is to provide beginner-friendly, static-analysis-based feedback on Python code. It is designed to act as a helpful mentor, not a strict enterprise linter.

## Supported Rules (38)

The MVP now implements 38 rules across 6 categories:
- **Syntax** (syntax errors)
- **Naming & Style** (e.g. unclear variable names, non-snake case)
- **Complexity** (e.g. deeply nested ifs, too many branches, too many local variables)
- **Function Design** (e.g. too many parameters, missing return value)
- **Common Pitfalls** (e.g. `compare-boolean`, `range-len-loop`)
- **Safety & Maintainability** (e.g. `use-eval`, `hardcoded-secret`, `global-variable-modification`)

(A complete list of rules can be dynamically retrieved via the `RuleRegistry`.)

## Explicitly Out of Scope

To keep the MVP focused and lightweight, the following are explicitly out of scope:

- **AI/LLM Integrations:** The tool is strictly rule-based and deterministic.
- **Type Checking (MyPy):** Advanced static type analysis and inference are not supported.
- **Code Execution:** The code is parsed into an AST but never executed (no runtime security risks).
- **Auto-formatting:** The tool does not automatically rewrite the user's code (no `black` or `ruff` integration).
- **Database & Authentication:** No user accounts, history tracking, or persistent storage.
- **Project-Level Analysis:** The analyzer evaluates isolated snippets of code, not entire repositories or multi-file projects.
