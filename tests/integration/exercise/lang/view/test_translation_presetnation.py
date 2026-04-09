"""Translation presentation exercise view test."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
from django.test import RequestFactory

from apps.core.adapters.response.dto import ResponseDTO
from apps.core.adapters.response.status import ResponseStatusEnum
from apps.core.domains.null import NullDTO
from apps.core.handlers import RequestHandler
from apps.lang.views.exercise.translation.presentation import (
    TranslationPresentationView,
)

if TYPE_CHECKING:
    from apps.lang.di.handler.web.container import WebHandlerContainer
    from apps.users.models import Person
    from di import MainContainer


@pytest.fixture
def handlers(main_container: MainContainer) -> WebHandlerContainer:
    """Provide lang app use cases DI container."""
    return main_container.lang.handlers  # type: ignore


@pytest.fixture
def mock_handler() -> Mock:
    """Provide request handler mock."""
    mock = Mock(spec=RequestHandler)
    # View has exercise process result status mapping.
    mock.execute.return_value = ResponseDTO(
        status=ResponseStatusEnum.NEW_CASE,
        context=NullDTO(),
    )
    return mock


@pytest.mark.django_db
class TestTranslationPresentationView:
    """Translation presentation exercise view test."""

    def test_get_request_with_handler_mock(
        self,
        user: Person,
        handlers: WebHandlerContainer,
        mock_handler: Mock,
    ) -> None:
        """Test GET request success with request handler mock."""
        # Arrange
        request = RequestFactory().get('')
        request.user = user

        # Act
        with handlers.process_regular_translation_presentation.override(  # type: ignore[unused-ignore]
            mock_handler
        ):
            response = TranslationPresentationView.as_view()(request)

        # Assert
        assert response.status_code == HTTPStatus.OK

    def test_post_request_with_handler_mock(
        self,
        user: Person,
        handlers: WebHandlerContainer,
        mock_handler: Mock,
    ) -> None:
        """Test POST request success with request handler mock."""
        # Arrange
        request = RequestFactory().post('')
        request.user = user

        # Act
        with handlers.process_regular_translation_presentation.override(  # type: ignore[unused-ignore]
            mock_handler
        ):
            response = TranslationPresentationView.as_view()(request)

        # Assert
        assert response.status_code == HTTPStatus.OK
