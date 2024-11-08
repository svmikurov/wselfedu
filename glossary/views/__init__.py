"""Glossary app views."""

from glossary.views.category import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
)
from glossary.views.exercise import (
    GlossaryParamsView,
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
    'TermListView',
    'TermUpdateView',
)
