"""Generic exercise service."""

from typing import TypeVar, override

from apps.core.assemblers.protocol import DataCommandProtocol
from apps.core.domains.exercise.abstract import (
    AbstractCheckExerciseDomain,
    AbstractConfigurableCandidatesExerciseDomain,
)
from apps.core.domains.exercise.dto import (
    ExerciseDomainResultDTO,
    TextExerciseExplainDTO,
)
from apps.core.domains.exercise.enums import ExerciseStatusEnum
from apps.core.domains.exercise.protocol import (
    Candidates,
    ExerciseParameters,
    HasExerciseConditions,
    HasExerciseConfig,
)
from apps.core.domains.exercise.test.dto import (
    TestExerciseMeta,
)
from apps.core.domains.exercise.test.protocol import HasOptionValue
from apps.core.repositories.abstract import AbstractUserFetchRepository
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
        candidates_repository: AbstractUserFetchRepository[
            HasExerciseConditions[object] | HasExerciseConfig[object],
            Candidates,
        ],
        domain: AbstractConfigurableCandidatesExerciseDomain[
            HasExerciseConfig[object],
            tuple[Case, CaseMeta],
        ],
    ) -> None:
        """Construct the service."""
        self._repository = candidates_repository
        self._domain = domain

    @override
    def execute(
        self,
        user: Person,
        spec: ExerciseParameters[
            HasExerciseConditions[object],
            HasExerciseConfig[object],
            object,
        ],
    ) -> tuple[Case, CaseMeta]:
        """Create and return exercise case."""
        candidates = self._repository.fetch(user, spec.conditions)
        return self._domain.execute(candidates, spec.conf)


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
        DataCommandProtocol[HasOptionValue],
        TestExerciseMeta,
        TextExerciseExplainDTO,
    ],
):
    """Explain exercise service."""

    def execute(  # type: ignore
        self,
        command: DataCommandProtocol[HasOptionValue],
        case_meta: TestExerciseMeta,
    ) -> ExerciseDomainResultDTO[TextExerciseExplainDTO]:
        explain = TextExerciseExplainDTO(
            question_text=case_meta.question_text,
            answer_text=case_meta.answer_text,
            selected_question_text=case_meta.get_question_text(
                command.data.option_value
            ),
            selected_answer_text=case_meta.get_answer_text(
                command.data.option_value
            ),
        )
        return ExerciseDomainResultDTO(
            status=ExerciseStatusEnum.EXPLAIN,
            exercise=explain,
        )
