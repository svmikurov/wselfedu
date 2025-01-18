"""Term app DRF views."""

from glossary.views.rest.exercise import (
    glossary_exercise_view,
    glossary_params_view,
    glossary_selected_view,
    update_term_favorites_view,
    update_term_progress_view,
)
from glossary.views.rest.term import (
    TermDetailAPIView,
    TermListCreateAPIView,
)

__all__ = [
    'TermDetailAPIView',
    'TermListCreateAPIView',
    'glossary_exercise_view',
    'glossary_params_view',
    'glossary_selected_view',
    'update_term_favorites_view',
    'update_term_progress_view',
]