"""Exercise web validators."""

from typing import Any

from apps.core.validators.request.abstract import AbstractRegularValidator
from apps.math.domains.dto import CalculationAnswer, CalculationConditions


class RegularCalculationStartWebValidator(
    AbstractRegularValidator[CalculationConditions]
):
    """Calculation conditions web validator."""

    @classmethod
    def validate(cls, raw_data: dict[str, Any]) -> CalculationConditions:
        """Validate calculation conditions request."""
        return CalculationConditions(
            min_operand=raw_data['min_operand'],
            max_operand=raw_data['max_operand'],
            operation_type=raw_data['operation_type'],
        )


class RegularCalculationCheckWebValidator(
    AbstractRegularValidator[CalculationAnswer]
):
    """Calculation conditions web validator."""

    @classmethod
    def validate(cls, raw_data: dict[str, Any]) -> CalculationAnswer:
        """Validate calculation conditions request."""
        return CalculationAnswer(
            user_answer=raw_data['user_answer'],
        )
