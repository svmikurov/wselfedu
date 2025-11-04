"""Abstract base classes for Language discipline services."""

import uuid
from abc import ABC, abstractmethod

from apps.lang import types

from ..types import WordStudyCase, WordStudyParams


class WordProgressServiceABC(ABC):
    """ABC for Update word study progress Service."""

    @abstractmethod
    def update(
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


class WordStudyServiceABC(ABC):
    """Word study service to create task case."""

    @abstractmethod
    def create(self, params: WordStudyParams) -> WordStudyCase:
        """Create word study task case."""
