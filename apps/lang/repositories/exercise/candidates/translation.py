"""Translation exercise candidates repository."""

from django.db.models import F, Manager

from apps.core.domains.null import NullDTO
from apps.core.repositories.abstract import AbstractRepository
from apps.lang.models import EnglishTranslation
from apps.users.models import Person


class TranslationCandidatesRepository(
    AbstractRepository[NullDTO, object],
):
    """Translation exercise candidates repository."""

    def __init__(
        self,
        manager: Manager[EnglishTranslation],
    ) -> None:
        """Construct the repository."""
        self._manager = manager

    def fetch(self, user: Person, filter: NullDTO) -> object:
        """Fetch translations for exercise."""
        return (
            self._manager.filter(
                user=user,
            )
            .select_related('native', 'foreign')
            .annotate(
                define=F('native__word'),
                explain=F('foreign__word'),
            )
        )
