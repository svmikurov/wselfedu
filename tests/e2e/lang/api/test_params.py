"""Test Word study Progress parameters API tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Sequence

import pytest
from rest_framework.exceptions import ErrorDetail

from apps.lang import models

if TYPE_CHECKING:
    from rest_framework.test import APIClient

    from apps.lang import types
    from apps.users.models import CustomUser

GET_PARAMETERS_PATH = '/api/v1/lang/study/params/'
UNAUTHORIZED_RESPONSE_DATA = {
    'detail': ErrorDetail(
        string='Учетные данные не были предоставлены.',
        code='not_authenticated',
    )
}

# Data fixtures
# ~~~~~~~~~~~~~

EMPTY_PARAMETERS_PAYLOAD: types.WordPresentationParamsT = {
    'categories': [],
    'labels': [],
    'category': None,
    'label': None,
    'word_source': None,
    'order': None,
    'start_period': None,
    'end_period': None,
    'word_count': None,
    'question_timeout': None,
    'answer_timeout': None,
}


@pytest.fixture
def parameters_empty_data() -> types.WordPresentationParamsT:
    """Provide Word study Presenter empty data parameters."""
    return EMPTY_PARAMETERS_PAYLOAD.copy()


@pytest.fixture
def parameters_db_data(
    user: CustomUser,
) -> types.WordPresentationParamsT:
    """Provide Word study Presenter DB data parameters."""
    categories = models.LangCategory.objects.bulk_create(
        [
            models.LangCategory(user=user, name='cat 1'),
            models.LangCategory(user=user, name='cat 2'),
        ],
        batch_size=None,
    )
    labels = models.LangLabel.objects.bulk_create(
        [
            models.LangLabel(user=user, name='label 1'),
            models.LangLabel(user=user, name='label 2'),
        ],
        batch_size=None,
    )
    return {
        **EMPTY_PARAMETERS_PAYLOAD,
        'categories': _build_choices(categories),
        'labels': _build_choices(labels),
    }


def _build_choices(data: Sequence[types.HasIdName]) -> list[types.IdName]:
    """Build list of id-name dictionaries from model objects."""
    return [{'id': d.id, 'name': d.name} for d in data]


# Tests
# ~~~~~


@pytest.mark.django_db
class TestGetSuccess:
    """Get Word study Progress parameters API success tests."""

    def test_get_data_empty_case(
        self,
        user: CustomUser,
        api_client: APIClient,
        parameters_empty_data: types.WordPresentationParamsT,
    ) -> None:
        """Fetch Word study Presentation parameters empty data."""
        # Arrange
        api_client.force_authenticate(user=user)

        # Act
        response = api_client.get(GET_PARAMETERS_PATH)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response.data == parameters_empty_data

    def test_get_data(
        self,
        user: CustomUser,
        api_client: APIClient,
        parameters_db_data: types.WordPresentationParamsT,
    ) -> None:
        """Fetch Word study Presentation parameters empty data."""
        # Arrange
        api_client.force_authenticate(user=user)

        # Act
        response = api_client.get(GET_PARAMETERS_PATH)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response.data == parameters_db_data


class TestPermissions:
    """Get Word study Progress parameters API permissions tests."""

    def test_anonymous(
        self,
        api_client: APIClient,
    ) -> None:
        """Test get parameters for anonymous."""
        # Act
        response = api_client.get(GET_PARAMETERS_PATH)

        # Assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.data == UNAUTHORIZED_RESPONSE_DATA

    @pytest.mark.django_db
    def test_ownership(
        self,
        api_client: APIClient,
        user_not_owner: CustomUser,
        parameters_empty_data: types.WordPresentationParamsT,
        parameters_db_data: types.WordPresentationParamsT,
    ) -> None:
        """Test get parameters for anonymous."""
        # Arrange
        api_client.force_authenticate(user=user_not_owner)

        # Act
        response = api_client.get(GET_PARAMETERS_PATH)

        # Assert
        assert response.status_code == HTTPStatus.OK
        # The user does not see the choices of others
        assert response.data != parameters_db_data
        assert response.data == parameters_empty_data
