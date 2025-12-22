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

PRESENTATION_CASE: Final[types.TranslationCase] = {
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

EMPTY_TRANSLATION_PARAMETERS: Final[types.CaseParametersAPI] = {
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

TRANSLATION_ORDERS: Final[list[types.CodeName]] = [
    {'code': 'from_native', 'name': 'С родного языка'},
    {'code': 'to_native', 'name': 'На родной язык'},
    {'code': 'random', 'name': 'Случайный порядок'},
]

PERIODS: Final[list[types.IdName]] = [
    {'id': 1, 'name': 'today'},
    {'id': 2, 'name': 'yesterday'},
    {'id': 3, 'name': 'to days before'},
]

OPTIONS: types.OptionsAPI = {
    'categories': [
        {'id': 1, 'name': 'cat 1'},
        {'id': 2, 'name': 'cat 2'},
    ],
    'marks': [
        {'id': 1, 'name': 'mark 1'},
        {'id': 2, 'name': 'mark 2'},
    ],
    'sources': [
        {'id': 1, 'name': 'source 1'},
        {'id': 2, 'name': 'source 2'},
    ],
    'periods': PERIODS,
    'translation_orders': TRANSLATION_ORDERS,
}

TRANSLATION_PARAMETERS: Final[types.TranslationParametersAPI] = {
    'category': OPTIONS['categories'][0],
    'mark': OPTIONS['marks'][1],
    'word_source': OPTIONS['sources'][0],
    'start_period': OPTIONS['periods'][0],
    'end_period': OPTIONS['periods'][1],
}

PROGRESS_PHASE: Final[types.ProgressPhase] = {
    'is_study': True,
    'is_repeat': True,
    'is_examine': True,
    'is_know': False,
}

TRANSLATION_SETTINGS: Final[types.TranslationSettingsAPI] = {
    # Database default translation order: to native
    'translation_order': TRANSLATION_ORDERS[1],
    'word_count': 90,
}

PRESENTATION_SETTINGS: Final[types.PresentationSettings] = {
    'question_timeout': 2,
    'answer_timeout': 5,
}

TRANSLATION_CASE_PARAMETERS: Final[types.CaseParametersAPI] = {
    **TRANSLATION_PARAMETERS,
    **PROGRESS_PHASE,
    **TRANSLATION_SETTINGS,
}

PRESENTATION_PARAMETERS: Final[types.CaseSettingsAPI] = {
    **OPTIONS,
    **TRANSLATION_CASE_PARAMETERS,
    **PRESENTATION_SETTINGS,
}
