"""Test Word study Progress parameters API tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Sequence

import pytest
from rest_framework.exceptions import ErrorDetail

from apps.core import models as core_models
from apps.lang import models, repos, types

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

# Data fixtures
# ~~~~~~~~~~~~~


@pytest.fixture
def public_parameters(
    parameters_db_data: types.WordPresentationParamsT,
) -> types.WordPresentationParamsT:
    """Provide public Parameters data.

    Contains fields for a user who has no saved settings
    or the field is not set in the user settings.
    """
    return {
        # Parameter options
        'categories': [],
        'marks': [],
        'sources': [],
        'periods': parameters_db_data['periods'],
        'orders': [
            {'value': 'to_native', 'label': 'На родной'},
            {'value': 'from_native', 'label': 'С родного'},
            {'value': 'random', 'label': 'Случайные'},
        ],
        # Selected parameter
        'category': None,
        'mark': None,
        'word_source': None,
        'order': None,
        'start_period': None,
        'end_period': None,
        # Set parameter
        'word_count': None,
        'question_timeout': None,
        'answer_timeout': None,
    }


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
    marks = models.LangMark.objects.bulk_create(
        [
            models.LangMark(user=user, name='mark 1'),
            models.LangMark(user=user, name='mark 2'),
        ],
        batch_size=None,
    )
    sources = core_models.Source.objects.bulk_create(
        [
            core_models.Source(user=user, name='source 1'),
            core_models.Source(user=user, name='source 2'),
        ],
        batch_size=None,
    )
    periods = core_models.Period.objects.bulk_create(
        [
            core_models.Period(name='start'),
            core_models.Period(name='end'),
        ]
    )

    parameters = models.Params.objects.create(
        user=user,
        # Initial choices
        category=categories[0],
        mark=marks[1],
        word_source=sources[0],
        word_count=80,
        start_period=periods[0],
        end_period=periods[1],
        question_timeout=2.9,
        answer_timeout=3.1,
    )
    return {
        'categories': _build_choices(categories),
        'marks': _build_choices(marks),
        'sources': _build_choices(sources),
        'periods': _build_choices(periods),
        'category': {'id': categories[0].pk, 'name': categories[0].name},
        'mark': {'id': marks[1].pk, 'name': marks[1].name},
        'word_source': {'id': sources[0].pk, 'name': sources[0].name},
        'order': parameters.order,  # type: ignore[typeddict-item]
        'start_period': {'id': periods[0].pk, 'name': periods[0].name},
        'end_period': {'id': periods[1].pk, 'name': periods[1].name},
        'word_count': parameters.word_count,
        'question_timeout': parameters.question_timeout,
        'answer_timeout': parameters.answer_timeout,
    }


def _build_choices(data: Sequence[types.HasIdName]) -> list[types.IdName]:
    """Build list of id-name dictionaries from model objects."""
    return [{'id': d.id, 'name': d.name} for d in data]


# Tests
# ~~~~~


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
