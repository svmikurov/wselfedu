"""Language app DI container test."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from di import MainContainer


class TestLanguageAppContainer:
    """Test lang app DI containers."""

    def test_create_app_container(
        self,
        main_container: MainContainer,
    ) -> None:
        """Test that lang app DI container initialized success."""
        assert main_container.lang is not None, (
            'Language app container was not initialized'
        )
