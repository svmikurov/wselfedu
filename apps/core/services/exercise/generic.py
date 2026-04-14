"""Generic exercise service."""

from typing import Protocol, TypeVar, override

from apps.core.assemblers.protocol import DataCommandProtocol
from apps.core.domains.exercise.abstract import (
    AbstractCheckExerciseDomain,
)
from apps.core.domains.exercise.dto import (
    ExerciseDomainResultDTO,
    TextExerciseExplainDTO,
)
from apps.core.domains.exercise.enums import ExerciseStatusEnum
from apps.core.domains.exercise.protocol import (
    Candidates,
    ConditionsProtocol,
    ExerciseConfigProtocol,
    ExerciseDomainProtocol,
    HasExerciseConditions,
    HasExerciseConfig,
    HasOptionValue,
)
from apps.core.domains.exercise.test.dto import (
    OptionMetaDTO,
    TestExerciseMeta,
)
from apps.core.repositories.protocol import UserRepositoryProtocol
from apps.users.models import Person

from .abstract import (
    AbstractCheckExerciseService,
    AbstractCreateExerciseService,
    AbstractExplainExerciseService,
)

__all__ = ('CreateExerciseService',)

# Current exercise case data
CaseT = TypeVar('CaseT')
TaskT = TypeVar('TaskT')
BuilderT = TypeVar('BuilderT')
CaseMetaT = TypeVar('CaseMetaT')


class _SpecT(
    HasExerciseConditions[ConditionsProtocol],
    HasExerciseConfig[ExerciseConfigProtocol],
    Protocol,
):
    """Protocol for exercise service specification."""


UserAnswerT = TypeVar('UserAnswerT')

# Current exercise case solve
CheckResultT = TypeVar('CheckResultT')


# =================================================
# Create
# =================================================


class CreateExerciseService(
    AbstractCreateExerciseService[
        _SpecT,
        CaseT,
    ],
):
    """Creates exercise case."""

    def __init__(
        self,
        candidates_repository: UserRepositoryProtocol[
            ConditionsProtocol,
            Candidates,
        ],
        domain: ExerciseDomainProtocol[
            ExerciseConfigProtocol,
            CaseT,
        ],
    ) -> None:
        """Construct the service."""
        self._repository = candidates_repository
        self._domain = domain

    @override
    def execute(
        self,
        user: Person,
        spec: _SpecT,
    ) -> CaseT:
        """Create and return exercise case."""
        candidates = self._repository.fetch(user, spec.conditions)
        case = self._domain.execute(candidates, spec.conf)
        return case


# =================================================
# Check
# =================================================


class CheckExerciseService(
    AbstractCheckExerciseService[
        UserAnswerT,
        CaseMetaT,
        CheckResultT,
    ],
):
    """Check exercise case."""

    def __init__(
        self,
        domain: AbstractCheckExerciseDomain[
            UserAnswerT,
            CaseMetaT,
            CheckResultT,
        ],
    ) -> None:
        """Construct the service."""
        self._domain = domain

    def execute(
        self,
        answer: UserAnswerT,
        case_meta: CaseMetaT,
    ) -> CheckResultT:
        """Check user's solution."""
        return self._domain.execute(answer, case_meta)


# =================================================
# Explain
# =================================================


class ExplainExerciseService(
    AbstractExplainExerciseService[
        DataCommandProtocol[HasOptionValue],
        TestExerciseMeta[OptionMetaDTO],
        TextExerciseExplainDTO,
    ],
):
    """Explain exercise service."""

    def execute(  # type: ignore
        self,
        command: DataCommandProtocol[HasOptionValue],
        case_meta: TestExerciseMeta[OptionMetaDTO],
    ) -> ExerciseDomainResultDTO[TextExerciseExplainDTO]:
        explain = TextExerciseExplainDTO(
            question_text=case_meta.question_text,
            answer_text=case_meta.answer_text,
            selected_question_text=case_meta.get_question_text(
                command.data.value
            ),
            selected_answer_text=case_meta.get_answer_text(
                command.data.value,
            ),
        )
        return ExerciseDomainResultDTO(
            status=ExerciseStatusEnum.EXPLAIN,
            exercise=explain,
        )
