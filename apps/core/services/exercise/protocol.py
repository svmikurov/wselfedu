"""Protocols for core exercise case service interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

SpecT = TypeVar('SpecT', contravariant=True)
CaseT = TypeVar('CaseT', covariant=True)


class ExerciseServiceProtocol(Protocol[SpecT, CaseT]):
    """Protocol for exercise case service interface."""

    def execute(
        self,
        user: Person,
        spec: SpecT,
    ) -> CaseT:
        """Create the exercise case."""
