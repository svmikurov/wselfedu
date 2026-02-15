"""Calculation exercise views."""

__all__ = [
    # Exercise CRUD
    'CalculationListView',
    # Exercise perform
    'DetailPerformView',
    'ExerciseChoiceView',
    'RegularPerformView',
    'AssignedPerformView',
]

from .crud import (
    CalculationListView,
)
from .perform import (
    AssignedPerformView,
    DetailPerformView,
    ExerciseChoiceView,
    RegularPerformView,
)
