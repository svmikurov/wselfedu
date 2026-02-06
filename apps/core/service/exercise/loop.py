"""Exercise loop."""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.core.domain.exercise import CaseStatus
from apps.core.domain.exercise.types import (
    ExerciseCase,
    ExerciseRequest,
    Explanation,
)

from .abstract import AbstractExerciseLoop

if TYPE_CHECKING:
    from apps.users.models import Person

    from . import types

# TODO: Improve protocols


class RegularExerciseLoop(
    AbstractExerciseLoop[ExerciseRequest, ExerciseCase, Explanation]
):
    """Regular exercise loop."""

    def __init__(
        self,
        storage: types.StorageService,
        check_service: types.CheckService,
        create_service: types.CreateService,
        explain_service: types.ExplainService,
        milestone_service: types.MilestoneService | None = None,
    ) -> None:
        """Construct the loop."""
        self._storage = storage
        self._check_service = check_service
        self._create_service = create_service
        self._explain_service = explain_service
        self._milestone_service = milestone_service

    def execute(
        self, user: Person, data: ExerciseRequest
    ) -> ExerciseCase | Explanation:
        """Execute exercise loop."""
        match data.status:
            case CaseStatus.NEW_CASE:
                return self._create_service.execute(user)

            # REVIEW: Creates services below on crate new case event
            case CaseStatus.ANSWER:
                case_meta = self._storage.retrieve_task(data.case_uuid)
                result = self._check_service.execute(case_meta, data)

                if self._milestone_service:
                    self._milestone_service.execute(user, result, case_meta)

                if result.is_correct:
                    return self._create_service.execute(user)
                return self._explain_service.execute(case_meta, data)

            case _:
                raise ValueError(
                    f'Got unexpected exercise status: {data.status}'
                )


class DetailExerciseLoop(
    AbstractExerciseLoop[ExerciseRequest, ExerciseCase, Explanation]
):
    """Detail exercise loop."""

    def __init__(
        self,
        storage: types.StorageService,
        check_service: types.CheckService,
        create_service: types.CreateDetailService,
        explain_service: types.ExplainService,
        milestone_service: types.MilestoneService | None = None,
    ) -> None:
        """Construct the loop."""
        self._storage = storage
        self._check_service = check_service
        self._create_service = create_service
        self._explain_service = explain_service
        self._milestone_service = milestone_service

    def execute(
        self, user: Person, data: ExerciseRequest
    ) -> ExerciseCase | Explanation:
        """Execute exercise loop."""
        match data.status:
            case CaseStatus.NEW_CASE:
                return self._create_service.execute(user, data.pk)

            # REVIEW: Creates services below on crate new case event
            case CaseStatus.ANSWER:
                case_meta = self._storage.retrieve_task(data.case_uuid)
                result = self._check_service.execute(case_meta, data)

                if self._milestone_service:
                    self._milestone_service.execute(user, result, case_meta)

                if result.is_correct:
                    return self._create_service.execute(user, data.pk)
                return self._explain_service.execute(case_meta, data)

            case _:
                raise ValueError(
                    f'Got unexpected exercise status: {data.status}'
                )
