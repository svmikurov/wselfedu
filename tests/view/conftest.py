"""View test configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
from django.test import RequestFactory

from apps.core.handlers import RequestHandler
from contracts.enums.exercise import ExerciseStatus
from contracts.schemas.base import NullDTO
from contracts.schemas.response.generic import ResponseDTO

if TYPE_CHECKING:
    from django.core.handlers.wsgi import WSGIRequest

    from apps.lang.di.handler.web.container import WebHandlerContainer
    from apps.users.models import Person
    from di import MainContainer

# =================================================
# Handler fixtures
# =================================================


@pytest.fixture
def handlers(main_container: MainContainer) -> WebHandlerContainer:
    """Provide lang app use cases DI container."""
    return main_container.lang.handlers  # type: ignore


@pytest.fixture
def mock_create_exercise_action_handler() -> Mock:
    """Provide request handler mock."""
    mock = Mock(spec=RequestHandler)
    # View has exercise process result status mapping.
    mock.execute.return_value = ResponseDTO(
        domain_status=ExerciseStatus.NEW_TASK,
        context=NullDTO(),
    )
    return mock


# =================================================
# HTTP Request fixtures
# =================================================


@pytest.fixture
def request_get_method(user: Person) -> WSGIRequest:
    """Provide request with GET method fixture."""
    request = RequestFactory().get('')
    request.user = user
    return request


@pytest.fixture
def request_post_method(user: Person) -> WSGIRequest:
    """Provide request with POST method fixture."""
    request = RequestFactory().post('')
    request.user = user
    return request
