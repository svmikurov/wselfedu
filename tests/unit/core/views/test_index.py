"""Test Core app index ViewSet."""

from http import HTTPStatus
from unittest.mock import patch

import pytest
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory

from apps.core.api.v1.views import IndexViewSet
from apps.users.models import Person
from tests.fixtures import user


class TestIndexViewSet:
    """Tests for IndexViewSet."""

    @pytest.fixture
    def viewset(self) -> IndexViewSet:
        """Fixture providing ViewSet."""
        return IndexViewSet()

    @pytest.fixture
    def factory(self) -> APIRequestFactory:
        """Fixture providing test request."""
        return APIRequestFactory()

    @pytest.mark.parametrize(
        'user, balance',
        [
            (user.mock_auth_user, '5'),
            (user.anonymous_user, None),
        ],
    )
    def test_index_action(
        self,
        user: Person | AnonymousUser,
        balance: str | None,
        viewset: IndexViewSet,
        factory: APIRequestFactory,
    ) -> None:
        """Test index action with anonymous user."""
        request = factory.get('/')
        request.user = user

        with patch.object(IndexViewSet, '_get_index_data') as mock_method:
            mock_method.return_value = {
                'balance': balance,
            }

            # Calling the method under test
            response = viewset.index(request=request)  # type: ignore

            # Check that the mock was called with the correct argument
            mock_method.assert_called_once_with(user)

            assert response.status_code == HTTPStatus.OK
            assert response.data == {
                'status': 'success',
                'data': {'balance': balance},
            }
