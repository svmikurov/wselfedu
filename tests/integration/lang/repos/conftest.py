"""Language discipline repository fixtures."""

from unittest.mock import Mock

import pytest

from apps.lang import repos, types
from apps.lang.repos import abc as base


@pytest.fixture
def presentation_repo() -> repos.Presentation:
    """Provide Word study Presentation repository."""
    return repos.Presentation()


@pytest.fixture
def progress_repo() -> repos.Progress:
    """Provide Word study Progress repository."""
    return repos.Progress()


@pytest.fixture
def mock_presentation_repo(
    presentation: types.PresentationT,
) -> Mock:
    """Mock Word study Presentation repo."""
    mock = Mock(spec=base.PresentationABC)
    mock.get_presentation_case.return_value = presentation
    return mock
