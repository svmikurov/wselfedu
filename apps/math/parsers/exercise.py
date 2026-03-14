"""Mathematical exercise parser."""

from apps.core.handlers.protocol import QueryRequestParamsProtocol
from apps.core.parsers.abstract import AbstractRequestParser
from apps.math.domains.dto import CalculationConditionDTO


class CalculationParser(
    AbstractRequestParser[QueryRequestParamsProtocol, CalculationConditionDTO]
):
    """Regular calculation exercise request parser."""

    def parse(
        self, params: QueryRequestParamsProtocol
    ) -> CalculationConditionDTO:
        """Parse calculation exercise request conditions."""
        return CalculationConditionDTO(
            min_operand=int(params.query['min_operand']),
            max_operand=int(params.query['max_operand']),
            operation_type=params.query['operation_type'],
        )
