"""Translation repository."""

from django.db.models import F, Manager, QuerySet

from apps.core.assemblers.command import UserCommand, UserDetailCommand
from apps.core.repositories.abstract import AbstractUserFetchRepository
from apps.lang.models import EnglishTranslation

__all__ = (
    'DetailTranslationRepository',
    'UserTranslationRepository',
    'TranslationExerciseRepository',
)


class DetailTranslationRepository(
    AbstractUserFetchRepository[
        UserDetailCommand,
        QuerySet[EnglishTranslation],
    ],
):
    """Exercise translation repository."""

    def __init__(self, manager: Manager[EnglishTranslation]) -> None:
        """Construct the repository."""
        self._manger = manager

    def fetch(  # type: ignore
        self, command: UserDetailCommand
    ) -> QuerySet[EnglishTranslation]:
        """Fetch exercise translations."""
        queryset = (
            self._manger.filter(
                exercises__exercise_id=command.pk,
            )
            .prefetch_related('exercises__exercise')
            .select_related('native', 'foreign')
            .annotate(
                define=F('native__word'),
                explain=F('foreign__word'),
            )
        )
        return queryset


class UserTranslationRepository(
    AbstractUserFetchRepository[UserCommand, QuerySet[EnglishTranslation]]
):
    """User translation repository."""

    def fetch(self, command: UserCommand) -> QuerySet[EnglishTranslation]:  # type: ignore
        """Fetch user's translations."""
        return EnglishTranslation.objects.filter(
            user=command.user
        ).select_related('native', 'foreign')


class TranslationExerciseRepository(
    AbstractUserFetchRepository[UserCommand, QuerySet[EnglishTranslation]]
):
    """Exercise translation repository."""

    def __init__(self, manager: Manager[EnglishTranslation]) -> None:
        """Construct the repository."""
        self._manger = manager

    def fetch(self, command: UserCommand) -> QuerySet[EnglishTranslation]:  # type: ignore
        """Fetch exercise translations."""
        queryset = (
            self._manger.filter(user=command.user)
            .select_related('native', 'foreign')
            .annotate(
                define=F('native__word'),
                explain=F('foreign__word'),
            )
        )
        return queryset
