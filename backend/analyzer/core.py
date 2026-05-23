import ast
import traceback
from typing import List

from .models import AnalysisReport, Finding, Category, Severity
from .rules import (
    Rule,
    UnclearVariableNameRule,
    NonSnakeCaseFunctionRule,
    FunctionTooLongRule,
    TooManyParametersRule,
    NestedIfTooDeepRule,
    PrintInFunctionRule,
    CompareBooleanRule,
    BareExceptRule,
    UseEvalRule,
    MagicNumberRule
)

class Analyzer:
    def __init__(self):
        self.rules: List[Rule] = [
            UnclearVariableNameRule(),
            NonSnakeCaseFunctionRule(),
            FunctionTooLongRule(),
            TooManyParametersRule(),
            NestedIfTooDeepRule(),
            PrintInFunctionRule(),
            CompareBooleanRule(),
            BareExceptRule(),
            UseEvalRule(),
            MagicNumberRule()
        ]
        
    def analyze(self, code: str) -> AnalysisReport:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return AnalysisReport(
                score=0,
                summary="We could not analyze your code because it has a syntax error.",
                findings=[
                    Finding(
                        id="syntax-error",
                        title="Syntax Error",
                        category=Category.SYNTAX,
                        severity=Severity.ERROR,
                        line_number=e.lineno,
                        explanation=f"Python couldn't parse this code because it found a syntax error. This usually happens when there's a missing symbol or incorrect indentation. Without valid syntax, Python doesn't know how to run your program.\n(Error detail: {e.msg})",
                        suggestion="Check this line and the line just above it. Look for missing colons (:), unmatched parentheses, or incorrect indentation."
                    )
                ]
            )
            
        all_findings = []
        for rule in self.rules:
            try:
                rule_findings = rule.analyze(tree)
                all_findings.extend(rule_findings)
            except Exception as e:
                print(f"Error running rule {rule.__class__.__name__}: {e}")
                traceback.print_exc()
                
        # Calculate score (start at 100, deduct points)
        score = 100
        for f in all_findings:
            if f.severity == Severity.ERROR:
                score -= 20
            elif f.severity == Severity.WARNING:
                score -= 10
            elif f.severity == Severity.INFO:
                score -= 5
                
        score = max(0, score)
        
        summary = "Your code looks great!"
        if score < 100:
            summary = f"We found {len(all_findings)} area{'s' if len(all_findings) != 1 else ''} for improvement."
            
        return AnalysisReport(
            score=score,
            summary=summary,
            findings=all_findings
        )
