"""Pytest configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from apps.core.storages.services.iabc import AbstractCommandStorage
from apps.users.models import Person
from ports.contract.enums import ExerciseAction
from ports.interfaces.schemas.request.handler import (
    RequestContext,
    RequestData,
)

from .fixtures.exercise.lang.no_db.translations import TRANSLATION_INDEX

if TYPE_CHECKING:
    from ports.interfaces.protocols.handler.exercise import (
        CheckRequestDataT,
        CreateRequestDataT,
        UpdateProgressRequestDataT,
    )
    from ports.interfaces.protocols.request.general import (
        RequestContextProtocol,
    )
    from ports.interfaces.schemas.domain.exercise.exercise import TaskItem


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
# Exercise WEB request handler attributes
# =================================================


@pytest.fixture
def request_context(
    user: Person,
) -> RequestContextProtocol:
    """Provide request parameters DTO fixture."""
    return RequestContext(user=user)


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


# =================================================
# Request handler attributes mock
# =================================================


@pytest.fixture
def mock_request_params() -> Mock:
    """Provide request parameters DTO mock."""
    return Mock()


@pytest.fixture
def mock_request_context(
    mock_user: Person,
) -> Mock:
    """Provide request context DTO mock."""
    mock = Mock()
    mock.user.return_value = mock_user
    return mock


@pytest.fixture
def mock_request_data() -> Mock:
    """Provide request data DTO mock."""
    return Mock()


# =================================================
# Request handler inner variable mock
# =================================================


@pytest.fixture
def mock_validated() -> Mock:
    """Provide validated request data DTO mock."""
    return Mock()


@pytest.fixture
def mock_command() -> Mock:
    """Provide command data DTO mock."""
    return Mock()


@pytest.fixture
def mock_use_case_result() -> Mock:
    """Provide use case result DTO mock."""
    return Mock()


# =================================================
# Request handler result mock
# =================================================


@pytest.fixture
def mock_response_data() -> Mock:
    """Provide request handler response DTO mock."""
    return Mock()


# =================================================
# Storage mock
# =================================================


@pytest.fixture
def mock_user_command_storage(
    translations: list[TaskItem],
) -> Mock:
    """Provide exercise case storage mock."""
    mock = Mock(spec=AbstractCommandStorage)
    mock.name = 'test_task'
    return mock
