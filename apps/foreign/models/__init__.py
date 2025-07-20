"""Contains foreign app models."""

__all__ = [
    'ForeignExercise',
    'SyntaxTask',
    'TranslationTestTask',
]

from .exercise import ForeignExercise
from .syntax import SyntaxTask
from .translate import TranslationTestTask
