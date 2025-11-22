"""Word study Presentation params data fixtures."""

import pytest

from apps.lang import types

# The Word study Presentation parameters consists from data:
# - parameter options
# - selected parameter
# - settings for presentation performance


@pytest.fixture
def options() -> types.ParamsChoicesT:
    """Provide Word study Presentation parameter options."""
    return {
        'categories': [{'id': 1, 'name': 'category'}],
        'marks': [{'id': 2, 'name': 'mark'}],
        'sources': [{'id': 3, 'name': 'source'}],
        'periods': [{'id': 4, 'name': 'source'}],
    }


@pytest.fixture
def selected() -> types.InitialChoicesT:
    """Provide Word study Presentation selected parameters."""
    return {
        'category': {'id': 1, 'name': 'category'},
        'mark': {'id': 2, 'name': 'mark'},
        'word_source': {'id': 3, 'name': 'source'},
        'order': None,
        'start_period': None,
        'end_period': None,
    }


@pytest.fixture
def settings() -> types.PresentationSettingsT:
    """Provide Word study Presentation settings."""
    return {
        'word_count': None,
        'question_timeout': None,
        'answer_timeout': None,
    }
