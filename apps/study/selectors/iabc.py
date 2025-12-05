"""Defines protocols and ABC for Study app selectors."""

from abc import ABC, abstractmethod
from typing import Protocol

from typing_extensions import override

from apps.math.services.types import CalcConditionType
from apps.users.models import Person


class IAssignedSelector(Protocol):
    """Protocol for assigned exercise selector interface."""

    @staticmethod
    def select(
        assignation_id: int,
        exercise_slug: str,
        student: Person,
    ) -> CalcConditionType:
        """Select assigned exercise data."""


class AssignedSelectorABC(IAssignedSelector, ABC):
    """Abstract base class for assigned exercise selector."""

    @staticmethod
    @abstractmethod
    @override
    def select(
        assignation_id: int,
        exercise_slug: str,
        student: Person,
    ) -> CalcConditionType:
        """Select assigned exercise data."""
