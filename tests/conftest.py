"""Test configuration."""

from unittest.mock import Mock

import pytest
from rest_framework.test import APIClient, APIRequestFactory

from di import MainContainer

pytest_plugins = [
    'tests.users.fixtures',
    'tests.lang.fixtures',
]


@pytest.fixture
def container() -> MainContainer:
    """Get main DI container."""
    return MainContainer()


@pytest.fixture
def factory() -> APIRequestFactory:
    """Get API request factory."""
    return APIRequestFactory()


@pytest.fixture
def client() -> APIClient:
    """Get API client."""
    return APIClient()


# Mocking
# -------


@pytest.fixture
def mock_request() -> Mock:
    """Mock request fixture."""
    return Mock()
