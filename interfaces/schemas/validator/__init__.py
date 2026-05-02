"""Request's data validator's interface."""

__all__ = (
    'ValidatedCreateTaskRequest',
    'ValidatedExerciseProgress',
)

from .progress import ValidatedExerciseProgress
from .task import ValidatedCreateTaskRequest
