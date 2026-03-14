"""Calculation exercise use case."""

from apps.core.handlers.protocol import (
    RequestContextProtocol,
    SimpleRequestParamsProtocol,
)
from apps.core.use_cases.abstract import AbstractUseCase
from apps.math.domains.dto import CalculationConditionDTO


# REVIEW: Update to null object
class CalculationConditionsUseCase(
    AbstractUseCase[
        SimpleRequestParamsProtocol,
        RequestContextProtocol,
        CalculationConditionDTO,
        CalculationConditionDTO,
    ],
):
    """Calculation conditions use case."""

    def execute(
        self,
        params: SimpleRequestParamsProtocol,
        context: RequestContextProtocol,
        validated: CalculationConditionDTO,
    ) -> CalculationConditionDTO:
        """Start regular calculation exercise."""
        return validated
