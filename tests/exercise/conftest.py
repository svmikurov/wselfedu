"""Language discipline presentation exercise DI tests."""

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
from di import MainContainer

from .._types.handler import (
    HandlerT,
    RequestContextT,
    RequestDataT,
    RequestParamsT,
)
from .._types.resource import TranslationCandidates

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
    return translation_repository.fetch(user, NullDTO()).order_by('pk')  # type: ignore


# =================================================
# Tested handler
# =================================================


@pytest.fixture
def regular_presentation_handler(
    main_container: MainContainer,
) -> HandlerT:
    """Provide translation regular presentation exercise handler."""
    return (  # type: ignore
        main_container.lang.handlers.process_regular_translation_test()  # type: ignore
    )
