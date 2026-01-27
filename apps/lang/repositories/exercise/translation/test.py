"""Translation repository."""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.lang import models

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.users.models import Person

__all__ = [
    'ExerciseTranslationRepository',
    'UserTranslationRepository',
]


class ExerciseTranslationRepository:
    """Exercise translation repository."""

    def fetch(self, exercise_id: int) -> QuerySet[models.EnglishTranslation]:
        """Fetch exercise translations."""
        res = (
            models.EnglishTranslation.objects.filter(
                exercises__exercise_id=exercise_id,
            )
            .prefetch_related('exercises__exercise')
            .select_related('native', 'foreign')
        )
        print(f'{res = }')
        return res


class UserTranslationRepository:
    """User translation repository."""

    def fetch(self, user: Person) -> QuerySet[models.EnglishTranslation]:
        """Fetch user's translations."""
        return models.EnglishTranslation.objects.filter(
            user=user
        ).select_related('native', 'foreign')
