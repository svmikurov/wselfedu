"""Calculation exercise milestone."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from apps.math.domains.dto import CalculationMetaDTO, CalculationResultDTO

from .protocol import MilestoneProtocol, ProgressBar, RewardScale

if TYPE_CHECKING:
    from apps.users.models.user import Person

type _RewardService = RewardScale
type _ProgressService = ProgressBar[CalculationResultDTO, CalculationMetaDTO]


# NOTE: It's experimental milestone definition
class UserCalculationMilestone(
    MilestoneProtocol[CalculationResultDTO, CalculationMetaDTO]
):
    """User calculation exercise perform milestone."""

    def __init__(
        self,
        progress_service: _ProgressService,
    ) -> None:
        """Construct the milestone."""
        self._progress_service = progress_service

    @override
    def execute(
        self,
        resource_pk: int,
        user: Person,
        result: CalculationResultDTO,
        case_meta: CalculationMetaDTO,
    ) -> None:
        """Execute."""
        if result.is_correct:
            self._progress_service.increment(
                resource_pk, user, result, case_meta
            )
        else:
            self._progress_service.decrement(
                resource_pk, user, result, case_meta
            )


# NOTE: It's experimental milestone definition
class StudentCalculationMilestone(
    MilestoneProtocol[CalculationResultDTO, CalculationMetaDTO]
):
    """Student calculation exercise perform milestone."""

    def __init__(
        self,
        reward_service: _RewardService,
        progress_service: _ProgressService,
    ) -> None:
        """Construct the milestone."""
        self._reward_service = reward_service
        self._progress_service = progress_service

    @override
    def execute(
        self,
        resource_pk: int,
        user: Person,
        result: CalculationResultDTO,
        case_meta: CalculationMetaDTO,
    ) -> None:
        """Execute."""
        if result.is_correct:
            self._reward_service.increment(resource_pk, user)
            self._progress_service.increment(
                resource_pk, user, result, case_meta
            )
        else:
            self._progress_service.decrement(
                resource_pk, user, result, case_meta
            )
