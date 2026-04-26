"""Abstract base classes for exercise case services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar, override

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

    @override
    @abstractmethod
    def execute(
        self,
        user: Person,
        spec: SpecT,
    ) -> CaseT:
        """Create the exercise case."""
