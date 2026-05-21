"""Exercise interface."""

__all__ = (
    # Parameters
    'ExerciseParametersDTO',
    # Exercise domain result
    'PresentationTaskDomainResult',
    'TestTaskDomainResult',
    'ExplainTaskResult',
)

from .exercise import (
    ExplainTaskResult,
    PresentationTaskDomainResult,
    TestTaskDomainResult,
)
from .params import ExerciseParametersDTO
