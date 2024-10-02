"""ORM queries of the Learning foreign words application."""

from foreign.queries.favorites import (
    is_word_in_favorites,
    update_word_favorites_status,
)
from foreign.queries.progress import (
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
