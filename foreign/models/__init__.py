"""Foreign words dictionary models."""

# ruff: noqa: I001 - if fix then a circular import
from foreign.models.word import (
    Word,
    WordProgress,
    WordFavorites,
)
from foreign.models.category import WordCategory
from foreign.models.source import WordSource
from foreign.models.params import WordParams
from foreign.models.analytics import (
    WordAnalytics,
)

__all__ = [
    'Word',
    'WordAnalytics',
    'WordCategory',
    'WordFavorites',
    'WordParams',
    'WordProgress',
    'WordSource',
]
