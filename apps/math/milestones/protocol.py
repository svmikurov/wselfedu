"""Protocols for mathematical discipline milestone."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

ExerciseMeta_contra = TypeVar('ExerciseMeta_contra', contravariant=True)
Result_contra = TypeVar('Result_contra', contravariant=True)
Availability_contra = TypeVar('Availability_contra', contravariant=True)
Reward_contra = TypeVar('Reward_contra', contravariant=True)

if TYPE_CHECKING:
    from apps.users.models import Person

# -----------------------------------------------
# Milestone dependencies
# -----------------------------------------------


# NOTE: It's experimental interface definition
class ProgressBar(Protocol[Result_contra, ExerciseMeta_contra]):
    """Protocol for tracking progress."""

    def increment(
        self,
        resource_pk: int,
        user: Person,
        result: Result_contra,
        meta: ExerciseMeta_contra,
    ) -> None:
        """Increase progress.

        Increases question progress as a result of an answer.
        """

    def decrement(
        self,
        resource_pk: int,
        user: Person,
        result: Result_contra,
        meta: ExerciseMeta_contra,
    ) -> None:
        """Decrease progress.

        Decreases question and answer progress
        in the event of an incorrect answer
        """


# -----------------------------------------------
# Milestone
# -----------------------------------------------


class MilestoneServiceProtocol(
    Protocol[
        ExerciseMeta_contra,
        Result_contra,
        Availability_contra,
        Reward_contra,
    ]
):
    """Protocol for exercise perform milestone service interface."""

    def execute(
        self,
        resource_pk: int,
        user: Person,
        meta: ExerciseMeta_contra,
        result: Result_contra,
        availability: Availability_contra | None = None,
        reward: Reward_contra | None = None,
    ) -> None:
        """Execute."""
