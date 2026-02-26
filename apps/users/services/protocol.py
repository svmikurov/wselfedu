"""User application protocols."""

from typing import Protocol

from apps.users.domains.dto import RewardDTO

__all__ = ('RewardServiceProtocol',)


class RewardServiceProtocol(Protocol):
    """Protocol for reward interface."""

    def increment(self, reward: RewardDTO) -> None:
        """Add reward."""
