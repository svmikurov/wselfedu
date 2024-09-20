"""Django REST framework views package."""

from english.views_drf.word_drf_views import (
    WordDetailAPIView,
    WordListCreateAPIView,
)

__all__ = (
    'WordDetailAPIView',
    'WordListCreateAPIView',
)
