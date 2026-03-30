"""Generic exercise service."""

from typing import TypeVar

from apps.core.domains.exercise.abstract import (
    AbstractCheckExerciseDomain,
    AbstractConfigurableCandidatesExerciseDomain,
)
from apps.core.domains.exercise.dto import TextExerciseCheckResult
from apps.core.domains.exercise.protocol import (
    Candidates,
    ExerciseParameters,
    HasExerciseConditions,
    HasExerciseConfig,
)
from apps.core.domains.exercise.test.dto import (
    TestExerciseMeta,
)
from apps.core.repositories.abstract import AbstractRepository
from apps.core.storages.services.iabc import TaskStorageABC
from apps.users.models import Person

from .abstract import (
    AbstractCheckExerciseService,
    AbstractCreateExerciseService,
    AbstractExplainExerciseService,
)

__all__ = ('CreateExerciseService',)

UserAnswer = TypeVar('UserAnswer')

# Current exercise case data
Case = TypeVar('Case')
CaseMeta = TypeVar('CaseMeta')

# Current exercise case solve
CheckResult = TypeVar('CheckResult')


# =================================================
# Create
# =================================================


class CreateExerciseService(
    AbstractCreateExerciseService[
        ExerciseParameters[
            HasExerciseConditions[object],
            HasExerciseConfig[object],
            object,
        ],
        Case,
        CaseMeta,
    ],
):
    """Creates exercise case."""

    def __init__(
        self,
        candidates_repository: AbstractRepository[
            HasExerciseConditions[object] | HasExerciseConfig[object],
            Candidates,
        ],
        domain: AbstractConfigurableCandidatesExerciseDomain[
            HasExerciseConfig[object],
            tuple[Case, CaseMeta],
        ],
        storage: TaskStorageABC[TestExerciseMeta],
    ) -> None:
        """Construct the service."""
        self._repository = candidates_repository
        self._domain = domain
        self._storage = storage

    def execute(
        self,
        parameters: ExerciseParameters[
            HasExerciseConditions[object],
            HasExerciseConfig[object],
            object,
        ],
        user: Person,
    ) -> tuple[Case, CaseMeta]:
        """Create and return exercise case."""
        candidates = self._repository.fetch(user, parameters.conditions)
        return self._domain.execute(candidates, parameters.conf)


# =================================================
# Check
# =================================================


class CheckExerciseService(
    AbstractCheckExerciseService[
        UserAnswer,
        CaseMeta,
        CheckResult,
    ],
):
    """Check exercise case."""

    def __init__(
        self,
        domain: AbstractCheckExerciseDomain[UserAnswer, CaseMeta, CheckResult],
    ) -> None:
        """Construct the service."""
        self._domain = domain

    def execute(
        self,
        answer: UserAnswer,
        case_meta: CaseMeta,
    ) -> CheckResult:
        """Check user's solution."""
        return self._domain.execute(answer, case_meta)


# =================================================
# Explain
# =================================================


class ExplainExerciseService(
    AbstractExplainExerciseService[
        UserAnswer,
        CaseMeta,
        TextExerciseCheckResult,
    ],
):
    """Explain exercise service."""

    def execute(
        self,
        answer: UserAnswer,
        case_meta: CaseMeta,
    ) -> TextExerciseCheckResult:
        return TextExerciseCheckResult(
            is_correct=False,
            question_text='question_text',
            answer_text='answer_text',
            selected_question_text='selected_question_text',
            selected_answer_text='selected_answer_text',
        )
