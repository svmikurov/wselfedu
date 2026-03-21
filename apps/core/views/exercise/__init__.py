"""Base exercise views."""

__all__ = (
    # TypeAlias
    'DetailHandler',
    'QueryHandler',
    # Views
    'ExercisePerformView',
    'QueryExercisePerformView',
    'DetailExercisePerformView',
)

from .base import (
    DetailExercisePerformView,
    DetailHandler,
    ExercisePerformView,
    QueryExercisePerformView,
    QueryHandler,
)
