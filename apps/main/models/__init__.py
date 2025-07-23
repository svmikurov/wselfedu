"""Contains main app models."""

__all__ = [
    'BaseExercise',
    'BaseTask',
    'Discipline',
]

from .base.exercise import BaseExercise
from .base.task import BaseTask
from .discipline import Discipline
