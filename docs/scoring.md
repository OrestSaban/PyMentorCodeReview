# PyMentor Review: Educational Scoring System

The scoring system in PyMentor Review is specifically designed for beginners. It is meant to be **educational, forgiving, and encouraging**, rather than an absolute measure of code correctness. The goal is to help users understand the impact of different coding practices without discouraging them with overly harsh penalties.

## Scoring Formula

- Every analysis starts with a base score of **100**.
- The score is strictly clamped between **0 and 100**.

### Base Deductions by Severity
Each finding reduces the score based on its severity:
- **Error**: `-15` points (e.g., Syntax errors, `eval()` usage). These represent significant bugs or severe security risks.
- **Warning**: `-8` points (e.g., Too many parameters, bare excepts). These represent architectural issues or bug-prone patterns.
- **Info**: `-3` points (e.g., Magic numbers, non-snake-case names). These are stylistic or minor readability suggestions.

### Grouped Finding Penalty Capping
If the exact same issue occurs multiple times (e.g., 5 different variables are named unclearly, or 10 magic numbers are used), we group them into a single finding. 

Instead of heavily punishing the user for making the same beginner mistake multiple times, we cap the penalty.
- The first occurrence takes the full base deduction based on severity.
- Each additional occurrence takes a flat **-1** point deduction.
- The extra penalty for multiple occurrences is strictly capped at a maximum of **-5** points.

**Example:**
Using a magic number (INFO) incurs a `-3` penalty. If a user uses 6 magic numbers, the penalty is:
`-3 (base) + 5 (max extra penalty cap) = -8 total`. 
Without the cap, the user would lose 18 points, which feels disproportionately harsh for a simple stylistic error.

## Score Labels

To make the score more human-readable, the API returns a qualitative `score_label` alongside the numerical score:

- **90-100**: `"Looks clean"`
- **75-89**: `"Good start"`
- **50-74**: `"Needs some improvement"`
- **0-49**: `"Needs careful review"`

## Why this approach?
A beginner learning Python might write a functional script that violates 10 PEP8 rules. A standard linter might report 10 errors and give a failing grade, which is highly discouraging. 

PyMentor Review recognizes that learning is iterative. By capping grouped mistakes and weighing stylistic issues lightly, the score reflects *growth* rather than strict enterprise compliance.
