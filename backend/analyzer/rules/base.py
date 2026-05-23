from abc import ABC, abstractmethod
from typing import List
from ..models import Finding, Category, Severity
from ..context import AnalysisContext

class BaseRule(ABC):
    id: str
    title: str
    category: Category
    severity: Severity

    @abstractmethod
    def check(self, context: AnalysisContext) -> List[Finding]:
        pass
