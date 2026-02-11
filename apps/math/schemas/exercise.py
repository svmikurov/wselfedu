"""Mathematical discipline exercise schemas."""

from typing import Literal

from pydantic import BaseModel, ConfigDict

Operation = Literal['add', 'sub', 'mul', 'div']


class CalculationConditionsDTO(BaseModel):
    """Calculation conditions DTO."""

    min_operand: str
    max_operand: str
    operation_type: Operation

    model_config = ConfigDict(
        extra='forbid',
        frozen=True,
    )
