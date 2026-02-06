"""Abstract base class for exercise domain business logic."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from .types import Candidates, CheckResult, TestCheckRequest

T = TypeVar('T')
R = TypeVar('R')


class AbstractCreateExerciseDomain(ABC, Generic[T, R]):
    """Abstract base class for exercise domain business logic."""

    @abstractmethod
    def execute(self, candidates: Candidates, settings: T) -> R:
        """Create exercise case."""


class AbstractCreateDetailExerciseDomain(ABC, Generic[R]):
    """Abstract base class for detail exercise domain business logic."""

    @abstractmethod
    def execute(self, candidates: Candidates) -> R:
        """Create exercise case."""


class AbstractCheckExerciseDomain(ABC, Generic[T]):
    """ABC for check user answer domain business logic."""

    @abstractmethod
    def execute(self, case_meta: T, data: TestCheckRequest) -> CheckResult:
        """Check user's answer."""
