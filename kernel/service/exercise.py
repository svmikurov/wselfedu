"""Generic exercise service."""

from typing import Protocol, TypeAlias, TypeVar, override

from apps.users.models import Person
from interfaces.protocols.domain.exercise import (
    CandidatesT,
    ConditionsProtocol,
    ExerciseConfigProtocol,
    TestAnswerProtocol,
    TestDomainResultProtocol,
)
from interfaces.protocols.spec.exercise import CheckTestSpecProtocol
from ports.abstract.service import AbstractUserSpecService
from ports.contract.entity.domain.exercise import fields
from ports.contract.entity.domain.exercise.flow import (
    PresentationDomainResultProtocol,
)
from ports.contract.entity.domain.general import HasCheckResult
from ports.contract.entity.domain.params import HasConditions, HasConfig
from ports.contract.infra.domain.exercise import (
    CheckTaskDomainProtocol,
    CreateTaskDomainProtocol,
)
from ports.contract.infra.formatter import ConfFormatterProtocol
from ports.contract.infra.repository import RepositoryProtocol
from utils.audit.base import BaseAuditable
from utils.audit.protocol import AuditorProtocol

__all__ = (
    'CreateExerciseService',
    'CheckExerciseService',
)

CreateResultT = TypeVar('CreateResultT', bound=fields.HasExerciseStatus)

CheckSpecT = TypeVar('CheckSpecT', bound=CheckTestSpecProtocol)
CheckResultT = TypeVar('CheckResultT', bound=HasCheckResult)

CaseAlias: TypeAlias = PresentationDomainResultProtocol

ExerciseDomainAlias: TypeAlias = CreateTaskDomainProtocol[
    ExerciseConfigProtocol,
    PresentationDomainResultProtocol,
]


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
    AbstractUserSpecService[_SpecT, CreateResultT],
):
    """Creates exercise case."""

    def __init__(
        self,
        candidates_repository: RepositoryProtocol[
            ConditionsProtocol,
            CandidatesT,
        ],
        domain: ExerciseDomainAlias,
        formatter: ConfFormatterProtocol[
            CaseAlias,
            ExerciseConfigProtocol,
            CreateResultT,
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
    ) -> CreateResultT:
        """Create and return exercise case."""
        candidates = self._repository.fetch(user, spec.conditions)
        domain = self._domain.execute(candidates, spec.conf)
        case = self._formatter.format(domain, spec.conf)
        return case


# =================================================
# Check
# =================================================


class CheckExerciseService(
    BaseAuditable,
    AbstractUserSpecService[
        CheckSpecT,
        CheckResultT,
    ],
):
    """Check exercise case."""

    def __init__(
        self,
        domain: CheckTaskDomainProtocol[
            TestAnswerProtocol,
            TestDomainResultProtocol,
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
        spec: CheckSpecT,
    ) -> CheckResultT:
        """Check user's solution."""
        # HACK: Implement no case handling
        if not spec.case:
            raise ValueError('Expected `TestDomainResultProtocol`, got None')

        self.auditor.record('domain.call', obj=self._domain, spec=spec)
        result = self._domain.execute(spec.answer, spec.case)
        return result
