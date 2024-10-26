"""Django REST framework views package."""

from foreign.views.rest.exercise import (
    exercise_view,
    params_view,
    update_word_assessment_view,
)
from foreign.views.rest.word import (
    WordDetailAPIView,
    WordListCreateAPIView,
)

__all__ = (
    'WordDetailAPIView',
    'WordListCreateAPIView',
    'params_view',
    'exercise_view',
    'update_word_assessment_view',
)
