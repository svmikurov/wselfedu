"""Translation query fixtures."""

from typing import Final

from apps.lang import types

EMPTY_LOOKUP_CONDITIONS: Final[types.WordParameters] = {
    'category': None,
    'mark': None,
    'word_source': None,
    'start_period': None,
    'end_period': None,
    # TODO: Update type, delete 'word_count', 'translation_order'
    'word_count': None,
    'translation_order': None,
}

TRANSLATIONS: Final[tuple[tuple[str, str], ...]] = (
    ('помидор', 'tomato'),
    ('огурец', 'cucumber'),
    ('яблоко', 'apple'),
    ('белый', 'white'),
    ('черный', 'black'),
    ('красный', 'red'),
    ('зеленый', 'green'),
    ('оранжевый', 'orange'),
    # TODO: Implement 'orange' adding?
    # ('апельсин', 'orange'),
)

CATEGORIES: Final[tuple[str, ...]] = (
    'Colors',
    'Fruits',
)

SOURCES: Final[tuple[str, ...]] = (
    'Traffic light',
    'Chess',
    'Garden',
)

MARKS: Final[tuple[str, ...]] = (
    'Edible',
    'Inedible',
)
