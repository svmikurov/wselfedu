"""Learning foreign words app Django ORM queries."""

from english.orm_queries.word_favorites import (
    is_word_in_favorites,
    update_word_favorites_status,
)
from english.orm_queries.word_progress import (
    get_numeric_value,
    get_progress,
    update_progress,
)

__all__ = [
    'get_numeric_value',
    'get_progress',
    'update_progress',
    'is_word_in_favorites',
    'update_word_favorites_status',
]
