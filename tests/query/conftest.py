"""Defines configuration for tests."""

import pytest

from apps.users.models import Balance, CustomUser


@pytest.fixture
def user() -> CustomUser:
    """Fixture providing user."""
    return CustomUser.objects.create(username='user')


@pytest.fixture
def balance(user: CustomUser) -> Balance:
    """Fixture providing balance."""
    return Balance.objects.create(user=user)
