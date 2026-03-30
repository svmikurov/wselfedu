"""Base exercise views."""

__all__ = (
    # TypeAlias
    'DetailHandler',
    'QueryHandler',
    # Views
    'StartExerciseView',
    'ProcessExerciseView',
    'ExercisePerformView',
    'DeprecatedExercisePerformView',
    'QueryExercisePerformView',
    'DetailExercisePerformView',
)

from .base import (
    DeprecatedExercisePerformView,
    DetailExercisePerformView,
    DetailHandler,
    ExercisePerformView,
    ProcessExerciseView,
    QueryExercisePerformView,
    QueryHandler,
    StartExerciseView,
)
