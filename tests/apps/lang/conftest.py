"""Request exercise request parameters test configurations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, TypeVar
from unittest.mock import Mock

import pytest
from django.test import RequestFactory

from apps.users.models import Person
from ports.contract.enums import ExerciseAction
from ports.interfaces.schemas.base import NullDTO
from ports.interfaces.schemas.request.handler import (
    RequestContext,
    RequestData,
)

if TYPE_CHECKING:
    from django.test import Client

    from di import MainContainer

    from ._types import PresentationHandlerT


ParamsT = TypeVar('ParamsT')

# =================================================
# User
# =================================================


@pytest.fixture
def user_schema() -> Person:
    """Provide user schema fixture."""
    return Person()


# =================================================
# Django request
# =================================================


@pytest.fixture
def auth_client(user: Person, client: Client) -> Client:
    """Provide authenticated client."""
    client.force_login(user)
    return client


@pytest.fixture
def request_factory(mock_user: Person) -> RequestFactory:
    """Provide request factory."""
    factory = RequestFactory()
    factory.user = mock_user  # type: ignore
    return factory


# =================================================
# Request parameters
# =================================================


@dataclass(frozen=True)
class RequestParams(Generic[ParamsT]):
    """Handler request parameters data."""

    params: ParamsT
    context: RequestContext
    data: RequestData[dict[str, Any]]


@pytest.fixture
def create_request_parameters(
    user_schema: Person,
) -> object:
    """Create translation request parameters."""
    return RequestParams(
        params=NullDTO(),
        context=RequestContext(
            user=user_schema,
        ),
        data=RequestData(
            data={
                'action': ExerciseAction.CREATE_TASK,
            },
        ),
    )


# =================================================
# Dependencies
# =================================================


@pytest.fixture
def regular_translation_presentation(
    main_container: MainContainer,
) -> PresentationHandlerT:
    """Provide regular translation presentation handler."""
    return main_container.lang.handlers.regular_translation_presentation  # type: ignore


@pytest.fixture
def mock_handler() -> Mock:
    """Provide request handler mock."""
    mock_context = Mock()
    mock_context.model_dump.return_value = {}

    mock_handler_result = Mock()
    mock_handler_result.context = mock_context

    mock_handler = Mock()
    mock_handler.execute.return_value = mock_handler_result
    return mock_handler
