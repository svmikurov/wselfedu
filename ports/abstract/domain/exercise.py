"""Abstract base classes for exercise domain."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from interfaces.protocols.domain.exercise import CandidatesT
from ports.contract.infra.domain.exercise import CheckTaskDomainProtocol
from ports.contract.infra.domain.selector import SelectorProtocol

ConfT = TypeVar('ConfT')
CaseT = TypeVar('CaseT')
TaskT = TypeVar('TaskT')

UserAnswerT = TypeVar('UserAnswerT')
ResultT = TypeVar('ResultT')

# =================================================
# Candidates selector
# =================================================


class AbstractSelector(
    ABC,
    SelectorProtocol[ConfT],
    Generic[ConfT],
):
    """ABC for candidates selector by configuration."""

    @override
    @abstractmethod
    def select(
        self,
        candidates: CandidatesT,
        conf: ConfT,
    ) -> CandidatesT:
        """Select data for exercise."""


# =================================================
# Create exercise
# =================================================


class AbstractCandidatesExerciseDomain(
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
