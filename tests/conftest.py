"""Pytest configuration."""

from unittest.mock import Mock

import pytest
from django.db.models import QuerySet

from apps.core.assemblers.command import UserDataCommand
from apps.core.handlers.dto import RequestContext, RequestData
from apps.core.repositories.protocol import UserRepositoryProtocol
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.exercise.candidates.translations import (
    UserTranslationsRepository,
)
from apps.users.models import Person
from contracts.enums.exercise import ExerciseAction
from contracts.schemas.base import NullDTO
from contracts.schemas.domain.exercise.params import (
    ExerciseParametersDTO,
)
from contracts.schemas.request.exercise import ExerciseRequestDTO

from ._types.handler import (
    RequestContextT,
    RequestDataT,
    RequestParamsT,
)
from ._types.resource import TranslationCandidates

pytest_plugins = [
    'tests.fixtures.db_user',
    'tests.fixtures.di.container',
    'tests.fixtures.exercise.request_data',
    'tests.fixtures.exercise.lang.db.params',
    'tests.fixtures.exercise.lang.db.translations',
    'tests.fixtures.exercise.lang.no_db.params',
]


@pytest.fixture
def mock_user() -> Person:
    """Provide user mock."""
    return Mock(spec=Person)


# =================================================
# Request's DTOs
# =================================================


@pytest.fixture
def request_params() -> RequestParamsT:
    """Provide request parameters DTO fixture."""
    return NullDTO()


@pytest.fixture
def request_context(
    user: Person,
) -> RequestContextT:
    """Provide request parameters DTO fixture."""
    return RequestContext(user=user)


@pytest.fixture
def request_data_create_task() -> RequestDataT:
    """Provide request parameters DTO fixture."""
    return RequestData(
        data={
            'action': 'create_task',
        },
    )


# =================================================
# Commands
# =================================================


@pytest.fixture
def create_command(
    user: Person,
) -> UserDataCommand[ExerciseRequestDTO]:
    """Provide create exercise command fixture."""
    return UserDataCommand(
        user=user,
        data=ExerciseRequestDTO(
            action=ExerciseAction.CREATE_TASK,
        ),
    )


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
def translation_repository() -> UserRepositoryProtocol[object, object]:
    """Provide exercise config.."""
    return UserTranslationsRepository(
        manager=EnglishTranslation.objects,
    )


@pytest.fixture
def translation_candidates_db(
    user: Person,
    translations: list[EnglishTranslation],  # Populate DB
    translation_repository: UserRepositoryProtocol[
        NullDTO,
        QuerySet[EnglishTranslation],
    ],
) -> TranslationCandidates:
    """Provide translation exercise candidates."""
    return translation_repository.fetch(user, NullDTO())  # type: ignore
