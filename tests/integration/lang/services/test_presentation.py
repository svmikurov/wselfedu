"""Word study presentation service tests."""

from unittest.mock import Mock

import pytest

from apps.core import exceptions
from apps.core import models as models_core
from apps.lang import models, repos, services, types
from apps.users.models import Person
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


class TestGetPresentationCase:
    """Get Word study presentation case tests."""

    @pytest.mark.django_db
    def test_no_case_exception_raise(
        self,
        user: Person,
        service: services.WordPresentationService,
        translations: list[models.EnglishTranslation],
        translations_meta: tuple[
            list[models.LangCategory],
            list[models_core.Source],
            list[models.LangMark],
        ],
        conditions: types.WordParameters,
    ) -> None:
        """Test that raises exception when no case for conditions."""
        categories, _, _ = translations_meta

        # Arrange
        category = categories[0]
        conditions['category'] = types.IdName(id=category.pk, name='')

        # Act & Assert
        with pytest.raises(exceptions.NoTranslationsAvailableException):
            service.get_presentation_case(user, conditions)
