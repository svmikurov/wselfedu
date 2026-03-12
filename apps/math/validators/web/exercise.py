"""Exercise web validators."""

from apps.core.handlers.protocol import RequestDataProtocol
from apps.core.validators.request.abstract import (
    AbstractRequestValidator,
)
from apps.math.domains.dto import (
    CalculationAnswerDTO,
    CalculationConditionDTO,
    CalculationLoopDTO,
)


class RegularCalculationStartWebValidator(
    AbstractRequestValidator[CalculationConditionDTO]
):
    """Calculation conditions web validator."""

    @classmethod
    def validate(cls, data: RequestDataProtocol) -> CalculationConditionDTO:
        """Validate calculation conditions request."""
        return CalculationConditionDTO(
            min_operand=int(data.query['min_operand']),
            max_operand=int(data.query['max_operand']),
            operation_type=data.query['operation_type'],
        )


class RegularCalculationCheckWebValidator(
    AbstractRequestValidator[CalculationLoopDTO]
):
    """Calculation conditions web validator."""

    @classmethod
    def validate(cls, data: RequestDataProtocol) -> CalculationLoopDTO:
        """Validate calculation conditions request."""
        return CalculationLoopDTO(
            min_operand=data.query['min_operand'],
            max_operand=data.query['max_operand'],
            operation_type=data.query['operation_type'],
            user_answer=data.query['user_answer'],
        )


class DetailCalculationCheckWebValidator(
    AbstractRequestValidator[CalculationAnswerDTO]
):
    """Calculation conditions web validator."""

    @classmethod
    def validate(cls, data: RequestDataProtocol) -> CalculationAnswerDTO:
        """Validate calculation conditions request."""
        return CalculationAnswerDTO(
            user_answer=data.query['user_answer'],
        )
