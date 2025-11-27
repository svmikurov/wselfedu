"""Word study Presentation params data fixtures."""

import pytest

from apps.lang import types

# The Word study Presentation parameters consists from data:
# - parameter options
# - selected parameter
# - set parameter value


@pytest.fixture
def translation_order_options() -> list[types.CodeName]:
    """Provide translation order options.

    Model default option is 'to_native'.
    """
    return [
        {'code': 'from_native', 'name': 'С родного языка'},
        {'code': 'to_native', 'name': 'На родной язык'},
        {'code': 'random', 'name': 'Случайный порядок'},
    ]


@pytest.fixture
def word_presentation_options(
    translation_order_options: list[types.CodeName],
) -> types.ParamOptionsT:
    """Provide Word study Presentation parameter options."""
    return {
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
        'translation_orders': translation_order_options,
    }


@pytest.fixture
def word_presentation_selected(
    translation_order_options: list[types.CodeName],
    word_presentation_options: types.ParamOptionsT,
) -> types.InitialChoicesT:
    """Provide Word study Presentation selected parameters."""
    return {
        'category': word_presentation_options['categories'][0],  # type: ignore
        'mark': word_presentation_options['marks'][1],  # type: ignore
        'word_source': word_presentation_options['sources'][0],  # type: ignore
        'start_period': word_presentation_options['periods'][0],
        'end_period': word_presentation_options['periods'][1],
        'translation_order': translation_order_options[0],
    }


@pytest.fixture
def word_presentation_settings() -> types.PresentationSettingsT:  #
    """Provide Word study Presentation settings."""
    return {
        'word_count': 90,
        'question_timeout': 2.0,
        'answer_timeout': 2.5,
    }


@pytest.fixture
def word_presentation_params(
    word_presentation_options: types.ParamOptionsT,
    word_presentation_selected: types.InitialChoicesT,
    word_presentation_settings: types.PresentationSettingsT,
) -> types.WordPresentationParamsT:
    """Provide Word study Presentation parameters valid data."""
    return {
        **word_presentation_options,
        **word_presentation_selected,
        **word_presentation_settings,
    }
