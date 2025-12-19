"""Language discipline fixtures."""

import uuid
from unittest.mock import Mock

import pytest

from apps.core.storage.services import TaskStorage
from apps.lang import schemas, services, types
from apps.lang.repositories.abc import ProgressABC

from .api.v1.view.study import cases

# Data fixtures
# -------------


@pytest.fixture
def stored_case() -> schemas.WordStudyStoredCase:
    """Provide Word study case data."""
    return schemas.WordStudyStoredCase(
        translation_id=1,
        language='english',
    )


@pytest.fixture
def progress_config() -> schemas.ProgressConfigSchema:
    """Word study progress config schema."""
    return schemas.ProgressConfigSchema(
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
    return Mock(spec=ProgressABC)


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
    progress_config: schemas.ProgressConfigSchema,
) -> services.UpdateWordProgressService:
    """Test Word study progress update service."""
    return services.UpdateWordProgressService(
        progress_repo=mock_progress_repo,
        case_storage=mock_task_storage,
        progress_config=progress_config,
    )
