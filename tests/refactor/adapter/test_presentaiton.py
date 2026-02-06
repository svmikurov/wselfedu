"""Tests for Presentation exercise adapters."""

import pytest

from apps.lang.adapters.response.exercise.presentation import (
    ApiPresentationAdapter,
    WebPresentationAdapter,
)

from .. import fixture


@pytest.fixture
def api_adapter() -> ApiPresentationAdapter:
    """Provide API adapter for Presentation exercise."""
    return ApiPresentationAdapter()


@pytest.fixture
def web_adapter() -> WebPresentationAdapter:
    """Provide WEB adapter for Presentation exercise."""
    return WebPresentationAdapter()


class TestApiPresentationAdapter:
    """Test suite for API adapter for Presentation exercise."""

    def test_success(self, api_adapter: ApiPresentationAdapter) -> None:
        """Successful adaptation of Presentation case to API DTO."""
        # Act & Assert
        assert (
            api_adapter.to_response(fixture.PRESENTATION_DOMAIN_DTO)
            == fixture.PRESENTATION_API_DTO
        )


class TestWebPresentationAdapter:
    """Test suite for WEB adapter for Presentation exercise."""

    def test_success(self, web_adapter: WebPresentationAdapter) -> None:
        """Successful adaptation of Presentation case to WEB DTO."""
        # Act & Assert
        assert (
            web_adapter.to_response(fixture.PRESENTATION_DOMAIN_DTO)
            == fixture.PRESENTATION_WEB_DTO
        )
