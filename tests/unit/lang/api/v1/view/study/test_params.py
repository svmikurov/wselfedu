"""Test the Word study parameters endpoint."""

from http import HTTPStatus
from typing import Callable
from unittest.mock import Mock

import pytest
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

import di
from apps.lang.api.v1.views.study import WordStudyViewSet
from apps.lang.repositories.abc import WordStudyParamsRepositoryABC
from tests.fixtures.lang.no_db import translation as fixtures


@pytest.fixture
def mock_repository() -> Mock:
    """Mock initial Word study parameters."""
    mock = Mock(spec=WordStudyParamsRepositoryABC)
    mock.fetch.return_value = fixtures.PRESENTATION_PARAMETERS
    return mock


class TestWordStudyParams:
    """Test Word study parameters REST API endpoint."""

    @pytest.fixture
    def view(self) -> Callable[[Request], Response]:
        """Provide Word study ViewSet."""
        return WordStudyViewSet.as_view(actions={'get': 'parameters'})

    def test_parameters_success(
        self,
        api_request_factory: APIRequestFactory,
        view: Callable[[Request], Response],
        mock_repository: Mock,
    ) -> None:
        """Test parameters success."""
        # Arrange
        request = api_request_factory.get('')
        force_authenticate(request, Mock())

        # Act
        with di.container.lang.parameters_repository.override(mock_repository):
            response = view(request)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response.data == fixtures.PRESENTATION_PARAMETERS
