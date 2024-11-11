"""Glossary app views."""

from glossary.views.category import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
)
from glossary.views.exercise import (
    GlossaryParamsView,
    TermExerciseView,
    update_term_favorite_status_view_ajax,
    update_term_study_progress,
)
from glossary.views.source import (
    SourceCreateView,
    SourceDeleteView,
    SourceListView,
    SourceUpdateView,
)
from glossary.views.term import (
    TermCreateView,
    TermDeleteView,
    TermDetailView,
    TermListView,
    TermUpdateView,
)

__all__ = (
    'CategoryCreateView',
    'CategoryDeleteView',
    'CategoryListView',
    'CategoryUpdateView',
    'GlossaryParamsView',
    'SourceCreateView',
    'SourceDeleteView',
    'SourceListView',
    'SourceUpdateView',
    'TermCreateView',
    'TermDeleteView',
    'TermDetailView',
    'TermExerciseView',
    'TermListView',
    'TermUpdateView',
    'update_term_study_progress',
    'update_term_favorite_status_view_ajax',
)
