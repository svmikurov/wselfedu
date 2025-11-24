"""Language application API documentation response data examples."""

from apps.lang import types

WORD_STUDY_PARAMETERS_DATA: types.WordPresentationParamsT = {
    'categories': [
        {'id': 1, 'name': 'cat 1'},
        {'id': 2, 'name': 'cat 2'},
    ],
    'marks': [
        {'id': 1, 'name': 'mark 1'},
        {'id': 2, 'name': 'mark'},
    ],
    'sources': [
        {'id': 1, 'name': 'source 1'},
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
    'mark': {'id': 2, 'name': 'mark'},
    'word_source': {'id': 1, 'name': 'source 1'},
    'start_period': {'id': 2, 'name': 'week_before'},
    'end_period': {'id': 1, 'name': 'today'},
    'translation_order': {'code': 'to_native', 'name': 'На родной язык'},
    'word_count': 90,
    'question_timeout': 2.0,
    'answer_timeout': 2.5,
}
