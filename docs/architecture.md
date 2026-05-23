# PyMentor Review: Analyzer Architecture

The backend of PyMentor Review is built on a modular, rule-based architecture designed for high maintainability, testability, and ease of extension. This document outlines the core components of the system.

## 1. Analyzer Pipeline
When a request is sent to the `/analyze` endpoint, the `Analyzer` (in `core.py`) executes the following pipeline:
1. **Parsing**: The raw Python code is parsed into an Abstract Syntax Tree (AST) using Python's built-in `ast` module.
2. **Context Creation**: If parsing is successful, an `AnalysisContext` is created, containing the code, line segments, and the AST.
3. **Rule Execution**: The analyzer fetches all registered rules from the `RuleRegistry` and calls `.check(context)` on each one.
4. **Scoring**: Findings are aggregated. The initial score is 100, and points are deducted based on severity (Error = -20, Warning = -10, Info = -5).
5. **Report Generation**: An `AnalysisReport` is generated and returned as structured JSON.

## 2. AnalysisContext
The `AnalysisContext` class encapsulates the current state of the analysis. It is passed to every rule during execution. 
It contains:
- `code`: The raw string of the source code.
- `lines`: A list of strings representing each line of code.
- `tree`: The parsed `ast.AST` object.

Crucially, the `AnalysisContext` automatically traverses the AST upon initialization and annotates each node with a `.parent` attribute. This allows rules to perform upward traversals (e.g., checking if a magic number is inside a list or top-level function call).

## 3. BaseRule Abstraction
Every rule in the system inherits from the `BaseRule` class. This enforces a strict contract:
- Every rule must declare its metadata: `id`, `title`, `category`, and `severity`.
- Every rule must implement the `check(self, context: AnalysisContext) -> List[Finding]` method.

This ensures that the analyzer engine does not need to know any implementation details about individual rules.

## 4. Rule Registry
The `RuleRegistry` (`registry.py`) is a centralized location where all active rules are explicitly declared. 
When the `Analyzer` starts, it asks the registry for a list of instantiated rules. This decouples the rule definitions from the engine execution, making it extremely easy to enable, disable, or add new rules without modifying `core.py`.

## Why this design?
This architecture makes adding future rules incredibly straightforward:
1. Create a new class inheriting from `BaseRule` in the appropriate category module (e.g., `naming.py` or `practices.py`).
2. Implement the AST traversal inside the `check` method.
3. Add the class to `RuleRegistry`.

There is no need to modify any core execution logic, API routing, or frontend components. The analyzer scales linearly with the number of rules.
