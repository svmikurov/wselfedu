"""Language discipline repository fixtures."""

import pytest

from apps.lang import repos


@pytest.fixture
def presentation_repo() -> repos.Presentation:
    """Provide Word study Presentation repository."""
    return repos.Presentation()


@pytest.fixture
def progress_repo() -> repos.Progress:
    """Provide Word study Progress repository."""
    return repos.Progress()
