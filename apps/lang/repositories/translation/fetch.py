"""Translation list repository."""

from typing import Any, TypeAlias

from django.db.models import Manager, QuerySet

from apps.core.repositories.abstract import AbstractUserFetchRepository
from apps.lang.models import EnglishTranslation

__all__ = ('TranslationListRepository',)

FilterType: TypeAlias = dict[str, Any]
EnglishQuerySet: TypeAlias = QuerySet[EnglishTranslation]


class TranslationListRepository(
    AbstractUserFetchRepository[FilterType, EnglishQuerySet],
):
    """Translation list repository."""

    def __init__(
        self,
        manager: Manager[EnglishTranslation],
    ) -> None:
        """Construct the repository."""
        self._manager = manager

    def fetch(self, filter: FilterType) -> EnglishQuerySet:  # type: ignore
        """Fetch translations."""
        return self._manager.filter(**filter)
