from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class Category(str, Enum):
    NAMING = "naming"
    COMPLEXITY = "complexity"
    BEST_PRACTICES = "best_practices"
    MAINTAINABILITY = "maintainability"
    SYNTAX = "syntax"

class Finding(BaseModel):
    id: str
    title: str
    category: Category
    severity: Severity
    line_number: Optional[int] = None
    line_numbers: List[int] = []
    explanation: str
    suggestion: str
    example: Optional[str] = None

class AnalysisReport(BaseModel):
    score: int
    summary: str
    findings: List[Finding]

class CodeRequest(BaseModel):
    code: str
