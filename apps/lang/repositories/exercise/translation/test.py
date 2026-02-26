"""Translation repository."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import F, Manager

from apps.core.repositories.abstract import AbstractDetailExerciseRepository
from apps.lang import models

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.core.domains.exercise.types import Conditions
    from apps.users.models import Person

__all__ = [
    'DetailTranslationRepository',
    'UserTranslationRepository',
]


class DetailTranslationRepository(AbstractDetailExerciseRepository):
    """Exercise translation repository."""

    def __init__(
        self,
        manager: Manager[models.EnglishTranslation],
    ) -> None:
        """Construct the repository."""
        self._manger = manager

    # TODO: Fix type ignore
    def fetch(  # type: ignore[override]
        self, user: Person, exercise_pk: int
    ) -> QuerySet[models.EnglishTranslation]:
        """Fetch exercise translations."""
        queryset = (
            self._manger.filter(
                exercises__exercise_id=exercise_pk,
            )
            .prefetch_related('exercises__exercise')
            .select_related('native', 'foreign')
            .annotate(
                define=F('native__word'),
                explain=F('foreign__word'),
            )
        )
        return queryset


class UserTranslationRepository:
    """User translation repository."""

    def fetch(self, user: Person) -> QuerySet[models.EnglishTranslation]:
        """Fetch user's translations."""
        return models.EnglishTranslation.objects.filter(
            user=user
        ).select_related('native', 'foreign')


class TranslationExerciseRepository:
    """Exercise translation repository."""

    def __init__(
        self,
        manager: Manager[models.EnglishTranslation],
    ) -> None:
        """Construct the repository."""
        self._manger = manager

    # HACK: Implement conditions
    def fetch(
        self, user: Person, conditions: Conditions
    ) -> QuerySet[models.EnglishTranslation]:
        """Fetch exercise translations."""
        queryset = (
            self._manger.filter(user=user)
            .select_related('native', 'foreign')
            .annotate(
                define=F('native__word'),
                explain=F('foreign__word'),
            )
        )
        return queryset
