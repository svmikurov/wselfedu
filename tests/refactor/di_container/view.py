"""View DI container tests."""

import pytest
from apps.lang.di.view.web.container import WebViewContainer

from apps.lang.di import LanguageContainer


@pytest.fixture
def view_deps_container() -> WebViewContainer:
    """Provide view ."""
    return LanguageContainer.view_container.exercise  # type: ignore[return-value]


class TestViewContainer:
    """View-injected exercise dependencies container tests."""

    def test_view_container_initialization(
        self, view_deps_container: WebViewContainer
    ) -> None:
        """View-injected exercise container initialization test."""
        assert view_deps_container
