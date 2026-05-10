"""Abstract base classes for exercise case services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar, override

from ports.contract.infra.service import UserSpecServiceProtocol

if TYPE_CHECKING:
    from apps.users.models import Person

SpecT = TypeVar('SpecT')
CaseT = TypeVar('CaseT')


class AbstractUserSpecService(
    ABC,
    UserSpecServiceProtocol[SpecT, CaseT],
):
    """ABC for user's service follows the specification."""

    @override
    @abstractmethod
    def execute(
        self,
        user: Person,
        spec: SpecT,
    ) -> CaseT:
        """Create the exercise case."""
