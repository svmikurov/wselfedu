"""Exercise interface."""

__all__ = (
    # Parameters
    'ExerciseParametersDTO',
    # Exercise domain result
    'PresentationTaskDomainResult',
    'TestTaskDomainResult',
)

from .exercise import (
    PresentationTaskDomainResult,
    TestTaskDomainResult,
)
from .params import ExerciseParametersDTO
