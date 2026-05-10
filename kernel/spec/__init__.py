"""Specification factories."""

__all__ = (
    # Exercise
    'CheckAnswerSpecFactory',
    'CreateExerciseSpecFactory',
    # Progress
    'UpdateProgressSpecFactory',
)

from .exercise import CheckAnswerSpecFactory, CreateExerciseSpecFactory
from .progress import UpdateProgressSpecFactory
