"""Test Core app index ViewSet."""

from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory

from apps.core.api.v1.views import IndexViewSet
from apps.users.models import CustomUser


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

    @pytest.fixture
    def authenticated_user(self) -> Mock:
        """Fixture providing test user mocking."""
        user = Mock(spec=CustomUser)
        user.is_authenticated = True
        return user

    @pytest.fixture
    def anonymous_user(self) -> AnonymousUser:
        """Fixture providing anonymous user."""
        return AnonymousUser()

    @pytest.mark.parametrize(
        'user, balance',
        [
            (authenticated_user, '5'),
            (anonymous_user, None),
        ],
    )
    def test_index_action(
        self,
        user: CustomUser | AnonymousUser,
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
