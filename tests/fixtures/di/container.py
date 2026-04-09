"""DI container fixtures."""

import pytest

from di import MainContainer, container


@pytest.fixture
def main_container() -> MainContainer:
    """Provide DI main container fixture."""
    return container
