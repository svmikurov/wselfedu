"""Language discipline repository fixtures."""

import pytest

from apps.lang import repos


@pytest.fixture
def presentation_repo() -> repos.EnglishPresentation:
    """Provide Word study Presentation repository."""
    return repos.EnglishPresentation()


@pytest.fixture
def progress_repo() -> repos.Progress:
    """Provide Word study Progress repository."""
    return repos.Progress()
