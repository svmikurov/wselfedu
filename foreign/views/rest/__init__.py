"""Django REST framework views package."""

from foreign.views.rest.exercise import (
    exercise_parameters,
    translate_exercise,
    update_word_assessment_view,
)
from foreign.views.rest.word import (
    WordDetailAPIView,
    WordListCreateAPIView,
)

__all__ = (
    'WordDetailAPIView',
    'WordListCreateAPIView',
    'exercise_parameters',
    'translate_exercise',
    'update_word_assessment_view',
)
