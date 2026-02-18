"""Calculation exercise views."""

__all__ = [
    # Custom calculation exercises
    'CalculationListView',
    'CalculationCreateView',
    'CalculationUpdateView',
    'CalculationDeleteView',
    # Mentors's assigned calculation exercises
    'AssignedCalculationConditionMentorListView',
    'AssignedCalculationConditionMentorCreateView',
    'AssignedCalculationConditionMentorDeleteView',
    # Student's assigned calculation exercises
    'AssignedCalculationExerciseStudentListVew',
    # Calculation exercise performing
    'DetailPerformView',
    'ExerciseChoiceView',
    'RegularPerformView',
    'AssignedPerformView',
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
from .student import (
    AssignedCalculationExerciseStudentListVew,
)
