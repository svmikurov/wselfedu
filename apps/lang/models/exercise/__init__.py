"""Language discipline exercises."""

__all__ = [
    'Exercise',
    'EnglishTranslationExercise',
    'EnglishAssignedExercise',
]

from ..assignment.mentorship.exercise import EnglishAssignedExercise
from .exercise import Exercise
from .translation import EnglishTranslationExercise
