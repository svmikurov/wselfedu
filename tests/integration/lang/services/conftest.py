"""Word study presentation service test configuration."""

from unittest.mock import Mock

import pytest

from apps.lang import repos, services, types
from tests.fixtures.lang.no_db import translation_query as fixtures


@pytest.fixture
def presentation_repo() -> repos.EnglishPresentation:
    """Provide Word study Presentation repository."""
    return repos.EnglishPresentation()


@pytest.fixture
def conditions() -> types.WordParameters:
    """Provide Word study lookup empty conditions."""
    return fixtures.EMPTY_LOOKUP_CONDITIONS.copy()


@pytest.fixture
def service(
    presentation_repo: repos.EnglishPresentation,
) -> services.WordPresentationService:
    """Provide Word study presentation service."""
    return services.WordPresentationService(
        word_repo=presentation_repo,
        case_storage=Mock(),
        domain=Mock(),
    )
