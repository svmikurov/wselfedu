"""Language discipline views."""

__all__ = [
    'IndexLangView',
    'LabelCreateView',
    'LabelUpdateView',
    'LabelDeleteView',
    'LabeDetailView',
    'LabelListView',
    'EnglishTranslationCreateView',
]

from .index import IndexLangView
from .label import (
    LabeDetailView,
    LabelCreateView,
    LabelDeleteView,
    LabelListView,
    LabelUpdateView,
)
from .translation import EnglishTranslationCreateView
