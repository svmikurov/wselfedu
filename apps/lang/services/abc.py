"""Abstract base classes for Language discipline services."""

import uuid
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
        case_uuid: uuid.UUID,
        progress_type: types.ProgressType,
    ) -> None:
        """Update word study progress.

        Parameters
        ----------
        case_uuid : `uuid.UUID`
            The UUID of the exercise case that was saved
            and provided to the client for word learning.

        progress_type : `Progress`
            Progress enumeration, may by 'known' or 'unknown'.

        """


class WordStudyDomainABC(ABC):
    """Word study service to create task case."""

    @abstractmethod
    def create(self, params: types.WordStudyParams) -> types.WordStudyCase:
        """Create word study task case."""
