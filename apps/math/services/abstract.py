"""Abstract base classes for services."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from django.db.models import Manager, Model

Exercise = TypeVar('Exercise', bound=Model)


class AbstractCompletionService(ABC, Generic[Exercise]):
    """Assigned exercise completion service."""

    @abstractmethod
    def add_success(self, assignation_pk: int) -> None:
        """Add a successful attempt to solve the exercise."""

    @abstractmethod
    def add_failure(self, assignation_pk: int) -> None:
        """Add an unsuccessful attempt to solve the exercise."""

    @property
    @abstractmethod
    def manager(self) -> Manager[Exercise]:
        """Get assigned exercise manager."""
