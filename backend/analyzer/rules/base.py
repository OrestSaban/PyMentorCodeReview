import ast
from abc import ABC, abstractmethod
from typing import List
from ..models import Finding

class Rule(ABC):
    @abstractmethod
    def analyze(self, tree: ast.AST) -> List[Finding]:
        pass
