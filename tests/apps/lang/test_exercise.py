"""Language discipline web request tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
from django.urls import reverse_lazy

if TYPE_CHECKING:
    from django.test import Client

    from apps.users.models import Person
    from di import MainContainer


@pytest.fixture
def mock_handler() -> Mock:
    """Provide request handler mock."""
    mock_schema = Mock()
    mock_schema.model_dump.return_value = {}

    mock_handler_result = Mock()
    mock_handler_result.context = mock_schema

    mock_handler = Mock()
    mock_handler.execute.return_value = mock_handler_result
    return mock_handler


@pytest.fixture
def auth_client(user: Person, client: Client) -> Client:
    """Provide authenticated client."""
    client.force_login(user)
    return client


@pytest.mark.django_db
class TestPresentationExerciseRequest:
    """Presentation exercise web request tests."""

    def test_create_task(
        self,
        auth_client: Client,
        main_container: MainContainer,
        mock_handler: Mock,
    ) -> None:
        """Test the create presentation exercise request."""
        # Arrange
        url = reverse_lazy('lang:translation_english_study')
        handler = main_container.lang.handlers.regular_translation_presentation  # type: ignore

        # Act
        with handler.override(mock_handler):
            response = auth_client.get(url)

            # Assert
            assert response.status_code == HTTPStatus.OK
