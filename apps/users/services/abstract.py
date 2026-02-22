"""Abstract base services."""

from abc import ABC, abstractmethod
from typing import override

from .protocol import RewardServiceProtocol

__all__ = ('AbstractRewardService',)


class AbstractRewardService(ABC, RewardServiceProtocol):
    """ABC for reward service."""

    @override
    @abstractmethod
    def increment(self, resource_pk: int, mentorship_pk: int) -> None:
        """Add reward."""

    @override
    @abstractmethod
    def decrement(self, resource_pk: int, mentorship_pk: int) -> None:
        """Remove reward."""
