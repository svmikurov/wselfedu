"""Core exercise."""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.core.domain.exercise import (
    TestExerciseData,
    TestExerciseExplanation,
    TestExerciseMeta,
)
from apps.core.domain.exercise.types import (
    CheckResult,
    TestCheckRequest,
)

from .abstract import (
    AbstractDetailExerciseCreate,
    AbstractExerciseCheck,
    AbstractExerciseCreate,
    AbstractExerciseExplain,
)

if TYPE_CHECKING:
    from uuid import UUID

    from apps.core.domain.exercise import TestExerciseCase
    from apps.core.domain.exercise.abstract import (
        AbstractCheckExerciseDomain,
        AbstractCreateDetailExerciseDomain,
        AbstractCreateExerciseDomain,
    )
    from apps.core.domain.exercise.types import ExerciseConfig, Settings
    from apps.core.repository.abstract import (
        AbstractConditionsExerciseRepository,
        AbstractParametersRepository,
    )
    from apps.core.storage.services.iabc import TaskStorageABC
    from apps.users.models import Person

    type CreateResult = tuple[TestExerciseCase, TestExerciseMeta]

__all__ = [
    'RegularTestCreate',
    'DetailTestCreate',
    'RegularTestCheck',
    'TestExplain',
]


class RegularTestCreate(AbstractExerciseCreate[TestExerciseData]):
    """Creates regular exercise case."""

    def __init__(
        self,
        parameters_repository: AbstractParametersRepository,
        candidates_repository: AbstractConditionsExerciseRepository,
        storage: TaskStorageABC[TestExerciseMeta],
        domain: AbstractCreateExerciseDomain[Settings, CreateResult],
        config: ExerciseConfig,
    ) -> None:
        """Construct the service."""
        self._parameters_repo = parameters_repository
        self._candidates_repo = candidates_repository
        self._storage = storage
        self._domain = domain
        self._config = config

    def execute(self, user: Person) -> TestExerciseData:
        """Create and return exercise case."""
        parameters = self._parameters_repo.fetch(user)
        candidates = self._candidates_repo.fetch(user, parameters.conditions)
        case, case_meta = self._domain.execute(candidates, parameters.settings)
        case_uuid = self._storage.save_task(case_meta)
        case_data = self._prepare_case(case_uuid, case)
        return case_data

    @staticmethod
    def _prepare_case(
        case_uuid: UUID, case: TestExerciseCase
    ) -> TestExerciseData:
        """Create stored exercise case."""
        return TestExerciseData(case_uuid=case_uuid, **case.model_dump())


class DetailTestCreate(AbstractDetailExerciseCreate[TestExerciseData]):
    """Creates detail (assigned) exercise case."""

    def __init__(
        self,
        candidates_repository: AbstractConditionsExerciseRepository,
        storage: TaskStorageABC[TestExerciseMeta],
        domain: AbstractCreateDetailExerciseDomain[CreateResult],
        config: ExerciseConfig,
    ) -> None:
        """Construct the service."""
        self._candidates_repo = candidates_repository
        self._storage = storage
        self._domain = domain
        self._config = config

    def execute(self, user: Person, exercise_pk: int) -> TestExerciseData:
        """Create and return exercise case."""
        candidates = self._candidates_repo.fetch(user, exercise_pk)

        case, case_meta = self._domain.execute(candidates)
        case_uuid = self._storage.save_task(case_meta)
        case_data = self._prepare_case(case_uuid, case)
        return case_data

    @staticmethod
    def _prepare_case(
        case_uuid: UUID, case: TestExerciseCase
    ) -> TestExerciseData:
        """Create stored exercise case."""
        return TestExerciseData(case_uuid=case_uuid, **case.model_dump())


class RegularTestCheck(
    AbstractExerciseCheck[TestExerciseMeta, TestCheckRequest, CheckResult]
):
    """Check user's answer."""

    def __init__(
        self,
        domain: AbstractCheckExerciseDomain[TestExerciseMeta],
    ) -> None:
        """Construct the service."""
        self._domain = domain

    def execute(
        self, case_meta: TestExerciseMeta, data: TestCheckRequest
    ) -> CheckResult:
        """Check user' answer."""
        return self._domain.execute(case_meta, data)


class TestExplain(
    AbstractExerciseExplain[
        TestExerciseMeta, TestCheckRequest, TestExerciseExplanation
    ]
):
    """Explain test exercise case."""

    def execute(
        self, case_meta: TestExerciseMeta, data: TestCheckRequest
    ) -> TestExerciseExplanation:
        """Explain the exercise case."""
        # EXPERIMENTAL: Possibly adding explanations
        return self._prepare_dto(case_meta, data)

    @staticmethod
    def _prepare_dto(
        case_meta: TestExerciseMeta, data: TestCheckRequest
    ) -> TestExerciseExplanation:
        return TestExerciseExplanation(
            question_text=case_meta.question_text,
            answer_text=case_meta.answer_text,
            selected_answer_text=case_meta.get_question_text(
                data.option_value
            ),
            selected_question_text=case_meta.get_answer_text(
                data.option_value
            ),
        )
