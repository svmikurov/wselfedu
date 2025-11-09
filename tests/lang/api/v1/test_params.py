"""Test the Word study params endpoint."""

from http import HTTPStatus
from unittest.mock import Mock

import pytest
from rest_framework.test import APIClient

from apps.lang.presenters.abc import (
    WordStudyParamsPresenterABC,
)
from apps.lang.types import WordParamsType
from apps.users.models import CustomUser
from di import container


@pytest.fixture
def initial_payload() -> WordParamsType:
    """Get Word study initial params."""
    return {
        'categories': [],
        'labels': [
            {'id': 2, 'name': 'label name'},
        ],
        'default_params': None,
    }


@pytest.mark.django_db
class TestWordStudyParams:
    """Test Word study params REST API endpoint."""

    @pytest.fixture
    def url(self) -> str:
        """Word study params url path."""
        return '/api/v1/lang/study/params/'

    @pytest.fixture
    def presenter_mock(
        self,
        initial_payload: WordParamsType,
    ) -> Mock:
        """Mock initial Word study params."""
        mock = Mock(spec=WordStudyParamsPresenterABC)
        mock.get_initial.return_value = initial_payload
        return mock

    def test_params_success(
        self,
        url: str,
        client: APIClient,
        user: CustomUser,
        initial_payload: WordParamsType,
        presenter_mock: Mock,
    ) -> None:
        """Test params success."""
        client.force_authenticate(user)

        # Mock presenter
        with container.lang.params_presenter.override(presenter_mock):
            response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.data == initial_payload
