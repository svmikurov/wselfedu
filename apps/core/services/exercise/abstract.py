"""Abstract base classes for exercise case services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar, override

from utils.audit.impl import NullAuditor
from utils.audit.protocol import AuditorProtocol

from .protocol import ExerciseServiceProtocol

if TYPE_CHECKING:
    from apps.users.models import Person

SpecT = TypeVar('SpecT')
CaseT = TypeVar('CaseT')


class AbstractExerciseService(
    ABC,
    ExerciseServiceProtocol[SpecT, CaseT],
):
    """ABC for exercise case services."""

    def __init__(
        self,
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the adapter."""
        self._name = name or 'undefined'
        self._auditor = auditor or NullAuditor()

    @override
    @abstractmethod
    def execute(
        self,
        user: Person,
        spec: SpecT,
    ) -> CaseT:
        """Create the exercise case."""

    @property
    def name(self) -> str:
        """Return adapter name."""
        return self._name
