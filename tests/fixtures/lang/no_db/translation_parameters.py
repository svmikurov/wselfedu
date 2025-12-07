"""Word study Presentation params data fixtures."""

from typing import Final

from apps.lang import types

# The Word study Presentation parameters consists from data:
# - parameter options
# - selected parameter
# - input parameter value
# - switch parameter boolean value
# - presentation settings

EMPTY_PARAMETERS: Final[types.StudyParameters] = {
    'category': None,
    'mark': None,
    'word_source': None,
    'translation_order': None,
    'start_period': None,
    'end_period': None,
    'is_study': True,
    'is_repeat': True,
    'is_examine': True,
    'is_know': False,
    'word_count': None,
    'question_timeout': None,
    'answer_timeout': None,
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

OPTIONS: types.Options = {
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

TRANSLATION_META: Final[types.TranslationMeta] = {
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

TRANSLATION_SETTINGS: Final[types.TranslationSettings] = {
    'translation_order': TRANSLATION_ORDERS[0],
    'word_count': 90,
    **PROGRESS_PHASE,
}

TRANSLATION_CASE_PARAMETERS: Final[types.WordParameters] = {
    **TRANSLATION_META,
    **TRANSLATION_SETTINGS,
}

PRESENTATION_SETTINGS: Final[types.PresentationSettings] = {
    'question_timeout': 2.0,
    'answer_timeout': 2.5,
}
PRESENTATION_PARAMETERS: Final[types.SetStudyParameters] = {
    **OPTIONS,
    **TRANSLATION_CASE_PARAMETERS,
    **PRESENTATION_SETTINGS,
}
