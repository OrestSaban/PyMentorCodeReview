import ast
from typing import List
from .models import Finding, AnalysisReport, Category, Severity
from .rules.naming import NamingRule
from .rules.length import LengthRule
from .rules.complexity import ComplexityRule
from .rules.practices import PracticesRule

class Analyzer:
    def __init__(self):
        self.rules = [
            NamingRule(),
            LengthRule(),
            ComplexityRule(),
            PracticesRule(),
        ]

    def analyze(self, code: str) -> AnalysisReport:
        findings: List[Finding] = []
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            findings.append(
                Finding(
                    id="syntax-error",
                    title="Syntax Error",
                    category=Category.SYNTAX,
                    severity=Severity.ERROR,
                    line_number=e.lineno,
                    explanation=f"Python couldn't understand your code. There's a syntax error: {e.msg}. This usually means a missing colon ':', parentheses '()', or a typo.",
                    suggestion="Check the line mentioned and look for missing characters or typos."
                )
            )
            return self._generate_report(findings)
            
        for rule in self.rules:
            findings.extend(rule.analyze(tree))
            
        return self._generate_report(findings)
        
    def _generate_report(self, findings: List[Finding]) -> AnalysisReport:
        # Calculate a basic score
        score = 100
        for finding in findings:
            if finding.severity == Severity.ERROR:
                score -= 20
            elif finding.severity == Severity.WARNING:
                score -= 10
            elif finding.severity == Severity.INFO:
                score -= 5
                
        score = max(0, score)
        
        if score == 100:
            summary = "Great job! Your code looks clean and follows best practices."
        elif score > 70:
            summary = "Good work! There are a few things you can improve to make your code even better."
        elif score > 40:
            summary = "You're getting there. Look at the suggestions below to improve readability and avoid common mistakes."
        else:
            summary = "There are several important issues in your code. Take it step by step and fix the errors and warnings first."
            
        return AnalysisReport(
            score=score,
            summary=summary,
            findings=findings
        )
