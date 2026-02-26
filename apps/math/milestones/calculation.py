"""Calculation exercise milestone."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from django.db.models import Manager
from django.shortcuts import get_object_or_404

from apps.math.domains.dto import CalculationMetaDTO, CalculationResultDTO
from apps.math.models import StudentCalculationCondition
from apps.math.services.abstract import AbstractCompletionService
from apps.users.services.protocol import RewardServiceProtocol

from .protocol import MilestoneProtocol, ProgressBar

if TYPE_CHECKING:
    from apps.users.models.user import Person

type _RewardService = RewardServiceProtocol
type _ProgressService = ProgressBar[CalculationResultDTO, CalculationMetaDTO]
type _CompletionService = AbstractCompletionService[
    StudentCalculationCondition
]
# HACK: Implement DIP
type _ExerciseManager = Manager[StudentCalculationCondition]


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
    """Student calculation exercise perform milestone.

    Attributes
    ----------
    reward_service : `_RewardService`
        Reward service.
    completion_service : `_CompletionService`
        Service to track a assigned exercise task count completion.
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
        student: Person,
        result: CalculationResultDTO,
        case_meta: CalculationMetaDTO,
    ) -> None:
        """Execute.

        Parameters
        ----------
        resource_pk : `int`
            Current exercise database identifier.

        """
        mentorship_pk = self._get_mentorship_pk(resource_pk, student)
        if result.is_correct:
            self._reward_service.increment(resource_pk, mentorship_pk)
            self._completion_service.add_success(resource_pk)
        else:
            self._completion_service.add_failure(resource_pk)

    def _get_mentorship_pk(self, resource_pk: int, student: Person) -> int:
        return get_object_or_404(
            self._exercise_manager,
            pk=resource_pk,
            mentorship__student=student,
        ).mentorship.pk
