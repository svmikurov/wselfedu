"""Word study parameters API tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

import pytest
from rest_framework.exceptions import ErrorDetail

from apps.lang import repos, types

if TYPE_CHECKING:
    from rest_framework.test import APIClient

    from apps.users.models import CustomUser

GET_PARAMETERS_PATH = '/api/v1/lang/study/params/'
PUT_PARAMETERS_PATH = '/api/v1/lang/study/params/update/'

UNAUTHORIZED_RESPONSE_DATA = {
    'detail': ErrorDetail(
        string='Учетные данные не были предоставлены.',
        code='not_authenticated',
    )
}


@pytest.mark.django_db
class TestGetSuccess:
    """Get Word study Presentation parameters API success tests."""

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


class TestUpdate:
    """Update Word study Presentation parameters API success tests."""

    @pytest.mark.django_db
    def test_update_success(
        self,
        user: CustomUser,
        api_client: APIClient,
        parameters_db_data: types.WordPresentationParamsT,
    ) -> None:
        """Test that parameters updated."""
        # Arrange
        parameters = {
            key: parameters_db_data[key]  # type: ignore[literal-required]
            for key in parameters_db_data.keys()
            if key not in ('categories', 'marks', 'sources', 'periods')
        }
        to_update = {
            'word_count': 324,
            'question_timeout': 7,
        }
        payload: dict[str, Any] = {**parameters, **to_update}

        api_client.force_authenticate(user)

        # Act
        response = api_client.put(PUT_PARAMETERS_PATH, payload, format='json')

        # Assert
        assert response.status_code == HTTPStatus.OK

        updated_data = repos.WordStudyParamsRepository().fetch(user)
        assert to_update.items() <= updated_data.items()
        assert response.data == updated_data


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
    def test_public_parameters_data(
        self,
        api_client: APIClient,
        user_not_owner: CustomUser,
        parameters_db_data: types.WordPresentationParamsT,
        public_parameters: types.WordPresentationParamsT,
    ) -> None:
        """Test the public parameters."""
        # Arrange
        # Authentication with not parameters owner
        api_client.force_authenticate(user=user_not_owner)

        # Act
        response = api_client.get(GET_PARAMETERS_PATH)

        # Assert
        assert response.status_code == HTTPStatus.OK

        # - The user does not see the choices of others
        assert response.data != parameters_db_data

        # - The user see only public data
        assert response.data == public_parameters
