"""Test the Word study ViewSet, `progress` action."""

from http import HTTPStatus
from typing import Callable
from unittest.mock import Mock

import pytest
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.lang import types
from apps.lang.api.v1.views.study import WordStudyViewSet
from apps.lang.services.abc import WordProgressServiceABC
from di import container

from . import cases


@pytest.fixture
def view() -> Callable[[Request], Response]:
    """Provide Word study ViewSet."""
    return WordStudyViewSet.as_view({'post': 'progress'})


@pytest.fixture
def mock_service() -> Mock:
    """Mock word study progress service."""
    return Mock(spec=WordProgressServiceABC)


@pytest.fixture
def valid_payload() -> types.WordProgressType:
    """Mock valid request payload."""
    return cases.VALID_PAYLOAD


class TestProgress:
    """Test the Word study ViewSet, `progress` action."""

    def test_success(
        self,
        mock_user: Mock,
        mock_service: Mock,
        api_request_factory: APIRequestFactory,
        view: Callable[[Request], Response],
        valid_payload: types.WordProgressType,
    ) -> None:
        """Test update progress success."""
        # Arrange
        request = api_request_factory.post('', valid_payload)
        force_authenticate(request, mock_user)

        # Act
        with container.lang.progress_service.override(mock_service):
            response = view(request)

        # Assert
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert response.data is None
        mock_service.update_progress.assert_called_once_with(
            mock_user, valid_payload
        )

    @pytest.mark.parametrize(
        'invalid_payload, expected_errors',
        cases.INVALID_PAYLOAD,
    )
    def test_validation_errors_handling(
        self,
        mock_user: Mock,
        mock_service: Mock,
        api_request_factory: APIRequestFactory,
        view: Callable[[Request], Response],
        invalid_payload: cases.InvalidPayload,
        expected_errors: cases.SerializerErrors,
    ) -> None:
        """Test update progress validation errors."""
        # Arrange
        request = api_request_factory.post('', invalid_payload)
        force_authenticate(request, mock_user)

        # Act
        with container.lang.progress_service.override(mock_service):
            response = view(request)

        # Assert
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.data == expected_errors
        mock_service.update_progress.assert_not_called()

    @pytest.mark.parametrize(
        'exception, expected_detail',
        cases.SERVICE_ERROR,
    )
    def test_service_errors_handling(
        self,
        mock_user: Mock,
        mock_service: Mock,
        api_request_factory: APIRequestFactory,
        view: Callable[[Request], Response],
        valid_payload: types.WordProgressType,
        exception: cases.ServiceErrors,
        expected_detail: str,
    ) -> None:
        """Test update progress service exception."""
        # Arrange
        request = api_request_factory.post('', valid_payload)
        force_authenticate(request, mock_user)
        mock_service.update_progress.side_effect = exception

        # Act
        with container.lang.progress_service.override(mock_service):
            response = view(request)

        # Assert
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.data == {'detail': expected_detail}
        mock_service.update_progress.assert_called_once_with(
            mock_user, valid_payload
        )
