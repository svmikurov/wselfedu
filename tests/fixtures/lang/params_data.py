"""Word study Presentation params data fixtures."""

import pytest

from apps.lang import types

# The Word study Presentation parameters consists from data:
# - choices for each parameter
# - initial parameter choice
# - settings for presentation performance


@pytest.fixture
def choices() -> types.ParamsChoicesT:
    """Provide Word study Presentation params choices."""
    return {
        'categories': [{'id': 1, 'name': 'category'}],
        'marks': [{'id': 2, 'name': 'mark'}],
        'sources': [{'id': 3, 'name': 'source'}],
        'periods': [{'id': 4, 'name': 'source'}],
    }


@pytest.fixture
def initial() -> types.InitialChoicesT:
    """Provide Word study Presentation params choices."""
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


# TODO: Add fixture
# @pytest.fixture
# def populate_db_with_params_data() -> None:
#     """Populate Database with test params data."""
