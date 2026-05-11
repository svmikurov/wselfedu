"""Pytest configuration."""

from unittest.mock import Mock

import pytest

from apps.core.storages.services.iabc import AbstractCommandStorage
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.exercise import UserTranslationsRepository
from apps.users.models import Person
from ports.contract import enums
from ports.contract.infra.repository import RepositoryProtocol
from ports.interfaces.schemas.domain.exercise import ExerciseParametersDTO
from ports.interfaces.schemas.domain.exercise.exercise import (
    TaskItem,
    TestTaskDomainResult,
)
from tests.fixtures.exercise.lang.no_db.translations import (
    TRANSLATION_INDEX,
    TRANSLATIONS,
)

# =================================================
# User
# =================================================


@pytest.fixture
def mock_user() -> Person:
    """Provide user mock."""
    mock = Mock(spec=Person)
    mock.pk.return_value = 1
    return mock


# =================================================
# Exercise parameters
# =================================================


@pytest.fixture
def exercise_params() -> ExerciseParametersDTO:
    """Provide exercise parameters."""
    return ExerciseParametersDTO()


# =================================================
# Exercise data
# =================================================


@pytest.fixture
def translation_repository() -> RepositoryProtocol[object, object]:
    """Provide exercise config.."""
    return UserTranslationsRepository(
        manager=EnglishTranslation.objects,
    )


# =================================================
# Repositories
# =================================================


@pytest.fixture
def mock_user_command_storage(
    translations: list[TaskItem],
) -> Mock:
    """Provide exercise case storage mock."""
    mock = Mock(spec=AbstractCommandStorage)
    mock.name = 'test_task'
    return mock


@pytest.fixture
def translation_task_items() -> list[TaskItem]:
    """Provide translation items without DB creation."""
    return [
        TaskItem(
            pk=pk,
            define=define,
            mean=mean,
            progress_value=0,
        )
        for pk, (define, mean) in enumerate(TRANSLATIONS, start=1)
    ]


@pytest.fixture
def create_translation_test_domain_result(
    translation_task_items: list[TaskItem],
) -> TestTaskDomainResult:
    """Provide create translation test domain result."""
    return TestTaskDomainResult(
        question_option_value=TRANSLATION_INDEX,
        items=translation_task_items,
        status=enums.ExerciseStatus.NEW_TASK,
    )
