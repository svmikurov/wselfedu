"""Exercise typing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from apps.core.domains.exercise.types import (
        CheckResult,
        ExerciseCase,
        ExerciseCaseMeta,
        ExerciseRequest,
        Explanation,
    )
    from apps.core.storages.services.iabc import TaskStorageABC

    from .abstract import (
        AbstractDetailExerciseCreate,
        AbstractExerciseCheck,
        AbstractExerciseCreate,
        AbstractExerciseExplain,
        AbstractMilestone,
        AbstractUuidExerciseCreate,
    )

    type StorageService = TaskStorageABC[ExerciseCaseMeta]
    type CheckService = AbstractExerciseCheck[
        ExerciseRequest, ExerciseCaseMeta, CheckResult
    ]
    type CreateService = AbstractExerciseCreate[ExerciseCase]
    type CreateDetailService = AbstractDetailExerciseCreate[ExerciseCase]
    # HACK: Fix Any
    type CreateConditionService = AbstractUuidExerciseCreate[Any, ExerciseCase]
    type ExplainService = AbstractExerciseExplain[
        ExerciseRequest, ExerciseCaseMeta, Explanation
    ]
    type MilestoneService = AbstractMilestone[CheckResult, ExerciseCaseMeta]
