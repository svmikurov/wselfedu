"""Django REST framework views package."""

from foreign.views.rest.exercise import (
    foreign_exercise_view,
    foreign_selected_view,
    foreign_params_view,
    update_word_assessment_view,
)
from foreign.views.rest.word import (
    WordDetailAPIView,
    WordListCreateAPIView,
)

__all__ = (
    'WordDetailAPIView',
    'WordListCreateAPIView',
    'foreign_params_view',
    'foreign_exercise_view',
    'foreign_selected_view',
    'update_word_assessment_view',
)
