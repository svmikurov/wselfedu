"""Calculation exercise views."""

__all__ = [
    # Exercise CRUD
    'CalculationListView',
    'CalculationCreateView',
    'CalculationUpdateView',
    'CalculationDeleteView',
    # Exercise perform
    'DetailPerformView',
    'ExerciseChoiceView',
    'RegularPerformView',
    'AssignedPerformView',
]

from .crud import (
    CalculationCreateView,
    CalculationDeleteView,
    CalculationListView,
    CalculationUpdateView,
)
from .perform import (
    AssignedPerformView,
    DetailPerformView,
    ExerciseChoiceView,
    RegularPerformView,
)
