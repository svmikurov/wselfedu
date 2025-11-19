"""Test the Word study params endpoint."""

from http import HTTPStatus
from unittest.mock import Mock

import pytest
from rest_framework.test import APIClient

import di
from apps.lang.repos.abc import (
    WordStudyParamsRepositoryABC,
)
from apps.lang.types import ParamsChoicesT


@pytest.fixture
def initial_payload() -> ParamsChoicesT:
    """Get Word study initial params."""
    return {
        'categories': [],
        'labels': [{'id': 2, 'name': 'label name'}],
    }


# @pytest.mark.django_db
class TestWordStudyParams:
    """Test Word study params REST API endpoint."""

    @pytest.fixture
    def url(self) -> str:
        """Word study params url path."""
        return '/api/v1/lang/study/params/'

    @pytest.fixture
    def presenter_mock(
        self,
        initial_payload: ParamsChoicesT,
    ) -> Mock:
        """Mock initial Word study params."""
        mock = Mock(spec=WordStudyParamsRepositoryABC)
        mock.fetch_initial.return_value = initial_payload
        return mock

    def test_params_success(
        self,
        url: str,
        api_client: APIClient,
        initial_payload: ParamsChoicesT,
        presenter_mock: Mock,
    ) -> None:
        """Test params success."""
        api_client.force_authenticate(Mock())

        # Mock presenter
        with di.container.lang.params_repo.override(presenter_mock):
            response = api_client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.data == initial_payload
