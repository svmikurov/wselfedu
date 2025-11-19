"""Abstract base classes for Language discipline app."""

from abc import ABC, abstractmethod

from apps.users.models import CustomUser

from ..types import ParamsChoicesT


class WordStudyParamsPresenterABC(ABC):
    """ABC for Word study params presenter."""

    @abstractmethod
    def get_initial(self, user: CustomUser) -> ParamsChoicesT:
        """Get Word study initial params."""

    @abstractmethod
    def update_initial(self, user: CustomUser, data: object) -> None:
        """Update Word study initial params."""
