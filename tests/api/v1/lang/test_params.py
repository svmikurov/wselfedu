"""Test the Word study params endpoint."""

from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

from apps.lang.presenters.abc import WordStudyInitialParamsType
from apps.users.models import CustomUser


@pytest.fixture
def initial_payload() -> WordStudyInitialParamsType:
    """Get Word study initial params."""
    return {
        'marks': [
            {1: 'color'},
            {2: 'time'},
        ]
    }


@pytest.mark.django_db
class TestWordStudyParams:
    """Test Word study params REST API endpoint."""

    @pytest.fixture
    def url(self) -> str:
        """Word study params url path."""
        return '/api/v1/lang/study/params/'

    def test_params_success(
        self,
        url: str,
        client: APIClient,
        user: CustomUser,
        initial_payload: WordStudyInitialParamsType,
    ) -> None:
        """Test params success."""
        client.force_authenticate(user)
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.data == initial_payload
