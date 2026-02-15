"""Mathematical application forms."""

__all__ = [
    'CreateCalculationConditionsForm',
    'UpdateCalculationConditionsForm',
    'RegularCalculationConditionsForm',
    'NumberInputForm',
]

from .calculation import (
    CreateCalculationConditionsForm,
    NumberInputForm,
    RegularCalculationConditionsForm,
    UpdateCalculationConditionsForm,
)
