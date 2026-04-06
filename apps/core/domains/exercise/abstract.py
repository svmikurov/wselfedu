"""Abstract base class for exercise domain business logic."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar, override

from .protocol import SelectorProtocol

if TYPE_CHECKING:
    from .protocol import Candidates

Conf = TypeVar('Conf')
Case = TypeVar('Case')
Task = TypeVar('Task')
CaseMeta = TypeVar('CaseMeta')
UserAnswer = TypeVar('UserAnswer')
CheckResult = TypeVar('CheckResult')

# =================================================
# Candidates selector for exercise
# =================================================


class AbstractSelector(
    ABC,
    SelectorProtocol[Conf],
    Generic[Conf],
):
    """ABC for candidates selector by configuration."""

    @override
    @abstractmethod
    def select(
        self,
        candidates: Candidates,
        conf: Conf,
    ) -> Candidates:
        """Select data for exercise."""


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
        candidates: Candidates,
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
