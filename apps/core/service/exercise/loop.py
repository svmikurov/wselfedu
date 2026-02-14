"""Exercise loop."""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.core.domain.exercise import ExerciseStatusEnum
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
        self, user: Person, schema: ExerciseRequest
    ) -> ExerciseCase | Explanation:
        """Execute exercise loop."""
        print(f'{schema = }')
        match schema.exercise_status:
            case ExerciseStatusEnum.NEW_CASE:
                return self._create_service.execute(user)

            # REVIEW: Creates services below on crate new case event
            case ExerciseStatusEnum.ANSWER:
                case_meta = self._storage.retrieve_task(schema.case_uuid)
                result = self._check_service.execute(schema, case_meta)

                if self._milestone_service:
                    self._milestone_service.execute(user, result, case_meta)

                if result.is_correct:
                    return self._create_service.execute(user)
                return self._explain_service.execute(schema, case_meta)

            case _:
                raise ValueError(
                    f'Got unexpected exercise status: {schema.exercise_status}'
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
        self, user: Person, schema: ExerciseRequest
    ) -> ExerciseCase | Explanation:
        """Execute exercise loop."""
        match schema.exercise_status:
            case ExerciseStatusEnum.NEW_CASE:
                return self._create_service.execute(user, schema.pk)

            # REVIEW: Creates services below on crate new case event
            case ExerciseStatusEnum.ANSWER:
                case_meta = self._storage.retrieve_task(schema.case_uuid)
                result = self._check_service.execute(schema, case_meta)

                if self._milestone_service:
                    self._milestone_service.execute(user, result, case_meta)

                if result.is_correct:
                    return self._create_service.execute(user, schema.pk)
                return self._explain_service.execute(schema, case_meta)

            case _:
                raise ValueError(
                    f'Got unexpected exercise status: {schema.exercise_status}'
                )
