"""Generic exercise service."""

from typing import Protocol, TypeVar, override

from apps.core.assemblers.protocol import DataCommandProtocol
from apps.core.domains.exercise.abstract import (
    AbstractCheckExerciseDomain,
)
from apps.core.domains.exercise.dto import (
    TextExerciseExplainDTO,
)
from apps.core.domains.exercise.protocol import (
    ConditionsProtocol,
    ExerciseConfigProtocol,
)
from apps.core.domains.exercise.test.dto import (
    OptionMetaDTO,
    TestExerciseMeta,
)
from apps.core.domains.task.protocol import TaskBuilderProtocol
from apps.core.repositories.protocol import UserRepositoryProtocol
from apps.users.models import Person
from interfaces import aliases
from interfaces.entity.domain.exercise import fields
from interfaces.entity.domain.params import HasConditions, HasConfig
from interfaces.schemas.domain.exercise.dtos import (
    ExplainExerciseDomainResult,
)

from .abstract import AbstractExerciseService

__all__ = (
    'CreateExerciseService',
    'CheckExerciseService',
    'ExplainExerciseService',
)

SpecT = TypeVar('SpecT')
CaseT = TypeVar('CaseT', bound=aliases.CaseAlias)
TaskT = TypeVar('TaskT')

BuilderT = TypeVar('BuilderT')
CaseMetaT = TypeVar('CaseMetaT')
ResultT = TypeVar('ResultT', bound=fields.HasExerciseStatus)
UserAnswerT = TypeVar('UserAnswerT')
CheckResultT = TypeVar('CheckResultT')


class _SpecT(
    HasConditions[ConditionsProtocol],
    HasConfig[ExerciseConfigProtocol],
    Protocol,
):
    """Protocol for exercise service specification."""


# =================================================
# Create
# =================================================


class CreateExerciseService(
    AbstractExerciseService[_SpecT, ResultT],
):
    """Creates exercise case."""

    def __init__(
        self,
        candidates_repository: UserRepositoryProtocol[
            ConditionsProtocol,
            aliases.CandidatesAlias,
        ],
        domain: aliases.ExerciseDomainAlias,
        builder: TaskBuilderProtocol[
            aliases.CaseAlias,
            ExerciseConfigProtocol,
            ResultT,
        ],
    ) -> None:
        """Construct the service."""
        self._repository = candidates_repository
        self._domain = domain
        self._builder = builder

    @override
    def execute(
        self,
        user: Person,
        spec: _SpecT,
    ) -> ResultT:
        """Create and return exercise case."""
        candidates = self._repository.fetch(user, spec.conditions)
        result = self._domain.execute(candidates, spec.conf)
        return self._builder.build(result, spec.conf)


# =================================================
# Check
# =================================================


class CheckExerciseService(
    AbstractExerciseService[
        SpecT,
        ResultT,
    ],
):
    """Check exercise case."""

    def __init__(
        self,
        domain: AbstractCheckExerciseDomain[
            Person,
            SpecT,
            CheckResultT,
        ],
    ) -> None:
        """Construct the service."""
        self._domain = domain

    @override
    def execute(
        self,
        user: Person,
        spec: SpecT,
    ) -> ResultT:
        """Check user's solution."""
        return self._domain.execute(user, spec)  # type: ignore


# =================================================
# Explain
# =================================================


class ExplainExerciseService(
    AbstractExerciseService[
        DataCommandProtocol[fields.HasQuestionOptionValue],
        TestExerciseMeta[OptionMetaDTO],
    ],
):
    """Explain exercise service."""

    def execute(  # type: ignore
        self,
        command: DataCommandProtocol[fields.HasQuestionOptionValue],
        case_meta: TestExerciseMeta[OptionMetaDTO],
    ) -> object:
        """Explain exercise."""
        explain = TextExerciseExplainDTO(
            question_text=case_meta.question_text,
            answer_text=case_meta.answer_text,
            selected_question_text=case_meta.get_question_text(
                command.data.option_value
            ),
            selected_answer_text=case_meta.get_answer_text(
                command.data.option_value,
            ),
        )
        assert explain
        # TODO: Update after explain DTO implementation
        return ExplainExerciseDomainResult()
