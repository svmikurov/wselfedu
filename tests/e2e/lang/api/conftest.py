"""Word study parameters API test configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from apps.lang import types
from tests.fixtures.lang.no_db import translations as fixtures

if TYPE_CHECKING:
    pass


@pytest.fixture
def public_parameters(
    parameters_db_data: types.CaseSettings,
) -> types.CaseSettings:
    """Provide public Parameters data.

    Contains fields for a user who has no saved settings
    or the field is not set in the user settings.
    """
    return {
        # Parameter options
        'categories': [],
        'marks': [],
        'sources': [],
        'periods': parameters_db_data['periods'],
        'translation_orders': fixtures.TRANSLATION_ORDERS,
        # Selected parameter
        'category': None,
        'mark': None,
        'word_source': None,
        'start_period': None,
        'end_period': None,
        'translation_order': fixtures.TRANSLATION_ORDERS[1],
        'is_study': True,
        'is_repeat': True,
        'is_examine': True,
        'is_know': False,
        # Set parameter
        'word_count': None,
        'question_timeout': 3,
        'answer_timeout': 3,
    }
