"""Word study presentation service test configuration."""

from unittest.mock import Mock

import pytest

from apps.lang import repositories, services, types
from tests.fixtures.lang.no_db import translations as fixtures


@pytest.fixture
def presentation_repo() -> repositories.EnglishPresentation:
    """Provide Word study Presentation repository."""
    return repositories.EnglishPresentation()


@pytest.fixture
def conditions() -> types.CaseParametersAPI:
    """Provide Word study lookup empty conditions."""
    return fixtures.EMPTY_TRANSLATION_PARAMETERS.copy()


@pytest.fixture
def service(
    presentation_repo: repositories.EnglishPresentation,
) -> services.WordPresentationService:
    """Provide Word study presentation service."""
    return services.WordPresentationService(
        word_repo=presentation_repo,
        case_storage=Mock(),
        domain=Mock(),
    )
