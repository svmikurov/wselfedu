"""Abstract base classes for Language discipline services."""

from abc import ABC, abstractmethod
from typing import override

from apps.core.presenters.abc import StudyPresenterGenABC
from apps.users.models import CustomUser

from .. import types


class WordPresentationServiceABC(
    StudyPresenterGenABC[types.WordParamsType, types.WordDataType],
    ABC,
):
    """ABC fore Word study presenter."""

    @abstractmethod
    @override
    def get_presentation_case(
        self,
        presentation_params: types.WordParamsType,
        user: CustomUser,
    ) -> types.WordCaseType:
        """Get Word study presentation case."""


class WordProgressServiceABC(ABC):
    """ABC for Update word study progress Service."""

    @abstractmethod
    def update_progress(
        self,
        user: CustomUser,
        data: types.WordProgressType,
    ) -> None:
        """Update word study progress.

        Parameters
        ----------
        user : `CustomUser`
            Current user instance.
        data : `WordProgressType`
            Update Word study progress data.

        """


class WordStudyDomainABC(ABC):
    """Word study service to create task case."""

    @abstractmethod
    def create(self, params: types.WordStudyParams) -> types.WordStudyCase:
        """Create word study task case."""
