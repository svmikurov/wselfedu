"""Language discipline repository fixtures."""

import pytest

from apps.lang import repos


@pytest.fixture
def progress_repo() -> repos.ProgressRepo:
    """Provide Word study Progress repository."""
    return repos.ProgressRepo()
