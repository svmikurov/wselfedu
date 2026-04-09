"""DI container tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from di import MainContainer


class TestMainContainer:
    """Main container test."""

    def test_initialize_main_container(
        self,
        main_container: MainContainer,
    ) -> None:
        """Test that main container initialized success."""
        assert main_container is not None, 'Main container was not initialized'
