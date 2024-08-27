"""Django REST framework views package."""

from english.views_drf.word_drf_views import (
    WordListCreateAPIView,
    WordRetrieveUpdateDestroyAPIView,
)

__all__ = (
    'WordListCreateAPIView',
    'WordRetrieveUpdateDestroyAPIView',
)
