"""Abstract base classes for Language app services."""

from abc import ABC, abstractmethod
from typing import override

from apps.core.presenters.abc import StudyPresenterGenABC
from apps.users.models import Person

from .. import types


class WordPresentationServiceABC(
    StudyPresenterGenABC[types.CaseParameters, types.PresentationCaseT],
    ABC,
):
    """ABC fore Word study service."""

    @abstractmethod
    @override
    def get_presentation_case(
        self,
        user: Person,
        presentation_params: types.CaseParameters,
    ) -> types.PresentationCaseT:
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
