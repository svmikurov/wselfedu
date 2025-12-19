"""Test configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
from rest_framework.test import APIClient, APIRequestFactory

from di import MainContainer

if TYPE_CHECKING:
    from django.test import Client

    from apps.users.models import Person


pytest_plugins = [
    'tests.fixtures.user',
    'tests.fixtures.lang.db.translation',
    'tests.fixtures.lang.db.translations',
    'tests.unit.lang.fixtures',
]


@pytest.fixture
def auth_client(user: Person, client: Client) -> Client:
    """Get main DI container."""
    client.force_login(user)
    return client


@pytest.fixture
def container() -> MainContainer:
    """Get main DI container."""
    return MainContainer()


@pytest.fixture
def api_request_factory() -> APIRequestFactory:
    """Get API request factory."""
    return APIRequestFactory()


@pytest.fixture
def api_client() -> APIClient:
    """Get API client."""
    return APIClient()


# Mocking
# -------


@pytest.fixture
def mock_request(
    mock_user: Mock,
) -> Mock:
    """Mock request fixture."""
    request = Mock()
    request.user = mock_user
    return request
