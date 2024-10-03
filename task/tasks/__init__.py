"""Task modules."""

from task.models import (
    ForeignExerciseSettings,
    Points,
)
from task.tasks.calculation_exercise import (
    CalculationExercise,
    CalculationExerciseCheck,
)
from task.tasks.foreign_exercise import ForeignWordTranslateExercise

__all__ = [
    'CalculationExercise',
    'CalculationExerciseCheck',
    'ForeignExerciseSettings',
    'ForeignWordTranslateExercise',
    'Points',
]
