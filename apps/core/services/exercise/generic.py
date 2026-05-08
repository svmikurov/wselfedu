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
from apps.core.formatters.protocol import ConfFormatterProtocol
from apps.core.repositories.protocol import RepositoryProtocol
from apps.users.models import Person
from contracts import aliases
from contracts.entity.domain.exercise import fields
from contracts.entity.domain.params import HasConditions, HasConfig
from contracts.schemas.domain.exercise.flow import (
    ExplainExerciseDomainResult,
)
from interfaces.protocols.domain.exercise import CandidatesProtocol
from utils.audit.base import BaseAuditable
from utils.audit.protocol import AuditorProtocol

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
    BaseAuditable,
    AbstractExerciseService[_SpecT, ResultT],
):
    """Creates exercise case."""

    def __init__(
        self,
        candidates_repository: RepositoryProtocol[
            ConditionsProtocol,
            CandidatesProtocol,
        ],
        domain: aliases.ExerciseDomainAlias,
        formatter: ConfFormatterProtocol[
            aliases.CaseAlias,
            ExerciseConfigProtocol,
            ResultT,
        ],
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the service."""
        super().__init__(name=name, auditor=auditor)
        self._repository = candidates_repository
        self._domain = domain
        self._formatter = formatter

    @override
    def execute(
        self,
        user: Person,
        spec: _SpecT,
    ) -> ResultT:
        """Create and return exercise case."""
        candidates = self._repository.fetch(user, spec.conditions)
        domain = self._domain.execute(candidates, spec.conf)
        case = self._formatter.format(domain, spec.conf)
        return case


# =================================================
# Check
# =================================================


# FIXME: Fix type ignore
class CheckExerciseService(
    BaseAuditable,
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
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the service."""
        super().__init__(name=name, auditor=auditor)
        self._domain = domain

    @override
    def execute(
        self,
        user: Person,
        spec: SpecT,
    ) -> ResultT:
        """Check user's solution."""
        self.auditor.record('domain.call', obj=self._domain, spec=spec)  # type: ignore
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
                command.data.question_option_value
            ),
            selected_answer_text=case_meta.get_answer_text(
                command.data.question_option_value,
            ),
        )
        assert explain
        # TODO: Update after explain DTO implementation
        return ExplainExerciseDomainResult()
