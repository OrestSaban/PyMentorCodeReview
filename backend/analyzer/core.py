import ast
import traceback
from typing import List

from .models import AnalysisReport, Finding, Category, Severity
from .context import AnalysisContext
from .registry import RuleRegistry

class Analyzer:
    def __init__(self):
        self.registry = RuleRegistry()
        self.rules = self.registry.get_all_rules()
        
    def analyze(self, code: str) -> AnalysisReport:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            snippet = ""
            if e.text:
                snippet = e.text.strip()
            elif e.lineno and 0 < e.lineno <= len(code.splitlines()):
                snippet = code.splitlines()[e.lineno - 1].strip()
                
            return AnalysisReport(
                score=0,
                score_label="Needs careful review",
                summary="We could not analyze your code because it has a syntax error.",
                findings=[
                    Finding(
                        id="syntax-error",
                        title="Syntax Error",
                        category=Category.SYNTAX,
                        severity=Severity.ERROR,
                        line_number=e.lineno,
                        col=e.offset,
                        snippet=snippet,
                        explanation=f"Python couldn't parse this code because it found a syntax error. This usually happens when there's a missing symbol or incorrect indentation. Without valid syntax, Python doesn't know how to run your program.\n(Error detail: {e.msg})",
                        suggestion="Check this line and the line just above it. Look for missing colons (:), unmatched parentheses, or incorrect indentation."
                    )
                ]
            )
            
        context = AnalysisContext(code, tree)
        all_findings = []
        
        for rule in self.rules:
            try:
                rule_findings = rule.check(context)
                all_findings.extend(rule_findings)
            except Exception as e:
                print(f"Error running rule {rule.__class__.__name__}: {e}")
                traceback.print_exc()
                
        # Calculate score (start at 100, deduct points)
        score = 100
        for f in all_findings:
            if f.severity == Severity.ERROR:
                score -= 15
            elif f.severity == Severity.WARNING:
                score -= 8
            elif f.severity == Severity.INFO:
                score -= 3
                
            if len(f.occurrences) > 1:
                extra_penalty = min(5, len(f.occurrences) - 1)
                score -= extra_penalty
                
        score = max(0, min(100, score))
        
        if score >= 90:
            score_label = "Looks clean"
        elif score >= 75:
            score_label = "Good start"
        elif score >= 50:
            score_label = "Needs some improvement"
        else:
            score_label = "Needs careful review"
        
        summary = "Your code looks great!"
        if score < 100:
            summary = f"We found {len(all_findings)} area{'s' if len(all_findings) != 1 else ''} for improvement."
            
        return AnalysisReport(
            score=score,
            score_label=score_label,
            summary=summary,
            findings=all_findings
        )
