"""Pytest configuration."""

from __future__ import annotations

import pytest

from wse.di.application import ApplicationContainer

pytest_plugins = ('tests.fixtures.model',)


###################################################
# DI Container fixture
###################################################


@pytest.fixture
def container() -> ApplicationContainer:
    """Provide a application DI container."""
    return ApplicationContainer()
