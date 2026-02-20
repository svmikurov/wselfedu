"""Mathematical application forms."""

__all__ = [
    # Calculation CRUD
    'CreateCalculationConditionsForm',
    'UpdateCalculationConditionsForm',
    'RegularCalculationConditionsForm',
    # Calculation assignation
    'AssignCalculationForm',
    # Calculation exercise
    'NumberInputForm',
]

from .calculation import (
    CreateCalculationConditionsForm,
    NumberInputForm,
    RegularCalculationConditionsForm,
    UpdateCalculationConditionsForm,
)
from .calculation_assignation import (
    AssignCalculationForm,
)
