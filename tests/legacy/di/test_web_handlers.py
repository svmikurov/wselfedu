"""Language app web handlers DI container test."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from di import MainContainer
    from di.lang.handler.web.container import WebHandlerContainer


@pytest.fixture
def handlers(main_container: MainContainer) -> WebHandlerContainer:
    """Provide lang app use cases DI container."""
    return main_container.lang.handlers  # type: ignore


class TestLanguageWebHandlersContainer:
    """Test lang app web handlers DI container."""

    def test_create_container(
        self,
        handlers: WebHandlerContainer,
    ) -> None:
        """Test that lang app DI container initialized success."""
        assert handlers is not None, (
            'Language app container was not initialized'
        )


class TestCreateWebHandlers:
    """Test create exercise use case."""

    def test_regular_translation_presentation_initialized(
        self,
        handlers: WebHandlerContainer,
    ) -> None:
        """Test that handler initialized."""
        assert handlers.regular_translation_presentation is not None, (
            'Process regular translation presentation '
            'handler was not initialized'
        )
