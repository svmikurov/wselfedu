"""Exercise web validators."""

from typing import TypedDict

from apps.core.handlers.protocol import RequestDataProtocol
from apps.core.validators.request.abstract import AbstractRequestValidator
from apps.math.domains.dto import (
    CalculationAnswerDTO,
    CalculationConditionDTO,
    CalculationLoopDTO,
    Operation,
)


class QuestionData(TypedDict):
    """Calculation exercise question dict type."""

    min_operand: int
    max_operand: int
    operation_type: Operation


class UserAnswerData(TypedDict):
    """Calculation exercise user's answer dict type."""

    user_answer: str


class CalculationLoopData(QuestionData, UserAnswerData):
    """Calculation loop data dict type."""


class RegularCalculationStartWebValidator(
    AbstractRequestValidator[CalculationConditionDTO]
):
    """Calculation conditions web validator."""

    @classmethod
    def validate(
        cls,
        data: RequestDataProtocol[QuestionData],
    ) -> CalculationConditionDTO:
        """Validate calculation conditions request."""
        return CalculationConditionDTO(
            min_operand=int(data.data['min_operand']),
            max_operand=int(data.data['max_operand']),
            operation_type=data.data['operation_type'],
        )


class RegularCalculationCheckWebValidator(
    AbstractRequestValidator[CalculationLoopDTO]
):
    """Calculation conditions web validator."""

    @classmethod
    def validate(
        cls,
        data: RequestDataProtocol[CalculationLoopData],
    ) -> CalculationLoopDTO:
        """Validate calculation conditions request."""
        return CalculationLoopDTO(
            min_operand=data.data['min_operand'],
            max_operand=data.data['max_operand'],
            operation_type=data.data['operation_type'],
            user_answer=data.data['user_answer'],
        )


class DetailCalculationCheckWebValidator(
    AbstractRequestValidator[CalculationAnswerDTO]
):
    """Calculation conditions web validator."""

    @classmethod
    def validate(
        cls,
        data: RequestDataProtocol[UserAnswerData],
    ) -> CalculationAnswerDTO:
        """Validate calculation conditions request."""
        return CalculationAnswerDTO(
            user_answer=data.data['user_answer'],
        )
