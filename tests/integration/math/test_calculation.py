"""Math discipline app REST API tests."""

from typing import Any, Callable
from unittest.mock import Mock, patch

import pytest
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.math.api.v1.views.calculation import CalculationViewSet
from apps.math.presenters.calculation import CalculationPresenter
from apps.users.models import CustomUser

# Test data
# ---------


@pytest.fixture
def payload() -> dict[str, Any]:
    """Request payload fixture."""
    return {
        'exercise_name': 'subtraction',
        'config': {'min_value': 1, 'max_value': 9},
    }


@pytest.fixture
def case() -> dict[str, Any]:
    """Get calculation case, fixture."""
    return {
        'uid': '1868ebac-8ea7-4ed5-a407-64c9751b4b46',
        'question': '9 - 4',
    }


# Test cases
# ----------


@pytest.mark.django_db
class TestCalculationViewSet:
    """Test Calculation endpoint."""

    @pytest.fixture
    def url(self) -> str:
        """Url path fixture."""
        return '/api/v1/math/exercise/calculation/'

    @pytest.fixture
    def view(self) -> Callable[[Request], Response]:
        """View fixture."""
        return CalculationViewSet.as_view({'post': 'calculation'})

    @pytest.fixture
    def presenter_mock(self, case: dict[str, Any]) -> Mock:
        """Mock presenter fixture."""
        mock = Mock(spec=CalculationPresenter)
        mock.get_task.return_value = case
        return mock

    def test_presentation_success(
        self,
        url: str,
        payload: dict[str, str],
        api_request_factory: APIRequestFactory,
        user: CustomUser,
        view: Callable[[Request], Response],
        presenter_mock: Mock,
        case: dict[str, Any],
    ) -> None:
        """Test successful presentation request."""
        request = api_request_factory.post(url, payload, format='json')
        force_authenticate(request, user=user)

        with patch.object(
            CalculationViewSet, 'exercise_presenter', presenter_mock
        ):
            view(request)

        presenter_mock.get_task.assert_called_once_with(payload)
