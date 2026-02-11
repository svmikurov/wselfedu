"""Exercise web validators."""

from typing import Any

from apps.core.validators.request.abstract import AbstractRegularValidator

from .dto import CalculationConditionsWebRequest


class RegularCalculationConditionsWebValidator(
    AbstractRegularValidator[CalculationConditionsWebRequest]
):
    """Calculation conditions web validator."""

    @classmethod
    def validate(
        cls, raw_data: dict[str, Any]
    ) -> CalculationConditionsWebRequest:
        """Validate calculation conditions request."""
        # TODO: Handle invalid cases
        return CalculationConditionsWebRequest(
            min_operand=raw_data['min_operand'],
            max_operand=raw_data['max_operand'],
            operation_type=raw_data['operation_type'],
        )
