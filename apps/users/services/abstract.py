"""Abstract base services."""

from abc import ABC, abstractmethod
from typing import override

from apps.users.domains.dto import RewardDTO

from .protocol import RewardServiceProtocol

__all__ = ('AbstractRewardService',)


class AbstractRewardService(ABC, RewardServiceProtocol):
    """ABC for reward service."""

    @override
    @abstractmethod
    def increment(self, reward: RewardDTO) -> None:
        """Add reward."""
