"""Test configuration."""

import pytest

from apps.users.models import CustomUser


@pytest.fixture
def user() -> CustomUser:
    """User fixture."""
    return CustomUser.objects.create_user(
        username='test_user',
        password='test_pass',
    )
