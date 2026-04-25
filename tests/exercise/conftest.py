"""Language discipline presentation exercise DI tests."""

import pytest

from apps.core.assemblers.command import UserDataCommand
from apps.core.handlers.dto import RequestContext, RequestData
from apps.users.models import Person
from di import MainContainer
from interfaces.enums.exercise import ExerciseAction
from interfaces.schemas.base import NullDTO
from interfaces.schemas.request.exercise import ExerciseRequestDTO

from .._types.handler import (
    HandlerT,
    RequestContextT,
    RequestDataT,
    RequestParamsT,
)

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
