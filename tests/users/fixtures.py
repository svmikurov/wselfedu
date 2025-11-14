"""Users application fixtures."""

from unittest.mock import Mock

import pytest
from django.contrib.auth.models import AnonymousUser

from apps.users.models import CustomUser


@pytest.fixture
def user() -> CustomUser:
    """User fixture."""
    return CustomUser.objects.create_user(
        username='test_user',
        password='test_pass',
    )


@pytest.fixture
def owner() -> CustomUser:
    """Owner of object, the User fixture."""
    return CustomUser.objects.create_user(
        username='owner_user',
        password='owner_pass',
    )


@pytest.fixture
def anonymous_user() -> AnonymousUser:
    """Provide anonymous user."""
    return AnonymousUser()


@pytest.fixture
def mock_user() -> Mock:
    """Provide user mock."""
    return Mock(spec=CustomUser)


@pytest.fixture
def mock_auth_user(
    mock_user: Mock,
) -> Mock:
    """Provide authenticated user mock."""
    mock_user.is_authenticated = True
    return mock_user
