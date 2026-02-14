"""Abstract base class for exercise domain business logic."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from .types import Candidates, CheckResult, TestCheckRequest

T = TypeVar('T')
R = TypeVar('R')


class AbstractConditionsExerciseDomain(ABC, Generic[T, R]):
    """ABC to create exercise by conditions."""

    @abstractmethod
    def execute(self, conditions: T) -> R:
        """Create exercise case."""


class AbstractSettingsExerciseDomain(ABC, Generic[T, R]):
    """Abstract base class for exercise domain business logic."""

    @abstractmethod
    def execute(self, candidates: Candidates, settings: T) -> R:
        """Create exercise case."""


class AbstractCandidatesExerciseDomain(ABC, Generic[R]):
    """Abstract base class for detail exercise domain business logic."""

    @abstractmethod
    def execute(self, candidates: Candidates) -> R:
        """Create exercise case."""


class AbstractCheckExerciseDomain(ABC, Generic[T]):
    """ABC for check user answer domain business logic."""

    @abstractmethod
    def execute(self, answer: TestCheckRequest, case_meta: T) -> CheckResult:
        """Check user's answer."""
