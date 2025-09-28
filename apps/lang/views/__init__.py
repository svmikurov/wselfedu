"""Language discipline views."""

__all__ = [
    'IndexLangView',
    'LabelCreateView',
    'LabelUpdateView',
    'LabelDeleteView',
    'LabeDetailView',
    'LabelListView',
]

from .index import IndexLangView
from .label import (
    LabeDetailView,
    LabelCreateView,
    LabelDeleteView,
    LabelListView,
    LabelUpdateView,
)
