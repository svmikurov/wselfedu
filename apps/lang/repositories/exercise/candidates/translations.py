"""Exercise candidates repository."""

from typing import TypeVar

from django.db.models import F, Manager, QuerySet

from apps.core.domains.protocol import NullProtocol
from apps.core.repositories.abstract import AbstractUserFetchRepository
from apps.lang.models import EnglishTranslation
from apps.users.models import Person

FilterT = TypeVar('FilterT')
ResultT = QuerySet[EnglishTranslation]


class UserTranslationsRepository(
    AbstractUserFetchRepository[
        NullProtocol,
        ResultT,
    ],
):
    """User's translations repository."""

    def __init__(
        self,
        manager: Manager[EnglishTranslation],
    ) -> None:
        """Construct the repository."""
        self._manager = manager

    def fetch(
        self,
        user: Person,
        filter: NullProtocol,
    ) -> ResultT:
        """Fetch translations."""
        return (
            self._manager.filter(
                user=user,
            )
            .select_related('native', 'foreign')
            .annotate(
                define=F('native__word'),
                mean=F('foreign__word'),
            )
        )
