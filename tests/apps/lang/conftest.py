"""Request exercise request parameters test configurations."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
from django.test import RequestFactory

from apps.users.models import Person

if TYPE_CHECKING:
    from django.test import Client

    from di import MainContainer
    from ports.contract.types.handler import PresentationHandlerT


# =================================================
# Django Person model
# =================================================


@pytest.fixture
def person_schema() -> Person:
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
# Dependencies
# =================================================


@pytest.fixture
def regular_translation_presentation(
    main_container: MainContainer,
) -> PresentationHandlerT:
    """Provide regular translation presentation exercise handler."""
    return main_container.lang.handlers.regular_translation_presentation  # type: ignore


@pytest.fixture
def regular_translation_test(
    main_container: MainContainer,
) -> PresentationHandlerT:
    """Provide regular translation test exercise handler."""
    return main_container.lang.handlers.regular_translation_test  # type: ignore


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
