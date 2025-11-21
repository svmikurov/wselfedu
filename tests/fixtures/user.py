"""Users application fixtures."""

from unittest.mock import Mock

import pytest
from django.contrib.auth.models import AnonymousUser

from apps.users.models import CustomUser

# Database fixtures
# -----------------


@pytest.fixture
def user() -> CustomUser:
    """Provide user."""
    return CustomUser.objects.create_user(
        username='test_user',
        password='test_pass',
    )


@pytest.fixture
def user_not_owner() -> CustomUser:
    """Provide user that is not the owner."""
    return CustomUser.objects.create_user(
        username='other_test_user',
        password='other_test_pass',
    )


@pytest.fixture
def owner() -> CustomUser:
    """Provide owner of object."""
    return CustomUser.objects.create_user(
        username='owner_user',
        password='owner_pass',
    )


# Mock user fixtures
# ------------------


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
