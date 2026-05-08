"""Request's data validator's interface."""

__all__ = (
    'ValidatedCreateTaskRequest',
    'ValidatedCheckTestTaskRequest',
    'ValidatedExerciseProgress',
)

from .progress import ValidatedExerciseProgress
from .task import ValidatedCheckTestTaskRequest, ValidatedCreateTaskRequest
