"""Request's data validator's interface."""

__all__ = (
    'ValidatedCreateTask',
    'ValidatedCheckTestAnswer',
    'ValidatedExerciseProgress',
)

from .progress import ValidatedExerciseProgress
from .task import ValidatedCheckTestAnswer, ValidatedCreateTask
