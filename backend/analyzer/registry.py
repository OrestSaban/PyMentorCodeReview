from typing import List, Type
from .rules.base import BaseRule
from .rules.naming import UnclearVariableNameRule, NonSnakeCaseFunctionRule
from .rules.length import FunctionTooLongRule, TooManyParametersRule
from .rules.complexity import NestedIfTooDeepRule
from .rules.practices import PrintInFunctionRule, CompareBooleanRule, BareExceptRule, UseEvalRule, MagicNumberRule

class RuleRegistry:
    def __init__(self):
        self._rules: List[Type[BaseRule]] = [
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
        ]

    def get_all_rules(self) -> List[BaseRule]:
        return [rule_class() for rule_class in self._rules]
