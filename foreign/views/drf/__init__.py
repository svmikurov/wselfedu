"""Django REST framework views package."""

from foreign.views.drf.exercise import (
    exercise_parameters,
)
from foreign.views.drf.word import (
    WordDetailAPIView,
    WordListCreateAPIView,
)

__all__ = (
    'WordDetailAPIView',
    'WordListCreateAPIView',
    'exercise_parameters',
)
