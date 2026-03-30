"""Database lockup condition factory."""

from typing import Protocol, TypedDict

from apps.users.models import Person


class LockupConditionsProtocol(Protocol):
    """Translation lockup conditions."""

    user: Person


class LockupConditionsFilter(TypedDict):
    """Translation lockup conditions."""

    user: Person


class UserTranslationLookupFactory:
    """User's translations lockup conditions factory."""

    def build(
        self,
        command: LockupConditionsProtocol,
    ) -> LockupConditionsFilter:
        """Build translation lockup conditions."""
        return {'user': command.user}
