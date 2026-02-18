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
    # Calculation exercise assignation CRUD
    'AssignedCalculationConditionMentorListView',
    'AssignedCalculationConditionMentorCreateView',
    'AssignedCalculationConditionMentorDeleteView',
]

from .custom import (
    CalculationCreateView,
    CalculationDeleteView,
    CalculationListView,
    CalculationUpdateView,
)
from .mentor import (
    AssignedCalculationConditionMentorCreateView,
    AssignedCalculationConditionMentorDeleteView,
    AssignedCalculationConditionMentorListView,
)
from .perform import (
    AssignedPerformView,
    DetailPerformView,
    ExerciseChoiceView,
    RegularPerformView,
)
