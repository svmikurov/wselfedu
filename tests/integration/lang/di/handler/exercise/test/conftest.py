"""Language discipline presentation exercise DI tests."""

import pytest

from apps.core.assemblers.command import UserDataCommand
from apps.core.domains.exercise.enums import ExerciseProcessEnum
from apps.core.domains.null import NullDTO
from apps.core.handlers.dto import RequestContext, RequestData
from apps.core.validators.request.dto import ExerciseActionWebDTO
from apps.users.models import Person
from di import MainContainer

from ._types import HandlerT, RequestContextT, RequestDataT, RequestParamsT

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
            'action': 'create_case',
        },
    )


# =================================================
# Commands
# =================================================


@pytest.fixture
def create_command(
    user: Person,
) -> UserDataCommand[ExerciseActionWebDTO]:
    """Provide create exercise command fixture."""
    return UserDataCommand(
        user=user,
        data=ExerciseActionWebDTO(
            action=ExerciseProcessEnum.CREATE_CASE,
        ),
    )


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
