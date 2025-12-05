"""Abstract base classes for Language app services."""

from abc import ABC, abstractmethod
from typing import override

from apps.core.presenters.abc import StudyPresenterGenABC
from apps.users.models import CustomUser

from .. import types


class WordPresentationServiceABC(
    StudyPresenterGenABC[types.WordParameters, types.PresentationCaseT],
    ABC,
):
    """ABC fore Word study service."""

    @abstractmethod
    @override
    def get_presentation_case(
        self,
        user: CustomUser,
        presentation_params: types.WordParameters,
    ) -> types.PresentationCaseT:
        """Get Word study presentation case."""


class WordProgressServiceABC(ABC):
    """ABC for Update word study progress Service."""

    @abstractmethod
    def update_progress(
        self,
        user: CustomUser,
        data: types.WordProgressT,
    ) -> None:
        """Update word study progress.

        Parameters
        ----------
        user : `CustomUser`
            Current user instance.
        data : `WordProgressType`
            Update Word study progress data.

        """
