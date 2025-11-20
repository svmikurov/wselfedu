"""Test the Word study params endpoint."""

# ruff: noqa: I001, F811, F401

from http import HTTPStatus
from unittest.mock import Mock
from typing import Callable

import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.request import Request
from rest_framework.response import Response

import di
from apps.lang.repos.abc import WordStudyParamsRepositoryABC
from apps.lang import types

from tests.fixtures.lang.params_data import choices, initial, settings

from apps.lang.api.v1.views.study import WordStudyViewSet


@pytest.fixture
def payload(
    choices: types.ParamsChoicesT,
    initial: types.InitialChoicesT,
    settings: types.PresentationSettingsT,
) -> types.WordPresentationParamsT:
    """Provide Word study Presentation params payload."""
    return {**choices, **initial, **settings}


@pytest.fixture
def mock_repository(
    payload: types.WordPresentationParamsT,
) -> Mock:
    """Mock initial Word study params."""
    mock = Mock(spec=WordStudyParamsRepositoryABC)
    mock.fetch_initial.return_value = payload
    return mock


class TestWordStudyParams:
    """Test Word study params REST API endpoint."""

    @pytest.fixture
    def view(self) -> Callable[[Request], Response]:
        """Provide Word study ViewSet."""
        return WordStudyViewSet.as_view(actions={'get': 'params'})

    def test_params_success(
        self,
        api_request_factory: APIRequestFactory,
        view: Callable[[Request], Response],
        payload: types.WordPresentationParamsT,
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
        assert response.data == payload
