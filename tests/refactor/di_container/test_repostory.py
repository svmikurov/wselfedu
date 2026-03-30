"""DI container tests."""

import pytest

from apps.core import models as models_core
from apps.lang import models
from apps.lang.di.container import LanguageContainer
from apps.lang.repositories import (
    RegularParametersRepository,
    TranslationConditionsRepository,
)
from apps.lang.schemas import LookupConditionsDTO
from apps.lang.types import CaseSettingsAPI
from apps.users.models import Person

REPOSITORIES = LanguageContainer.repositories


@pytest.fixture
def container() -> LanguageContainer:
    """Provide language container."""
    return LanguageContainer()


@pytest.fixture
def condition_repository() -> RegularParametersRepository:
    """Provide exercise condition repository."""
    return (  # type: ignore[no-any-return]
        REPOSITORIES.regular_parameters()
    )


@pytest.fixture
def candidates_repository() -> TranslationConditionsRepository:
    """Provide translation candidates repository."""
    return (  # type: ignore[no-any-return]
        REPOSITORIES.regular_translation_condition()
    )


class TestContainer:
    """Test language app DI container."""

    def test_create_container(self, container: LanguageContainer) -> None:
        """Create container success."""
        assert container is not None


class TestConditionRepository:
    """Test exercise conditions repository."""

    @pytest.mark.django_db
    def test_condition_repository(
        self,
        user: Person,
        condition_repository: RegularParametersRepository,
        parameters_db_data: CaseSettingsAPI,
    ) -> None:
        """Test 'fetch' method of condition repository."""
        # Act & Assert
        assert condition_repository.fetch(user)


# TODO: Add missing tests for each lookup condition
class TestTranslationsRegularRepository:
    """Test translations regular repository."""

    @pytest.mark.django_db
    def test_fetch_translations_success_without_conditions(
        self,
        user: Person,
        candidates_repository: TranslationConditionsRepository,
        translations: list[models.EnglishTranslation],
    ) -> None:
        """Fetch translations success without lookup conditions."""
        # Act & Assert
        assert candidates_repository.fetch(user, conditions=None)

    @pytest.mark.django_db
    def test_fetch_translations_empty(
        self,
        user: Person,
        candidates_repository: TranslationConditionsRepository,
        translations: list[models.EnglishTranslation],
        translations_meta: tuple[
            list[models.Category],
            list[models_core.Source],
            list[models.Mark],
            list[models_core.Period],
        ],
    ) -> None:
        """No translations with lookup conditions."""
        # Arrange
        category = translations_meta[0][0]
        parameters = LookupConditionsDTO(category=category.pk)

        # Act & Assert
        assert not candidates_repository.fetch(user, conditions=parameters)

    @pytest.mark.django_db
    def test_fetch_translations_success_by_category(
        self,
        user: Person,
        candidates_repository: TranslationConditionsRepository,
        translations: list[models.EnglishTranslation],
        translations_meta: tuple[
            list[models.Category],
            list[models_core.Source],
            list[models.Mark],
            list[models_core.Period],
        ],
    ) -> None:
        """Fetch translations success by category lookup condition."""
        # Arrange
        # - Set up lookup conditions
        category = translations_meta[0][0]
        parameters = LookupConditionsDTO(category=category.pk)

        # - Set translation with condition
        translation = translations[0]
        translation.category = category
        translation.save()

        # Act
        candidates = candidates_repository.fetch(user, conditions=parameters)

        # Assert
        assert translation in candidates
