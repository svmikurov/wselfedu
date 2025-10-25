"""Language discipline app REST API tests."""

from typing import Callable
from unittest.mock import Mock

from http import HTTPStatus

import pytest
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.lang import types
from apps.lang.api.v1.views.study import WordStudyViewSet
from apps.lang.presenters.abc import WordStudyPresenterABC
from apps.users.models import CustomUser
from di import container

# Test data
# ---------


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


# Test cases
# ----------


@pytest.mark.django_db
class TestWordStudyViewSet:
    """Test WordStudyViewSet presentation endpoint."""

    @pytest.fixture
    def url(self) -> str:
        """Url path fixture."""
        return '/api/v1/lang/study/presentation/'

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

        print(f'\n{response.data = }')
