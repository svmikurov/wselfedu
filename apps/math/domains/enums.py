"""Mathematical discipline domain entity enumerations."""

from apps.core.enums import BaseEnum


class CalculationEnum(BaseEnum):
    """Calculation type enumerations."""

    ADD = 'add'
    SUB = 'sub'
    MUL = 'mul'
    DIV = 'div'
