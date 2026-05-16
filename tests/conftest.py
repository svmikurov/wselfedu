"""Pytest configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from apps.users.models import Person
from ports.contract.enums import ExerciseAction
from ports.interfaces.schemas.request.handler import RequestData

from .fixtures.exercise.lang.no_db.translations import TRANSLATION_INDEX

if TYPE_CHECKING:
    from ._types import (
        CheckRequestDataT,
        CreateRequestDataT,
        UpdateProgressRequestDataT,
    )

pytest_plugins = [
    'tests.fixtures.db_user',
    'tests.fixtures.di',
    'tests.fixtures.exercise.request_data',
    'tests.fixtures.exercise.lang.db.params',
    'tests.fixtures.exercise.lang.db.translations',
    'tests.fixtures.exercise.lang.no_db.params',
]


@pytest.fixture
def mock_user() -> Person:
    """Provide user mock."""
    mock = Mock(spec=Person)
    mock.pk = 1
    return mock


# =================================================
# Exercise WEB request data
# =================================================


@pytest.fixture
def create_task_request_data() -> CreateRequestDataT:
    """Provide create exercise request's data DTO."""
    # Request data DTO creates in view's method with GET request.
    return RequestData(
        data={
            'action': ExerciseAction.CREATE_TASK,
        },
    )


@pytest.fixture
def check_test_answer_request_data() -> CheckRequestDataT:
    """Provide check exercise request's data DTO."""
    # Request data DTO creates in view's method with GET request.
    return RequestData(
        data={
            'action': ExerciseAction.CHECK_ANSWER,
            'option_value': str(TRANSLATION_INDEX),
        },
    )


@pytest.fixture
def update_progress_request_data() -> UpdateProgressRequestDataT:
    """Provide *update progress* request data fixture."""
    return RequestData(
        data={
            'action': ExerciseAction.UPDATE_PROGRESS,
            'is_known': 'true',
        }
    )
