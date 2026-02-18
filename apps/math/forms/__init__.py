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

from .assignation import (
    AssignCalculationForm,
)
from .calculation import (
    CreateCalculationConditionsForm,
    NumberInputForm,
    RegularCalculationConditionsForm,
    UpdateCalculationConditionsForm,
)
