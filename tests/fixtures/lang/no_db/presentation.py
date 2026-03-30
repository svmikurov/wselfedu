"""Translation presentation **request** test fixtures."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from apps.core.domains.exercise import DisplayOrder
from apps.lang import schemas

if TYPE_CHECKING:
    from tests.types import ApiRequest, WebRequestRaw

CATEGORY_ID = 1
START_PERIOD_ID = 3
END_PERIOD_ID = 1
WORD_COUNT = 90

# ----------------
# Web request data
# ----------------

EMPTY_WEB_REQUEST: WebRequestRaw = {
    # Translation parameters
    'category': '',
    'mark': [],
    'source': '',
    'start_period': '',
    'end_period': '',
    # Progress phases
    'is_examine': 'true',
    'is_know': 'true',
    'is_repeat': 'true',
    'is_study': 'true',
    # Translation settings
    'display_order': 'to_native',
    'word_count': str(WORD_COUNT),  # Fix to ''
}

WEB_REQUEST = {
    # Translation parameters
    'category': str(CATEGORY_ID),
    'mark': ['1', '2'],
    'source': '',
    'start_period': str(START_PERIOD_ID),
    'end_period': str(END_PERIOD_ID),
    # Progress phases
    'is_examine': 'true',
    'is_know': 'true',
    'is_repeat': 'false',
    'is_study': 'false',
    # Translation settings
    'display_order': 'random',
    'item_count': str(WORD_COUNT),
}


# -----------------
# Api request data
# ----------------


API_REQUEST: Final[ApiRequest] = {
    # Translation parameters
    'category': {'id': CATEGORY_ID, 'name': 'cat 1'},
    'mark': [
        {'id': 1, 'name': 'mark 1'},
        {'id': 2, 'name': 'mark 2'},
    ],
    'word_source': None,
    'start_period': {'id': START_PERIOD_ID, 'name': 'to days before'},
    'end_period': {'id': END_PERIOD_ID, 'name': 'today'},
    # Progress phases
    'is_study': False,
    'is_repeat': False,
    'is_examine': True,
    'is_know': True,
    # Translation settings
    'display_order': {'code': 'random', 'name': 'Случайный порядок'},
    'word_count': WORD_COUNT,
}


# --------------
# Validated data
# --------------

EMPTY_PARAMETERS_DTO = schemas.LookupConditionsDTO(
    category=None,
    mark=[],
    source=None,
    start_period=None,
    end_period=None,
    is_study=True,
    is_repeat=True,
    is_examine=True,
    is_know=True,
)

PARAMETERS_DTO = schemas.LookupConditionsDTO(
    category=CATEGORY_ID,
    source=None,
    mark=[1, 2],
    start_period=START_PERIOD_ID,
    end_period=END_PERIOD_ID,
    is_study=False,
    is_repeat=False,
    is_examine=True,
    is_know=True,
)
SETTINGS_DTO = schemas.ExerciseConfigDTO(
    display_order=DisplayOrder.RANDOM,
    item_count=WORD_COUNT,
)
REQUEST_DTO: Final = schemas.ExerciseParametersDTO(
    parameters=PARAMETERS_DTO,
    conf=SETTINGS_DTO,
)
