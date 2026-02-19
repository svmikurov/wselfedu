"""Milestone dependency service."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from apps.math.domains.dto import CalculationMetaDTO, CalculationResultDTO
from apps.users.models.user import Person
from utils import decorators

from .protocol import ProgressBar, RewardScale

if TYPE_CHECKING:
    from apps.users.models.user import Person

type _AwardService = RewardScale
type _ProgressService = ProgressBar[CalculationResultDTO, CalculationMetaDTO]

__all__ = [
    'CalculationProgressService',
    'CalculationRewardService',
]


# TODO: Implement calculation progress service
# Temporary uses for dependency injection stub
class CalculationProgressService(
    ProgressBar[CalculationResultDTO, CalculationMetaDTO]
):
    """Calculation progress service."""

    @override
    @decorators.log_unimplemented_call
    def increment(
        self,
        resource_pk: int,
        user: Person,
        result: CalculationResultDTO,
        case_meta: CalculationMetaDTO,
    ) -> None:
        """Increase progress.

        Increases question progress as a result of an answer.
        """
        ...

    @override
    @decorators.log_unimplemented_call
    def decrement(
        self,
        resource_pk: int,
        user: Person,
        result: CalculationResultDTO,
        case_meta: CalculationMetaDTO,
    ) -> None:
        """Decrease progress.

        Decreases question and answer progress
        in the event of an incorrect answer
        """
        ...


class CalculationRewardService(RewardScale):
    """Calculation exercise reward service."""

    @override
    @decorators.log_unimplemented_call
    def increment(self, resource_pk: int, user: Person) -> None:
        """Add reward."""

    @override
    @decorators.log_unimplemented_call
    def decrement(self, resource_pk: int, user: Person) -> None:
        """Remove reward."""
