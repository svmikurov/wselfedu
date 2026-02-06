"""Test translation repository."""

import pytest

from apps.lang import models
from apps.lang.repositories.exercise.translation.test import (
    TranslationExerciseRepository,
)
from apps.users.models import Person


@pytest.fixture
def repository() -> TranslationExerciseRepository:
    """Provide regular translation repository."""
    return TranslationExerciseRepository(
        manager=models.EnglishTranslation.objects
    )


@pytest.mark.django_db
class TestRegularTranslationRepository:
    """Test regular translation repository."""

    def test_get_translations(
        self,
        user: Person,
        translations: list[models.EnglishTranslation],
        repository: TranslationExerciseRepository,
    ) -> None:
        """Test repository."""
        assert repository.fetch(user, {})
