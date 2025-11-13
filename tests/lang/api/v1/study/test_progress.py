"""Test the Word study progress."""

from http import HTTPStatus
from unittest.mock import Mock

import pytest

from apps.lang.api.v1.views.study import WordStudyViewSet
from apps.lang.services.abc import WordProgressServiceABC
from apps.lang.types import WordProgressType
from di import container

from . import cases


@pytest.fixture
def viewset() -> WordStudyViewSet:
    """Get ViewSet fixture."""
    return WordStudyViewSet()


@pytest.fixture
def mock_service() -> Mock:
    """Mock word study progress service fixture."""
    return Mock(spec=WordProgressServiceABC)


@pytest.fixture
def valid_payload() -> WordProgressType:
    """Mock valid request payload."""
    return cases.VALID_PAYLOAD


class TestWordStudyViewSet:
    """Test Word study progress HTTP ViewSet."""

    def test_progress_success(
        self,
        viewset: WordStudyViewSet,
        mock_request: Mock,
        mock_service: Mock,
        valid_payload: WordProgressType,
    ) -> None:
        """Test successful progress update."""
        mock_request.data = valid_payload

        with container.lang.progress_service.override(mock_service):
            response = viewset.progress(mock_request)  # type: ignore

        assert response.status_code == HTTPStatus.NO_CONTENT
        mock_service.update_progress.assert_called_once_with(**valid_payload)

    @pytest.mark.parametrize(
        'invalid_payload, expected_errors',
        cases.INVALID_PAYLOAD,
    )
    def test_progress_validation_errors_handling(
        self,
        viewset: WordStudyViewSet,
        mock_request: Mock,
        mock_service: Mock,
        invalid_payload: cases.InvalidPayload,
        expected_errors: cases.SerializerErrors,
    ) -> None:
        """Test validation errors handling."""
        mock_request.data = invalid_payload

        response = viewset.progress(mock_request)  # type: ignore

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.data == expected_errors

        mock_service.update_progress.assert_not_called()

    @pytest.mark.parametrize(
        'exception, expected_detail',
        cases.SERVICE_ERROR,
    )
    def test_service_errors_handling(
        self,
        viewset: WordStudyViewSet,
        mock_request: Mock,
        mock_service: Mock,
        valid_payload: WordProgressType,
        exception: cases.ServiceErrors,
        expected_detail: str,
    ) -> None:
        """Test service exception handling."""
        mock_request.data = valid_payload
        mock_service.update_progress.side_effect = exception

        with container.lang.progress_service.override(mock_service):
            response = viewset.progress(mock_request)  # type: ignore

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.data == {'detail': expected_detail}
