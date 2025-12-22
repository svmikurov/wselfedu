"""Language application API documentation response data examples."""

from apps.lang import types

SET_WORD_STUDY_PARAMETERS_DATA: types.CaseSettingsAPI = {
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
    'periods': [
        {'id': 1, 'name': 'today'},
        {'id': 2, 'name': 'week_before'},
    ],
    'translation_orders': [
        {'code': 'from_native', 'name': 'С родного языка'},
        {'code': 'to_native', 'name': 'На родной язык'},
        {'code': 'random', 'name': 'Случайный порядок'},
    ],
    'category': {'id': 1, 'name': 'cat 1'},
    'mark': {'id': 2, 'name': 'mark 2'},
    'word_source': {'id': 1, 'name': 'source 1'},
    'start_period': {'id': 2, 'name': 'week_before'},
    'end_period': {'id': 1, 'name': 'today'},
    'translation_order': {'code': 'to_native', 'name': 'На родной язык'},
    'is_study': True,
    'is_repeat': True,
    'is_examine': True,
    'is_know': False,
    'word_count': 90,
    'question_timeout': 3,
    'answer_timeout': 5,
}

WORD_STUDY_PARAMETERS_DATA: types.CaseParametersAPI = {
    'category': {'id': 1, 'name': 'cat 1'},
    'mark': {'id': 2, 'name': 'mark 2'},
    'word_source': {'id': 1, 'name': 'source 1'},
    'start_period': {'id': 2, 'name': 'week_before'},
    'end_period': {'id': 1, 'name': 'today'},
    'translation_order': {'code': 'to_native', 'name': 'На родной язык'},
    'is_study': True,
    'is_repeat': True,
    'is_examine': True,
    'is_know': False,
    'word_count': 90,
}
