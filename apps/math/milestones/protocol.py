"""Protocols for mathematical discipline milestone."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

CaseMeta_contra = TypeVar('CaseMeta_contra', contravariant=True)
Result_contra = TypeVar('Result_contra', contravariant=True)

if TYPE_CHECKING:
    from apps.users.models import Person

# -----------------------------------------------
# Milestone dependencies
# -----------------------------------------------


# NOTE: It's experimental interface definition
class ProgressBar(Protocol[Result_contra, CaseMeta_contra]):
    """Protocol for tracking progress."""

    def increment(
        self,
        resource_pk: int,
        user: Person,
        result: Result_contra,
        case_meta: CaseMeta_contra,
    ) -> None:
        """Increase progress.

        Increases question progress as a result of an answer.
        """

    def decrement(
        self,
        resource_pk: int,
        user: Person,
        result: Result_contra,
        case_meta: CaseMeta_contra,
    ) -> None:
        """Decrease progress.

        Decreases question and answer progress
        in the event of an incorrect answer
        """


# -----------------------------------------------
# Milestone
# -----------------------------------------------


class MilestoneProtocol(Protocol[Result_contra, CaseMeta_contra]):
    """Protocol for exercise perform milestone interface."""

    def execute(
        self,
        resource_pk: int,
        user: Person,
        result: Result_contra,
        case_meta: CaseMeta_contra,
    ) -> None:
        """Execute."""
