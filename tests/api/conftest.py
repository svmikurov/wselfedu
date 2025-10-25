"""REST API test configuration."""

import pytest
from rest_framework.test import APIRequestFactory


@pytest.fixture
def factory() -> APIRequestFactory:
    """Get API request."""
    return APIRequestFactory()
