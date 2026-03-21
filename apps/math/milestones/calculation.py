"""Calculation exercise milestone."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, override

from django.db.models import Manager

from apps.math.domains.dto import (
    CalculationMetaDTO,
    CalculationResultDTO,
    ExerciseAvailabilityDTO,
    ExerciseCompletionDTO,
    ExerciseRewardDTO,
)
from apps.math.models import StudentCalculationCondition
from apps.study.services.abstract import AbstractCompletionService
from apps.users.services.protocol import RewardServiceProtocol

from .protocol import MilestoneServiceProtocol, ProgressBar

if TYPE_CHECKING:
    from apps.users.models.user import Person

type _RewardService = RewardServiceProtocol
type _ProgressService = ProgressBar[CalculationResultDTO, CalculationMetaDTO]
type _CompletionService = AbstractCompletionService[
    StudentCalculationCondition
]
# HACK: Implement DIP
type _ExerciseManager = Manager[StudentCalculationCondition]

# HACK: Remove temporary amount constant
TEMPORARY_AMOUNT = Decimal(10)


# NOTE: It's experimental milestone definition
class UserCalculationMilestone(
    MilestoneServiceProtocol[
        CalculationMetaDTO,
        CalculationResultDTO,
        ExerciseAvailabilityDTO,
        ExerciseCompletionDTO,
        ExerciseRewardDTO,
    ]
):
    """User calculation exercise perform milestone."""

    def __init__(
        self,
        progress_service: _ProgressService,
    ) -> None:
        """Construct the milestone."""
        self._progress_service = progress_service

    @override
    def execute(  # noqa: D417
        self,
        resource_pk: int,
        user: Person,
        meta: CalculationMetaDTO,
        result: CalculationResultDTO,
        availability: ExerciseAvailabilityDTO | None,
        completion: ExerciseCompletionDTO | None,
        # FIXME: Remove reward
        reward: ExerciseRewardDTO | None,
    ) -> None:
        if result.is_correct:
            self._progress_service.increment(resource_pk, user, result, meta)
        else:
            self._progress_service.decrement(resource_pk, user, result, meta)


# NOTE: It's experimental milestone definition
class StudentCalculationMilestone(
    MilestoneServiceProtocol[
        CalculationMetaDTO,
        CalculationResultDTO,
        ExerciseAvailabilityDTO,
        ExerciseCompletionDTO,
        ExerciseRewardDTO,
    ]
):
    """Student calculation exercise perform milestone.

    Attributes
    ----------
    reward_service : `_RewardService`
        Reward service.
    completion_service : `_CompletionService`
        Service to track a assigned exercise task **count** completion.
    progress_service : `_ProgressService`
        Service to track a calculation study **progress**.
    exercise_manager : `_ExerciseManager`
        ORM model manager to get mentorship identifier by current
        exercise identifier and by student model instance relationship.

    """

    def __init__(
        self,
        reward_service: _RewardService,
        completion_service: _CompletionService,
        exercise_manager: _ExerciseManager,
    ) -> None:
        """Construct the milestone."""
        self._reward_service = reward_service
        self._completion_service = completion_service
        self._exercise_manager = exercise_manager

    @override
    def execute(  # noqa: D417
        self,
        resource_pk: int,
        user: Person,
        meta: CalculationMetaDTO,
        result: CalculationResultDTO,
        availability: ExerciseAvailabilityDTO,
        completion: ExerciseCompletionDTO,
        reward: ExerciseRewardDTO | None,
    ) -> None:
        """Execute.

        Parameters
        ----------
        resource_pk : `int`
            Current exercise database identifier.

        """
        # If a student successfully completes the specified
        # number of tasks, no milestone are set.
        # However, the student must be given the opportunity
        # to perform assignments without milestones.
        if (
            availability.is_completed
            or not availability.is_active
            or completion.success_count >= availability.required_count
        ):
            return

        if not result.is_correct:
            self._completion_service.add_failure(resource_pk)
            return

        # FIXME: Implement atomic transaction
        # for completion mark and reward
        is_completed = self._completion_service.add_success(
            resource_pk,
            availability,
            completion,
        )

        if reward:
            self._reward_service.increment(user, reward, is_completed)
