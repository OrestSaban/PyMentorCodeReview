from typing import List, Type
from .rules.base import BaseRule
from .rules.naming import (
    UnclearVariableNameRule, NonSnakeCaseFunctionRule,
    NonSnakeCaseVariableRule, ConstantNotUppercaseRule,
    ShadowingBuiltinNameRule, UnclearFunctionNameRule
)
from .rules.length import FunctionTooLongRule, TooManyParametersRule, TooManyLocalVariablesRule
from .rules.complexity import (
    NestedIfTooDeepRule, TooManyBranchesRule, ComplexBooleanConditionRule, UnnecessaryElseAfterReturnRule
)
from .rules.practices import (
    PrintInFunctionRule, CompareBooleanRule, BareExceptRule, UseEvalRule, MagicNumberRule,
    MutableDefaultArgumentRule, UseExecRule, BroadExceptionRule, MissingReturnValueRule, UnusedLoopVariableRule,
    InconsistentReturnRule, EmptyFunctionRule, RangeLenLoopRule, ManualCounterLoopRule,
    UnnecessaryListConversionRule, RepeatedConditionRule
)
from .rules.safety import (
    HardcodedSecretRule, UnsafeYamlLoadRule, SubprocessShellTrueRule, AssertUsedForValidationRule
)
from .rules.maintainability import (
    LargeTopLevelScriptRule, GlobalVariableModificationRule, DuplicateStringLiteralRule, TodoCommentRule
)

class RuleRegistry:
    def __init__(self):
        self._rules: List[Type[BaseRule]] = [
            UnclearVariableNameRule,
            NonSnakeCaseFunctionRule,
            NonSnakeCaseVariableRule,
            ConstantNotUppercaseRule,
            ShadowingBuiltinNameRule,
            UnclearFunctionNameRule,
            FunctionTooLongRule,
            TooManyParametersRule,
            TooManyLocalVariablesRule,
            NestedIfTooDeepRule,
            TooManyBranchesRule,
            ComplexBooleanConditionRule,
            UnnecessaryElseAfterReturnRule,
            PrintInFunctionRule,
            CompareBooleanRule,
            BareExceptRule,
            UseEvalRule,
            MagicNumberRule,
            MutableDefaultArgumentRule,
            UseExecRule,
            BroadExceptionRule,
            MissingReturnValueRule,
            UnusedLoopVariableRule,
            InconsistentReturnRule,
            EmptyFunctionRule,
            RangeLenLoopRule,
            ManualCounterLoopRule,
            UnnecessaryListConversionRule,
            RepeatedConditionRule,
            HardcodedSecretRule,
            UnsafeYamlLoadRule,
            SubprocessShellTrueRule,
            AssertUsedForValidationRule,
            LargeTopLevelScriptRule,
            GlobalVariableModificationRule,
            DuplicateStringLiteralRule,
            TodoCommentRule
        ]

    def get_all_rules(self) -> List[BaseRule]:
        return [rule_class() for rule_class in self._rules]
