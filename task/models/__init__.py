"""Task app models module."""

from task.models.exercises_math import MathematicalExercise
from task.models.points import Points
from task.models.task_settings import ForeignExerciseSettings

__all__ = (
    'MathematicalExercise',
    'Points',
    'ForeignExerciseSettings',
)
