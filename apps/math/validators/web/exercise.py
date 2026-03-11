"""Exercise web validators."""

from typing import Any

from apps.core.handlers.protocol import RequestDataProtocol
from apps.core.validators.request.abstract import (
    AbstractDetailValidator,
    AbstractRegularValidator,
)
from apps.math.domains.dto import (
    CalculationAnswerDTO,
    CalculationConditionDTO,
    CalculationLoopDTO,
)


class RegularCalculationStartWebValidator(
    AbstractRegularValidator[CalculationConditionDTO]
):
    """Calculation conditions web validator."""

    @classmethod
    def validate(cls, raw_data: dict[str, Any]) -> CalculationConditionDTO:
        """Validate calculation conditions request."""
        return CalculationConditionDTO(
            min_operand=int(raw_data['min_operand']),
            max_operand=int(raw_data['max_operand']),
            operation_type=raw_data['operation_type'],
        )


class RegularCalculationCheckWebValidator(
    AbstractRegularValidator[CalculationLoopDTO]
):
    """Calculation conditions web validator."""

    @classmethod
    def validate(cls, raw_data: dict[str, Any]) -> CalculationLoopDTO:
        """Validate calculation conditions request."""
        return CalculationLoopDTO(
            min_operand=raw_data['min_operand'],
            max_operand=raw_data['max_operand'],
            operation_type=raw_data['operation_type'],
            user_answer=raw_data['user_answer'],
        )


class DetailCalculationCheckWebValidator(
    AbstractDetailValidator[CalculationAnswerDTO]
):
    """Calculation conditions web validator."""

    @classmethod
    def validate(cls, data: RequestDataProtocol) -> CalculationAnswerDTO:
        """Validate calculation conditions request."""
        return CalculationAnswerDTO(
            user_answer=data.query['user_answer'],
        )
