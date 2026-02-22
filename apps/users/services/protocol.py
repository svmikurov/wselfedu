"""User application protocols."""

from typing import Protocol

__all__ = ('RewardServiceProtocol',)


class RewardServiceProtocol(Protocol):
    """Protocol for reward interface."""

    def increment(self, resource_pk: int, mentorship_pk: int) -> None:
        """Add reward."""

    def decrement(self, resource_pk: int, mentorship_pk: int) -> None:
        """Remove reward."""
