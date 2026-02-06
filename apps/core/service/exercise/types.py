"""Exercise typing."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.core.domain.exercise.types import (
        CheckResult,
        ExerciseCase,
        ExerciseCaseMeta,
        ExerciseRequest,
        Explanation,
    )
    from apps.core.storage.services.iabc import TaskStorageABC

    from .abstract import (
        AbstractDetailExerciseCreate,
        AbstractExerciseCheck,
        AbstractExerciseCreate,
        AbstractExerciseExplain,
        AbstractMilestone,
    )

    type StorageService = TaskStorageABC[ExerciseCaseMeta]
    type CheckService = AbstractExerciseCheck[
        ExerciseCaseMeta, ExerciseRequest, CheckResult
    ]
    type CreateService = AbstractExerciseCreate[ExerciseCase]
    type CreateDetailService = AbstractDetailExerciseCreate[ExerciseCase]
    type ExplainService = AbstractExerciseExplain[
        ExerciseCaseMeta, ExerciseRequest, Explanation
    ]
    type MilestoneService = AbstractMilestone[CheckResult, ExerciseCaseMeta]
