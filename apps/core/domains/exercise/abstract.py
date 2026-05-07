"""Abstract base class for exercise domain business logic."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from interfaces.protocols.domain.exercise import (
    CandidateProtocol,
    CandidatesProtocol,
)

Conf = TypeVar('Conf')
Case = TypeVar('Case')
Task = TypeVar('Task')

CandidateT = TypeVar('CandidateT', bound=CandidateProtocol)

CaseMeta = TypeVar('CaseMeta')
UserAnswer = TypeVar('UserAnswer')
CheckResult = TypeVar('CheckResult')


# =================================================
# Create exercise
# =================================================


class AbstractConfigurableCandidatesExerciseDomain(
    ABC,
    Generic[Conf, Task],
):
    """ABC for configurable exercise domain."""

    @abstractmethod
    def execute(
        self,
        candidates: CandidatesProtocol,
        conf: Conf,
    ) -> Task:
        """Create exercise case."""


# =================================================
# Check exercise
# =================================================


class AbstractCheckExerciseDomain(
    ABC,
    Generic[UserAnswer, CaseMeta, CheckResult],
):
    """ABC for check user answer domain business logic."""

    @abstractmethod
    def execute(
        self,
        answer: UserAnswer,
        case_meta: CaseMeta,
    ) -> CheckResult:
        """Check user's answer."""
