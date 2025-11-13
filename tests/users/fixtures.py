"""Users application fixtures."""

from unittest.mock import Mock

import pytest

from apps.users.models import CustomUser


@pytest.fixture
def user() -> CustomUser:
    """User fixture."""
    return CustomUser.objects.create_user(
        username='test_user',
        password='test_pass',
    )


@pytest.fixture
def mock_user() -> Mock:
    """Mock user fixture."""
    return Mock(spec=CustomUser)


@pytest.fixture
def owner() -> CustomUser:
    """Owner of object, the User fixture."""
    return CustomUser.objects.create_user(
        username='owner_user',
        password='owner_pass',
    )
