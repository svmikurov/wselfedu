"""Test the Word study ViewSet, `presentation` action."""

from http import HTTPStatus
from typing import Callable, TypedDict
from unittest.mock import Mock

import pytest
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.lang import types
from apps.lang.api.v1.views.study import WordStudyViewSet
from apps.lang.services.abc import WordPresentationServiceABC
from di import container
from tests.fixtures.lang.no_db import translations as fixtures


@pytest.fixture
def presentation_case() -> types.PresentationCaseT:
    """Provide Word study presentation case."""
    return fixtures.PRESENTATION_CASE


class PresentationResponse(TypedDict):
    """Word study Presentation response data typed dict."""

    case_uuid: str
    definition: str
    explanation: str
    info: types.InfoT


@pytest.fixture
def view() -> Callable[[Request], Response]:
    """Provide ViewSet."""
    return WordStudyViewSet.as_view({'post': 'presentation'})


@pytest.fixture
def valid_payload() -> types.CaseParameters:
    """Provide Request payload."""
    return fixtures.EMPTY_TRANSLATION_PARAMETERS.copy()


@pytest.fixture
def valid_response_data() -> PresentationResponse:
    """Provide Word study success Response data."""
    return {
        'case_uuid': '5b518a3e-45a4-4147-a097-0ed28211d8a4',
        'definition': 'house',
        'explanation': 'дом',
        'info': {'progress': 7},
    }


@pytest.fixture
def mock_service(
    presentation_case: types.PresentationT,
) -> Mock:
    """Mock Word study presentation service."""
    mock = Mock(spec=WordPresentationServiceABC)
    mock.get_case.return_value = presentation_case
    return mock


class TestPresentation:
    """Test WordStudyViewSet."""

    def test_success(
        self,
        mock_user: Mock,
        mock_service: Mock,
        api_request_factory: APIRequestFactory,
        view: Callable[[Request], Response],
        valid_response_data: PresentationResponse,
        valid_payload: types.CaseParameters,
    ) -> None:
        """Test successful presentation request."""
        # Arrange
        request = api_request_factory.post('', valid_payload, format='json')
        force_authenticate(request, mock_user)

        # Act
        with container.lang.word_presentation_service.override(mock_service):
            response = view(request)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response.data == valid_response_data
        mock_service.get_case.assert_called_once_with(
            mock_user,
            valid_payload,
        )
