"""Users application fixtures."""

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
def owner() -> CustomUser:
    """Owner of object, the User fixture."""
    return CustomUser.objects.create_user(
        username='owner_user',
        password='owner_pass',
    )
