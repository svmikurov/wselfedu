"""Exercise candidates repository."""

from typing import TypeVar

from django.db.models import F, Manager

from apps.core.repositories.abstract import AbstractUserFetchRepository
from apps.lang.models import EnglishTranslation
from apps.users.models import Person
from contracts import NullProtocol
from interfaces.schemas.domain.exercise import TaskItem

FilterT = TypeVar('FilterT')
ResultT = list[TaskItem]


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
        queryset = (
            self._manager.filter(
                user=user,
            )
            .select_related('native', 'foreign')
            .annotate(
                define=F('native__word'),
                mean=F('foreign__word'),
                progress_value=F('progress'),
            )
        ).order_by('id')

        candidates = [
            TaskItem.model_validate(candidate) for candidate in queryset
        ]

        return candidates
