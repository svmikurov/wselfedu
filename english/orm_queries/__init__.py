"""English app Django ORM queries."""

from english.orm_queries.word_favorites import (
    is_word_in_favorites,
    update_word_favorites_status,
)
from english.orm_queries.word_knowledge_assessment import (
    get_knowledge_assessment,
    get_numeric_value,
    update_word_knowledge_assessment,
)

__all__ = [
    'get_numeric_value',
    'get_knowledge_assessment',
    'update_word_knowledge_assessment',
    'is_word_in_favorites',
    'update_word_favorites_status',
]
