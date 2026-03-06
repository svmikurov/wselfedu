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
from apps.study.models.exercise.reward import RewardType
from apps.study.services.abstract import AbstractCompletionService
from apps.users.domains.dto import RewardDTO
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
        availability: ExerciseAvailabilityDTO | None,
        completion: ExerciseCompletionDTO | None,
        reward: ExerciseRewardDTO | None,
    ) -> None:
        """Execute.

        Parameters
        ----------
        resource_pk : `int`
            Current exercise database identifier.

        """
        if result.is_correct:
            if (
                completion
                and availability
                and completion.success_count < availability.required_count
            ):
                self._completion_service.add_success(resource_pk)
            else:
                return

            if current_reward := self._get_reward(user, availability, reward):
                self._reward_service.increment(current_reward)

        else:
            self._completion_service.add_failure(resource_pk)

    # HACK: Implement reward type
    def _get_reward(
        self,
        student: Person,
        availability: ExerciseAvailabilityDTO | None,
        reward: ExerciseRewardDTO | None = None,
    ) -> RewardDTO | None:
        if (
            reward
            and reward.reward_type is RewardType.PER_CASE
            and availability
            and availability.is_active
            and not availability.is_completed
        ):
            return RewardDTO(
                student=student,
                amount=Decimal(reward.reward_amount),
            )
        return None
