"""Mathematical discipline domain entity enumerations."""

from contracts.enums.base import BaseEnum


class CalculationEnum(BaseEnum):
    """Calculation type enumerations."""

    ADD = 'add'
    SUB = 'sub'
    MUL = 'mul'
    DIV = 'div'
