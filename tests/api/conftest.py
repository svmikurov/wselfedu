"""REST API test configuration."""

import pytest
from rest_framework.test import APIClient, APIRequestFactory


@pytest.fixture
def factory() -> APIRequestFactory:
    """Get API request factory."""
    return APIRequestFactory()


@pytest.fixture
def client() -> APIClient:
    """Get API client."""
    return APIClient()
