"""Language discipline fixtures."""

import uuid
from unittest.mock import Mock

import pytest

from apps.core.domains.exercise import ProgressConfigSchema
from apps.core.storages.services import TaskStorage
from apps.lang import types, use_cases
from apps.lang.repositories.abc import ProgressRepositoryABC
from apps.lang.schemas import dto

from .api.v1.view.study import cases

# Data fixtures
# -------------


@pytest.fixture
def stored_case() -> dto.CaseMeta:
    """Provide Word study case data."""
    return dto.CaseMeta(
        pk=1,
    )


@pytest.fixture
def progress_config() -> ProgressConfigSchema:
    """Word study progress config schema."""
    return ProgressConfigSchema(
        increment=1,
        decrement=1,
    )


@pytest.fixture
def progress_case() -> types.ProgressCase:
    """Provide valid word study progress update case."""
    return cases.VALID_PAYLOAD


# Mocked dependency fixtures
# --------------------------


@pytest.fixture
def mock_progress_repo() -> Mock:
    """Mock Word study progress repo fixture."""
    return Mock(spec=ProgressRepositoryABC)


@pytest.fixture
def mock_task_storage(
    case_uuid: uuid.UUID,
) -> Mock:
    """Mock task storage fixture."""
    mock = Mock(spec=TaskStorage)
    mock.save_task.return_value = case_uuid
    return mock


@pytest.fixture
def progress_service_di_mock(
    mock_progress_repo: Mock,
    mock_task_storage: Mock,
    progress_config: ProgressConfigSchema,
) -> use_cases.ProgressService:
    """Test Word study progress update service."""
    return use_cases.ProgressService(
        repository=mock_progress_repo,
        case_storage=mock_task_storage,
        config=progress_config,
    )
