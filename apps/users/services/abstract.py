"""Abstract base services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

from .protocol import RewardServiceProtocol

if TYPE_CHECKING:
    from apps.math.domains.dto import ExerciseRewardDTO
    from apps.users.models.user import Person

__all__ = ('AbstractRewardService',)


class AbstractRewardService(ABC, RewardServiceProtocol):
    """ABC for reward service."""

    @override
    @abstractmethod
    def increment(
        self,
        student: Person,
        reward: ExerciseRewardDTO,
        is_completed: bool,
    ) -> None:
        """Add reward."""
