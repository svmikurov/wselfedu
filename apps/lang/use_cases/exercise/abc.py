"""Abstract base classes for Language app services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

from apps.core.presenters.abc import StudyPresenterGenABC

from ... import types

if TYPE_CHECKING:
    from apps.users.models import Person

    from .types import TestCase

__all__ = [
    'RegularTestServiceABC',
    'WordPresentationServiceABC',
    'WordProgressServiceABC',
]


class RegularTestServiceABC(ABC):
    """ABC for regular exercise service."""

    @abstractmethod
    def execute(self, user: Person) -> TestCase:
        """Build and return exercise case."""


class AssignedTestServiceABC(ABC):
    """ABC for assigned exercise service."""

    @abstractmethod
    def execute(self, user: Person, exercise_pk: int) -> TestCase:
        """Build and return exercise case."""


class WordPresentationServiceABC(
    StudyPresenterGenABC[types.CaseParametersAPI, types.TranslationCase],
    ABC,
):
    """ABC fore Word study service."""

    @abstractmethod
    @override
    def get_case(
        self,
        user: Person,
        case_parameters: types.CaseParametersAPI,
    ) -> types.TranslationCase:
        """Get Word study presentation case."""


class WordProgressServiceABC(ABC):
    """ABC for Update word study progress Service."""

    @abstractmethod
    def update_progress(
        self,
        user: Person,
        data: types.ProgressCase,
    ) -> None:
        """Update word study progress.

        Parameters
        ----------
        user : `Person`
            Current user instance.
        data : `WordProgressType`
            Update Word study progress data.

        """
