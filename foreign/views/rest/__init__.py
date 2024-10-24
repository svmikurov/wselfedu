"""Django REST framework views package."""

from foreign.views.rest.exercise import (
    exercise_parameters,
)
from foreign.views.rest.word import (
    WordDetailAPIView,
    WordListCreateAPIView,
)

__all__ = (
    'WordDetailAPIView',
    'WordListCreateAPIView',
    'exercise_parameters',
)
