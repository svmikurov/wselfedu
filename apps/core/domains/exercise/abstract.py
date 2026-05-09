"""Abstract base class for exercise domain business logic."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from contracts.infra.domain.exercise import CheckTaskDomainProtocol
from interfaces.protocols.domain.exercise import (
    CandidateProtocol,
    CandidatesT,
)

ConfT = TypeVar('ConfT')
CaseT = TypeVar('CaseT')
TaskT = TypeVar('TaskT')

CandidateT = TypeVar('CandidateT', bound=CandidateProtocol)
UserAnswerT = TypeVar('UserAnswerT')
ResultT = TypeVar('ResultT')


# =================================================
# Create exercise
# =================================================


class AbstractConfigurableCandidatesExerciseDomain(
    ABC,
    Generic[ConfT, TaskT],
):
    """ABC for configurable exercise domain."""

    @abstractmethod
    def execute(
        self,
        candidates: CandidatesT,
        conf: ConfT,
    ) -> TaskT:
        """Create exercise case."""


# =================================================
# Check exercise
# =================================================


class AbstractCheckExerciseDomain(
    ABC,
    CheckTaskDomainProtocol[UserAnswerT, CaseT, ResultT],
):
    """ABC for check user answer domain business logic."""

    @abstractmethod
    def execute(
        self,
        answer: UserAnswerT,
        case: CaseT,
    ) -> ResultT:
        """Check user's answer."""
