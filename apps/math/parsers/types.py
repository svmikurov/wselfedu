"""Request parameters query types."""

from typing import Literal, Protocol, TypedDict

OPERATION_TYPE = Literal['add', 'sub', 'mul', 'div']


class CalculationConditionsData(TypedDict):
    """Regular calculation exercise data."""

    min_operand: str
    max_operand: str
    operation_type: OPERATION_TYPE


class CalculationConditionsProtocol(Protocol):
    """Regular calculation exercise data."""

    min_operand: int
    max_operand: int
    operation_type: OPERATION_TYPE
