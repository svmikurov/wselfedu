"""User application protocols."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from apps.math.domains.dto import ExerciseRewardDTO
    from apps.users.models.user import Person

__all__ = ('RewardServiceProtocol',)


class RewardServiceProtocol(Protocol):
    """Protocol for reward interface."""

    def increment(
        self,
        student: Person,
        reward: ExerciseRewardDTO,
        is_completed: bool,
    ) -> None:
        """Add reward."""
