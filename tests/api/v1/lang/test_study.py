"""Test Word study presentation endpoint.

Test via APIClient, APIRequestFactory.
"""

from http import HTTPStatus
from typing import Callable
from unittest.mock import Mock

import pytest
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import (
    APIClient,
    APIRequestFactory,
    force_authenticate,
)

from apps.core.api.renderers import WrappedJSONRenderer
from apps.lang import types
from apps.lang.api.v1.views.study import WordStudyViewSet
from apps.lang.presenters.abc import WordStudyPresenterABC
from apps.users.models import CustomUser
from di import container


@pytest.fixture
def url() -> str:
    """Url path fixture."""
    return '/api/v1/lang/study/presentation/'


@pytest.fixture
def payload() -> dict[str, str]:
    """Request payload fixture."""
    return {}


@pytest.fixture
def case() -> types.WordType:
    """Word study case fixture."""
    return {
        'definition': 'Test definition',
        'explanation': 'Test explanation',
    }


@pytest.mark.django_db
class TestWordStudyViewSet:
    """Test WordStudyViewSet."""

    @pytest.fixture
    def view(self) -> Callable[[Request], Response]:
        """View fixture."""
        return WordStudyViewSet.as_view({'post': 'presentation'})

    @pytest.fixture
    def presenter_mock(self, case: types.WordType) -> Mock:
        """Mock presenter fixture."""
        mock = Mock(spec=WordStudyPresenterABC)
        mock.get_presentation.return_value = case
        return mock

    def test_presentation_success(
        self,
        url: str,
        payload: dict[str, str],
        factory: APIRequestFactory,
        user: CustomUser,
        view: Callable[[Request], Response],
        presenter_mock: Mock,
        case: types.WordType,
    ) -> None:
        """Test successful presentation request."""
        request = factory.post(url, payload, format='json')
        force_authenticate(request, user=user)

        with container.lang.word_study_presenter.override(presenter_mock):
            response = view(request)

        assert response.status_code == HTTPStatus.OK
        assert response.data == case
        presenter_mock.get_presentation.assert_called_once()


@pytest.mark.django_db
class TestWordStudy:
    """Test Word study presentation endpoint."""

    @pytest.fixture
    def presenter_mock(self, case: types.WordType) -> Mock:
        """Mock presenter fixture."""
        mock = Mock(spec=WordStudyPresenterABC)
        mock.get_presentation.return_value = case
        return mock

    def test_presentation_success(
        self,
        url: str,
        payload: dict[str, str],
        client: APIClient,
        user: CustomUser,
        presenter_mock: Mock,
        case: types.WordType,
    ) -> None:
        """Test successful presentation request."""
        client.force_authenticate(user)
        client.credentials(HTTP_ACCEPT='application/json')

        with container.lang.word_study_presenter.override(presenter_mock):
            response = client.post(url, payload, format='json')

        assert isinstance(response.accepted_renderer, WrappedJSONRenderer)

        assert response.status_code == HTTPStatus.OK
        assert response.data == case
        presenter_mock.get_presentation.assert_called_once()
