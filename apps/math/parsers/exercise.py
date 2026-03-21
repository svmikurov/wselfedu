"""Mathematical exercise request query parser."""

from apps.core.parsers.abstract import AbstractRequestParamsQueryParser
from apps.math.domains.dto import CalculationConditionDTO

from . import types


class CalculationParser(
    AbstractRequestParamsQueryParser[
        types.CalculationConditionsData,
        types.CalculationConditionsProtocol,
    ]
):
    """Regular calculation exercise request parser."""

    def parse(
        self,
        query: types.CalculationConditionsData,
    ) -> types.CalculationConditionsProtocol:
        """Parse calculation exercise request conditions."""
        return CalculationConditionDTO(
            min_operand=int(query['min_operand']),
            max_operand=int(query['max_operand']),
            operation_type=query['operation_type'],
        )
