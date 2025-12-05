"""Test the Word study params endpoint."""

from http import HTTPStatus
from typing import Callable
from unittest.mock import Mock

import pytest
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

import di
from apps.lang.api.v1.views.study import WordStudyViewSet
from apps.lang.repos.abc import WordStudyParamsRepositoryABC
from tests.fixtures.lang.no_db import word_study_params as fixtures


@pytest.fixture
def mock_repository() -> Mock:
    """Mock initial Word study params."""
    mock = Mock(spec=WordStudyParamsRepositoryABC)
    mock.fetch.return_value = fixtures.PRESENTATION_PARAMETERS
    return mock


class TestWordStudyParams:
    """Test Word study params REST API endpoint."""

    @pytest.fixture
    def view(self) -> Callable[[Request], Response]:
        """Provide Word study ViewSet."""
        return WordStudyViewSet.as_view(actions={'get': 'parameters'})

    def test_params_success(
        self,
        api_request_factory: APIRequestFactory,
        view: Callable[[Request], Response],
        mock_repository: Mock,
    ) -> None:
        """Test params success."""
        # Arrange
        request = api_request_factory.get('')
        force_authenticate(request, Mock())

        # Act
        with di.container.lang.params_repo.override(mock_repository):
            response = view(request)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response.data == fixtures.PRESENTATION_PARAMETERS
