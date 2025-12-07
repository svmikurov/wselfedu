"""Translation query fixtures."""

import uuid
from typing import Final

from apps.lang import types

# Translations
# ~~~~~~~~~~~~

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

# Translation case
# ~~~~~~~~~~~~~~~~

TRANSLATION_CASE_UUID: Final[uuid.UUID] = uuid.UUID(
    '5b518a3e-45a4-4147-a097-0ed28211d8a4'
)

PRESENTATION: Final[types.PresentationDataT] = {
    'definition': 'house',
    'explanation': 'дом',
    'info': {'progress': 7},
}

PRESENTATION_CASE: Final[types.PresentationCaseT] = {
    'case_uuid': TRANSLATION_CASE_UUID,
    **PRESENTATION,
}

# Translation meta
# ~~~~~~~~~~~~~~~~

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

# Translation parameters
# ~~~~~~~~~~~~~~~~~~~~~~

EMPTY_LOOKUP_CONDITIONS: Final[types.WordParameters] = {
    'category': None,
    'mark': None,
    'word_source': None,
    'start_period': None,
    'end_period': None,
    'is_study': True,
    'is_repeat': True,
    'is_examine': True,
    'is_know': False,
    'word_count': None,
    'translation_order': None,
}
